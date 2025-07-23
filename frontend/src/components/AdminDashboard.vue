<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// State for lots
const lots = ref([]);
const showCreateForm = ref(false);
const newLot = ref({
  name: '',
  price: null,
  addr: '',
  pin: '',
  max_spots: null
});

// State for users
const users = ref([]);

const API_URL = 'http://127.0.0.1:5000';
const activeTab = ref('lots'); // 'lots' or 'users'

// --- LOTS API Functions ---
const fetchLots = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/lots`);
    lots.value = response.data.lots;
  } catch (error) {
    console.error('Error fetching lots:', error);
    alert('Could not fetch parking lots.');
  }
};

const createLot = async () => {
  try {
    const response = await axios.post(`${API_URL}/api/lots`, newLot.value);
    alert(response.data.message);
    showCreateForm.value = false;
    newLot.value = { name: '', price: null, addr: '', pin: '', max_spots: null }; // Reset form
    fetchLots();
  } catch (error) {
    console.error('Error creating lot:', error);
    alert('Failed to create lot.');
  }
};

// --- Start of New Code ---
// Function to delete a parking lot
const deleteLot = async (lotId) => {
  if (!confirm(`Are you sure you want to delete lot ID: ${lotId}? This action cannot be undone.`)) {
    return;
  }
  try {
    const response = await axios.delete(`${API_URL}/api/lots/${lotId}`);
    alert(response.data.message);
    fetchLots(); // Refresh the list after deletion
  } catch (error) {
    console.error('Error deleting lot:', error);
    // Display the specific error message from the backend if available
    alert(error.response?.data?.message || 'Failed to delete lot.');
  }
};
// --- End of New Code ---


// --- USERS API Function ---
const fetchUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/admin/users`);
    users.value = response.data.users;
  } catch (error) {
    console.error('Error fetching users:', error);
    alert('Could not fetch registered users.');
  }
};

// Fetch initial data when component mounts
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
        <!-- Tab Navigation -->
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'lots' }" @click="activeTab = 'lots'" href="#">Manage Lots</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'" href="#">View Users</a>
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

        <!-- Form to create a new lot -->
        <div v-if="showCreateForm" class="card p-3 mb-4 bg-light">
          <form @submit.prevent="createLot">
             <h5>Create New Lot</h5>
             <div class="row g-3">
              <div class="col-md-6"><input type="text" v-model="newLot.name" class="form-control" placeholder="Lot Name" required></div>
              <div class="col-md-6"><input type="number" step="0.01" v-model="newLot.price" class="form-control" placeholder="Price per Hour" required></div>
              <div class="col-12"><input type="text" v-model="newLot.addr" class="form-control" placeholder="Address" required></div>
              <div class="col-md-6"><input type="text" v-model="newLot.pin" class="form-control" placeholder="Pin Code" required></div>
              <div class="col-md-6"><input type="number" v-model="newLot.max_spots" class="form-control" placeholder="Max Spots" required></div>
              <div class="col-12"><button type="submit" class="btn btn-success">Create Lot</button></div>
            </div>
          </form>
        </div>

        <!-- Table to display existing lots -->
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th><th>Name</th><th>Price</th><th>Address</th><th>Available</th><th>Total Spots</th>
                <!-- Add Actions column header -->
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in lots" :key="lot.id">
                <td>{{ lot.id }}</td><td>{{ lot.name }}</td><td>${{ lot.price.toFixed(2) }}</td>
                <td>{{ lot.addr }}, {{ lot.pin }}</td><td>{{ lot.available_spots }}</td><td>{{ lot.max_spots }}</td>
                <!-- Add cell with Delete button -->
                <td>
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
                <th>ID</th><th>Name</th><th>Email</th><th>Address</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td><td>{{ user.name }}</td><td>{{ user.email }}</td>
                <td>{{ user.address }}, {{ user.pin }}</td>
                <td><span :class="user.active ? 'text-success' : 'text-danger'">{{ user.active ? 'Active' : 'Inactive' }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="users.length === 0">No registered users found.</p>
      </div>
    </div>
  </div>
</template>
