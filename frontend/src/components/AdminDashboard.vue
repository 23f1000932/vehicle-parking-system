<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// General State
const API_URL = 'http://127.0.0.1:5000';
const activeTab = ref('lots');

// State for Lots, Editing, and Users
const lots = ref([]);
const showCreateForm = ref(false);
const newLot = ref({ name: '', price: null, addr: '', pin: '', max_spots: null });
const showEditModal = ref(false);
const editingLot = ref(null);
const users = ref([]);

// Chart instance state
const lotSummaryChart = ref(null);

const renderLotSummaryChart = () => {
  if (lotSummaryChart.value) {
    lotSummaryChart.value.destroy();
  }
  const ctx = document.getElementById('lotSummaryChartCanvas');
  if (!ctx || lots.value.length === 0) return;

  const labels = lots.value.map(lot => lot.name);
  const totalSpotsData = lots.value.map(lot => lot.max_spots);
  const occupiedSpotsData = lots.value.map(lot => lot.max_spots - lot.available_spots);

  lotSummaryChart.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Total Spots',
          data: totalSpotsData,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'Occupied Spots',
          data: occupiedSpotsData,
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Total vs. Occupied Spots per Lot'
        }
      }
    }
  });
};

watch(activeTab, (newTab) => {
  if (newTab === 'summary') {
    nextTick(() => {
      renderLotSummaryChart();
    });
  }
});

// --- API Functions ---
const fetchLots = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/lots`);
    lots.value = response.data.lots;
    if (activeTab.value === 'summary') {
      nextTick(() => renderLotSummaryChart());
    }
  } catch (error) {
    console.error('Error fetching lots:', error);
  }
};

const openEditModal = (lot) => {
  editingLot.value = { ...lot };
  showEditModal.value = true;
};

const handleUpdateLot = async () => {
  if (!editingLot.value) return;
  try {
    const lotId = editingLot.value.id;
    const updateData = {
      name: editingLot.value.name,
      price: editingLot.value.price,
      addr: editingLot.value.addr,
      pin: editingLot.value.pin,
      max_spots: editingLot.value.max_spots,
    };
    const response = await axios.put(`${API_URL}/api/lots/${lotId}`, updateData);
    console.log(response.data.message);
    showEditModal.value = false;
    fetchLots();
  } catch (error) {
    console.error('Error updating lot:', error.response?.data?.message || error.message);
  }
};

const createLot = async () => {
  try {
    const response = await axios.post(`${API_URL}/api/lots`, newLot.value);
    console.log(response.data.message);
    showCreateForm.value = false;
    newLot.value = { name: '', price: null, addr: '', pin: '', max_spots: null };
    fetchLots();
  } catch (error) {
    console.error('Error creating lot:', error);
  }
};

const deleteLot = async (lotId) => {
  if (!confirm(`Are you sure you want to delete lot ID: ${lotId}?`)) return;
  try {
    const response = await axios.delete(`${API_URL}/api/lots/${lotId}`);
    console.log(response.data.message);
    fetchLots();
  } catch (error) {
    console.error('Error deleting lot:', error.response?.data?.message || 'Failed to delete lot.');
  }
};

const fetchUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/admin/users`);
    users.value = response.data.users;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

onMounted(() => {
  fetchLots();
  fetchUsers();
});
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h3>Admin Dashboard</h3>
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'lots' }" @click="activeTab = 'lots'" href="#">Manage Lots</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'" href="#">View Users</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'" href="#">Summary</a>
          </li>
        </ul>
      </div>

      <!-- Tab Content: Manage Lots -->
      <div v-if="activeTab === 'lots'" class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4>Existing Lots</h4>
          <button @click="showCreateForm = !showCreateForm" class="btn btn-primary">
            {{ showCreateForm ? 'Cancel' : 'Add New Lot' }}
          </button>
        </div>

        <div v-if="showCreateForm" class="card p-3 mb-4 bg-light">
          <form @submit.prevent="createLot">
            <h5>Create New Lot</h5>
            <div class="row g-3">
              <div class="col-md-6">
                <input type="text" v-model="newLot.name" class="form-control" placeholder="Lot Name" required>
              </div>
              <div class="col-md-6">
                <input type="number" step="0.01" v-model="newLot.price" class="form-control" placeholder="Price per Hour" required>
              </div>
              <div class="col-12">
                <input type="text" v-model="newLot.addr" class="form-control" placeholder="Address" required>
              </div>
              <div class="col-md-6">
                <input type="text" v-model="newLot.pin" class="form-control" placeholder="Pin Code" required>
              </div>
              <div class="col-md-6">
                <input type="number" v-model="newLot.max_spots" class="form-control" placeholder="Max Spots" required>
              </div>
              <div class="col-12">
                <button type="submit" class="btn btn-success">Create Lot</button>
              </div>
            </div>
          </form>
        </div>

        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Address</th>
                <th>Available</th>
                <th>Total Spots</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in lots" :key="lot.id">
                <td>{{ lot.id }}</td>
                <td>{{ lot.name }}</td>
                <td>₹{{ lot.price.toFixed(2) }}</td>
                <td>{{ lot.addr }}, {{ lot.pin }}</td>
                <td>{{ lot.available_spots }}</td>
                <td>{{ lot.max_spots }}</td>
                <td>
                  <button @click="openEditModal(lot)" class="btn btn-warning btn-sm me-2">Edit</button>
                  <button @click="deleteLot(lot.id)" class="btn btn-danger btn-sm">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="lots.length === 0">No parking lots found.</p>
      </div>

      <!-- Tab Content: View Users -->
      <div v-if="activeTab === 'users'" class="card-body">
        <h4>Registered Users</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Address</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.address }}, {{ user.pin }}</td>
                <td>
                  <span :class="user.active ? 'text-success' : 'text-danger'">{{ user.active ? 'Active' : 'Inactive' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="users.length === 0">No registered users found.</p>
      </div>
      
      <!-- Tab Content: Summary Chart -->
      <div v-if="activeTab === 'summary'" class="card-body">
        <h4>Lot Summary</h4>
        <div style="height: 400px;">
          <canvas id="lotSummaryChartCanvas"></canvas>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Lot Modal -->
  <div v-if="showEditModal" class="modal fade show" style="display: block;" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Lot #{{ editingLot.id }}</h5>
          <button type="button" class="btn-close" @click="showEditModal = false"></button>
        </div>
        <div class="modal-body">
          <form v-if="editingLot" @submit.prevent="handleUpdateLot">
            <div class="mb-3">
              <label class="form-label">Lot Name</label>
              <input type="text" v-model="editingLot.name" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Price per Hour</label>
              <input type="number" step="0.01" v-model="editingLot.price" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Address</label>
              <input type="text" v-model="editingLot.addr" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Pin Code</label>
              <input type="text" v-model="editingLot.pin" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Max Spots</label>
              <input type="number" v-model="editingLot.max_spots" class="form-control" required>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showEditModal = false">Cancel</button>
          <button type="button" class="btn btn-primary" @click="handleUpdateLot">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showEditModal" class="modal-backdrop fade show"></div>
</template>
