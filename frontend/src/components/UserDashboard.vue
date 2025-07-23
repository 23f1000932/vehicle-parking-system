<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const lots = ref([]);
const authStore = useAuthStore();
const API_URL = 'http://127.0.0.1:5000';

// Function to fetch all parking lots
const fetchLots = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/lots`);
    lots.value = response.data.lots;
  } catch (error) {
    console.error('Error fetching lots:', error);
    alert('Could not fetch parking lots.');
  }
};

// Function to handle making a reservation
const makeReservation = async (lotId) => {
  if (!confirm('Are you sure you want to reserve a spot in this lot?')) {
    return;
  }
  try {
    const response = await axios.post(`${API_URL}/api/reservations`, {
      lot_id: lotId,
      user_id: authStore.user.id
    });
    alert(response.data.message);
    fetchLots(); // Refresh lot data to show updated spot count
  } catch (error) {
    console.error('Error making reservation:', error);
    alert(error.response?.data?.message || 'Failed to make reservation.');
  }
};

// Fetch lots when the component is mounted
onMounted(() => {
  fetchLots();
});
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h3>User Dashboard - Find a Parking Spot</h3>
      </div>
      <div class="card-body">
        <div class="row">
          <div v-for="lot in lots" :key="lot.id" class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">{{ lot.name }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${{ lot.price.toFixed(2) }}/hr</h6>
                <p class="card-text">{{ lot.addr }}, {{ lot.pin }}</p>
                <p class="card-text">
                  <strong>Spots Available:</strong> {{ lot.available_spots }} / {{ lot.max_spots }}
                </p>
              </div>
              <div class="card-footer">
                <button 
                  @click="makeReservation(lot.id)" 
                  class="btn btn-primary w-100"
                  :disabled="lot.available_spots === 0">
                  {{ lot.available_spots > 0 ? 'Reserve a Spot' : 'Lot Full' }}
                </button>
              </div>
            </div>
          </div>
          <div v-if="lots.length === 0" class="col-12">
            <p>No parking lots are available at the moment.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
