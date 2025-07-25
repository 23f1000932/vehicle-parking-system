<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// General State
const API_URL = 'http://127.0.0.1:5000';
const authStore = useAuthStore();
const activeTab = ref('find');

// State for Lots & Reservations
const lots = ref([]);
const reservations = ref([]);

// State for Payment Modal
const showPaymentModal = ref(false);
const paymentDetails = ref({ reservationId: null, cost: 0, lotName: '' });

// --- Start of New Code for Charts ---
const reservationChart = ref(null); // To hold the chart instance

const renderReservationChart = () => {
  if (reservationChart.value) {
    reservationChart.value.destroy();
  }
  const ctx = document.getElementById('reservationChartCanvas');
  if (!ctx || reservations.value.length === 0) return;

  const activeCount = reservations.value.filter(r => r.status === 'Active').length;
  const completedCount = reservations.value.filter(r => r.status === 'Completed').length;

  reservationChart.value = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Active Reservations', 'Completed Reservations'],
      datasets: [{
        label: 'Reservations',
        data: [activeCount, completedCount],
        backgroundColor: [
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'My Parking History Summary'
        }
      }
    }
  });
};

watch(activeTab, (newTab) => {
  if (newTab === 'summary') {
    nextTick(() => {
      renderReservationChart();
    });
  }
});
// --- End of New Code for Charts ---


// --- API Functions ---
const fetchLots = async () => { try { const response = await axios.get(`${API_URL}/api/lots`); lots.value = response.data.lots; } catch (error) { console.error('Error fetching lots:', error); } };
const makeReservation = async (lotId) => { try { const response = await axios.post(`${API_URL}/api/reservations`, { lot_id: lotId, user_id: authStore.user.id }); console.log('Reservation successful:', response.data.message); fetchLots(); fetchReservations(); activeTab.value = 'history'; } catch (error) { console.error('Error making reservation:', error.response?.data?.message || error.message); } };
const fetchReservations = async () => { if (!authStore.user) return; try { const response = await axios.get(`${API_URL}/api/users/${authStore.user.id}/reservations`); reservations.value = response.data.reservations; if (activeTab.value === 'summary') { renderReservationChart(); } } catch (error) { console.error('Error fetching reservations:', error); } };
const prepareToEndReservation = async (reservation) => { try { const response = await axios.get(`${API_URL}/api/reservations/${reservation.id}/calculate_cost`); paymentDetails.value = { reservationId: reservation.id, cost: response.data.total_cost, lotName: reservation.lot_name, }; showPaymentModal.value = true; } catch (error) { console.error('Error calculating cost:', error.response?.data?.message || error.message); } };
const handlePayment = async () => { if (!paymentDetails.value.reservationId) return; try { const response = await axios.put(`${API_URL}/api/reservations/${paymentDetails.value.reservationId}/end`); console.log("Payment successful!", response.data.message); showPaymentModal.value = false; fetchLots(); fetchReservations(); } catch (error) { console.error('Error during final payment:', error.response?.data?.message || error.message); } };
const formatDate = (dateString) => { if (!dateString) return 'N/A'; return new Date(dateString).toLocaleString(); };

onMounted(() => {
  fetchLots();
  fetchReservations();
});
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h3>User Dashboard</h3>
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item"><a class="nav-link" :class="{ active: activeTab === 'find' }" @click="activeTab = 'find'" href="#">Find a Spot</a></li>
          <li class="nav-item"><a class="nav-link" :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'" href="#">My Reservations</a></li>
          <!-- New Summary Tab -->
          <li class="nav-item"><a class="nav-link" :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'" href="#">Summary</a></li>
        </ul>
      </div>

      <!-- Tab Content: Find a Spot -->
      <div v-if="activeTab === 'find'" class="card-body">
        <!-- Lot finding UI (no changes) -->
        <div class="row"><div v-for="lot in lots" :key="lot.id" class="col-md-6 col-lg-4 mb-4"><div class="card h-100"><div class="card-body"><h5 class="card-title">{{ lot.name }}</h5><h6 class="card-subtitle mb-2 text-muted">₹{{ lot.price.toFixed(2) }}/hr</h6><p class="card-text">{{ lot.addr }}, {{ lot.pin }}</p><p class="card-text"><strong>Spots Available:</strong> {{ lot.available_spots }} / {{ lot.max_spots }}</p></div><div class="card-footer"><button @click="makeReservation(lot.id)" class="btn btn-primary w-100" :disabled="lot.available_spots === 0">{{ lot.available_spots > 0 ? 'Reserve a Spot' : 'Lot Full' }}</button></div></div></div><div v-if="lots.length === 0" class="col-12"><p>No parking lots are available at the moment.</p></div></div>
      </div>

      <!-- Tab Content: My Reservations -->
      <div v-if="activeTab === 'history'" class="card-body">
        <!-- Reservation history table (no changes) -->
        <h4>My Reservation History</h4><div class="table-responsive"><table class="table table-striped"><thead><tr><th>Lot Name</th><th>Address</th><th>Time In</th><th>Time Out</th><th>Status</th><th>Action</th></tr></thead><tbody><tr v-for="res in reservations" :key="res.id"><td>{{ res.lot_name }}</td><td>{{ res.lot_address }}</td><td>{{ formatDate(res.time_in) }}</td><td>{{ formatDate(res.time_out) }}</td><td><span class="badge" :class="res.status === 'Active' ? 'bg-success' : 'bg-secondary'">{{ res.status }}</span></td><td><button v-if="res.status === 'Active'" @click="prepareToEndReservation(res)" class="btn btn-info btn-sm">End Reservation</button></td></tr></tbody></table></div><p v-if="reservations.length === 0">You have no reservation history.</p>
      </div>

      <!-- Tab Content: Summary Chart -->
      <div v-if="activeTab === 'summary'" class="card-body">
        <h4>My Parking Summary</h4>
        <div style="height: 400px; max-width: 500px; margin: auto;">
          <canvas id="reservationChartCanvas"></canvas>
        </div>
        <p v-if="reservations.length === 0" class="text-center mt-3">You have no parking data to display.</p>
      </div>
    </div>
  </div>

  <!-- Payment Modal (no changes) -->
  <div v-if="showPaymentModal" class="modal fade show" style="display: block;" tabindex="-1"><div class="modal-dialog modal-dialog-centered"><div class="modal-content"><div class="modal-header"><h5 class="modal-title">Confirm Payment</h5><button type="button" class="btn-close" @click="showPaymentModal = false"></button></div><div class="modal-body"><p>You are about to end your reservation for <strong>{{ paymentDetails.lotName }}</strong>.</p><h4>Total Cost: ₹{{ paymentDetails.cost.toFixed(2) }}</h4><p class="text-muted small">This is a simulated payment.</p></div><div class="modal-footer"><button type="button" class="btn btn-secondary" @click="showPaymentModal = false">Cancel</button><button type="button" class="btn btn-success" @click="handlePayment">Pay Now</button></div></div></div></div>
  <div v-if="showPaymentModal" class="modal-backdrop fade show"></div>
</template>
