from application.models import db, Lot, Spot, Reservation, User, Role
from flask import request, jsonify, current_app
from flask_security import Security
from datetime import datetime

# =============== LOT CRUD APIs ===============

def create_lot():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['name', 'price', 'addr', 'pin', 'max_spots']):
            return jsonify({'message': 'Missing required fields: name, price, addr, pin, max_spots'}), 400
        
        new_lot = Lot(
            name=data['name'],
            price=data['price'],
            addr=data['addr'],
            pin=data['pin'],
            max_spots=data['max_spots']
        )
        
        db.session.add(new_lot)
        db.session.commit()
        
        # Create spots for the lot
        for i in range(data['max_spots']):
            spot = Spot(lot_id=new_lot.id, status='A')  # A = Available
            db.session.add(spot)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lot created successfully',
            'lot': {
                'id': new_lot.id,
                'name': new_lot.name,
                'price': new_lot.price,
                'addr': new_lot.addr,
                'pin': new_lot.pin,
                'max_spots': new_lot.max_spots
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating lot: {str(e)}'}), 500

def get_all_lots():
    try:
        lots = Lot.query.all()
        lots_list = []
        
        for lot in lots:
            available_spots = Spot.query.filter_by(lot_id=lot.id, status='A').count()
            lots_list.append({
                'id': lot.id,
                'name': lot.name,
                'price': lot.price,
                'addr': lot.addr,
                'pin': lot.pin,
                'max_spots': lot.max_spots,
                'available_spots': available_spots
            })
        
        return jsonify({'lots': lots_list}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching lots: {str(e)}'}), 500

def get_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        if not lot:
            return jsonify({'message': 'Lot not found'}), 404
        
        available_spots = Spot.query.filter_by(lot_id=lot.id, status='A').count()
        occupied_spots = Spot.query.filter_by(lot_id=lot.id, status='O').count()
        
        return jsonify({
            'lot': {
                'id': lot.id,
                'name': lot.name,
                'price': lot.price,
                'addr': lot.addr,
                'pin': lot.pin,
                'max_spots': lot.max_spots,
                'available_spots': available_spots,
                'occupied_spots': occupied_spots
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching lot: {str(e)}'}), 500

def update_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        if not lot:
            return jsonify({'message': 'Lot not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            lot.name = data['name']
        if 'price' in data:
            lot.price = data['price']
        if 'addr' in data:
            lot.addr = data['addr']
        if 'pin' in data:
            lot.pin = data['pin']
        if 'max_spots' in data:
            old_max = lot.max_spots
            new_max = data['max_spots']
            lot.max_spots = new_max
            
            # Adjust spots if max_spots changed
            if new_max > old_max:
                # Add new spots
                for i in range(new_max - old_max):
                    spot = Spot(lot_id=lot.id, status='A')
                    db.session.add(spot)
            elif new_max < old_max:
                # Remove excess spots (only if they're available)
                spots_to_remove = Spot.query.filter_by(lot_id=lot.id, status='A').limit(old_max - new_max).all()
                for spot in spots_to_remove:
                    db.session.delete(spot)
        
        db.session.commit()
        
        return jsonify({'message': 'Lot updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error updating lot: {str(e)}'}), 500

def delete_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        if not lot:
            return jsonify({'message': 'Lot not found'}), 404
        
        # Check if there are active reservations
        active_reservations = Reservation.query.join(Spot).filter(
            Spot.lot_id == lot_id,
            Reservation.time_out.is_(None)
        ).count()
        
        if active_reservations > 0:
            return jsonify({'message': 'Cannot delete lot with active reservations'}), 400
        
        # Delete all spots and reservations for this lot
        spots = Spot.query.filter_by(lot_id=lot_id).all()
        for spot in spots:
            Reservation.query.filter_by(spot_id=spot.id).delete()
            db.session.delete(spot)
        
        db.session.delete(lot)
        db.session.commit()
        
        return jsonify({'message': 'Lot deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error deleting lot: {str(e)}'}), 500

# =============== SPOT CRUD APIs ===============

def get_spots_by_lot(lot_id):
    try:
        lot = Lot.query.get(lot_id)
        if not lot:
            return jsonify({'message': 'Lot not found'}), 404
        
        spots = Spot.query.filter_by(lot_id=lot_id).all()
        spots_list = []
        
        for spot in spots:
            spot_data = {
                'id': spot.id,
                'lot_id': spot.lot_id,
                'status': spot.status
            }
            
            # If spot is occupied, get reservation details
            if spot.status == 'O':
                reservation = Reservation.query.filter_by(spot_id=spot.id, time_out=None).first()
                if reservation:
                    spot_data['reservation'] = {
                        'id': reservation.id,
                        'user_id': reservation.user_id,
                        'time_in': reservation.time_in.isoformat(),
                        'rate': reservation.rate
                    }
            
            spots_list.append(spot_data)
        
        return jsonify({'spots': spots_list}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching spots: {str(e)}'}), 500

# =============== RESERVATION CRUD APIs ===============

def create_reservation():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['lot_id', 'user_id']):
            return jsonify({'message': 'Missing required fields: lot_id, user_id'}), 400
        
        # Find available spot in the lot
        available_spot = Spot.query.filter_by(lot_id=data['lot_id'], status='A').first()
        if not available_spot:
            return jsonify({'message': 'No available spots in this lot'}), 400
        
        # Get lot price
        lot = Lot.query.get(data['lot_id'])
        if not lot:
            return jsonify({'message': 'Lot not found'}), 404
        
        # Create reservation
        new_reservation = Reservation(
            spot_id=available_spot.id,
            user_id=data['user_id'],
            rate=lot.price
        )
        
        # Update spot status to occupied
        available_spot.status = 'O'
        
        db.session.add(new_reservation)
        db.session.commit()
        
        return jsonify({
            'message': 'Reservation created successfully',
            'reservation': {
                'id': new_reservation.id,
                'spot_id': new_reservation.spot_id,
                'user_id': new_reservation.user_id,
                'time_in': new_reservation.time_in.isoformat(),
                'rate': new_reservation.rate,
                'lot_name': lot.name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating reservation: {str(e)}'}), 500

def get_all_reservations():
    try:
        reservations = Reservation.query.all()
        reservations_list = []
        
        for reservation in reservations:
            spot = Spot.query.get(reservation.spot_id)
            lot = Lot.query.get(spot.lot_id)
            user = User.query.get(reservation.user_id)
            
            reservations_list.append({
                'id': reservation.id,
                'spot_id': reservation.spot_id,
                'user_email': user.email,
                'lot_name': lot.name,
                'time_in': reservation.time_in.isoformat(),
                'time_out': reservation.time_out.isoformat() if reservation.time_out else None,
                'rate': reservation.rate,
                'status': 'Active' if reservation.time_out is None else 'Completed'
            })
        
        return jsonify({'reservations': reservations_list}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching reservations: {str(e)}'}), 500

def get_user_reservations(user_id):
    try:
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        reservations_list = []
        
        for reservation in reservations:
            spot = Spot.query.get(reservation.spot_id)
            lot = Lot.query.get(spot.lot_id)
            
            reservations_list.append({
                'id': reservation.id,
                'spot_id': reservation.spot_id,
                'lot_name': lot.name,
                'lot_address': lot.addr,
                'time_in': reservation.time_in.isoformat(),
                'time_out': reservation.time_out.isoformat() if reservation.time_out else None,
                'rate': reservation.rate,
                'status': 'Active' if reservation.time_out is None else 'Completed'
            })
        
        return jsonify({'reservations': reservations_list}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching user reservations: {str(e)}'}), 500

def end_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({'message': 'Reservation not found'}), 404
        
        if reservation.time_out:
            return jsonify({'message': 'Reservation already completed'}), 400
        
        # End the reservation
        reservation.time_out = datetime.utcnow()
        
        # Free up the spot
        spot = Spot.query.get(reservation.spot_id)
        spot.status = 'A'
        
        db.session.commit()
        
        # Calculate duration and total cost
        duration = reservation.time_out - reservation.time_in
        hours = duration.total_seconds() / 3600
        total_cost = hours * reservation.rate
        
        return jsonify({
            'message': 'Reservation ended successfully',
            'duration_hours': round(hours, 2),
            'total_cost': round(total_cost, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error ending reservation: {str(e)}'}), 500
    

def get_all_users():
    """
    Retrieves all users with the 'user' role.
    Accessible only by an admin.
    """
    try:
        # Find the 'user' role object
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            return jsonify({'message': "'user' role not found"}), 500

        # Filter users who have the 'user' role
        users = User.query.filter(User.roles.contains(user_role)).all()
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'address': user.address,
                'pin': user.pin,
                'active': user.active
            })
            
        return jsonify({'users': users_list}), 200

    except Exception as e:
        return jsonify({'message': f'Error fetching users: {str(e)}'}), 500

    
