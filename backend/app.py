from flask import Flask
from application.config import LocalDevelopmentConfig
from application.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import hash_password        



app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    return app

app = create_app()
#i want to create 
with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name = 'admin', description = "this is admin")
    app.security.datastore.find_or_create_role(name = 'user', description = "this is user")
    db.session.commit()


    if not app.security.datastore.find_user(email = "user@admin.com"):
        app.security.datastore.create_user(email = "user@admin.com",
                                           password = hash_password("1234"),
                                           roles = ['admin'])
    db.session.commit()
        

from application.auth_apis import register, login, logout
from application.crud_apis import (
    create_lot, get_all_lots, get_lot, update_lot, delete_lot,
    get_spots_by_lot, create_reservation, get_all_reservations,
    get_user_reservations, end_reservation
)

# Register the routes
app.add_url_rule('/api/auth/register', 'register', register, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['POST'])

# Register lot CRUD routes
app.add_url_rule('/api/lots', 'create_lot', create_lot, methods=['POST'])
app.add_url_rule('/api/lots', 'get_all_lots', get_all_lots, methods=['GET'])
app.add_url_rule('/api/lots/<int:lot_id>', 'get_lot', get_lot, methods=['GET'])
app.add_url_rule('/api/lots/<int:lot_id>', 'update_lot', update_lot, methods=['PUT'])
app.add_url_rule('/api/lots/<int:lot_id>', 'delete_lot', delete_lot, methods=['DELETE'])

# Register spot routes
app.add_url_rule('/api/lots/<int:lot_id>/spots', 'get_spots_by_lot', get_spots_by_lot, methods=['GET'])

# Register reservation CRUD routes
app.add_url_rule('/api/reservations', 'create_reservation', create_reservation, methods=['POST'])
app.add_url_rule('/api/reservations', 'get_all_reservations', get_all_reservations, methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>/reservations', 'get_user_reservations', get_user_reservations, methods=['GET'])
app.add_url_rule('/api/reservations/<int:reservation_id>/end', 'end_reservation', end_reservation, methods=['PUT'])


if __name__ == "__main__":
    app.run()