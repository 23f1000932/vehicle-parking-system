<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Define reactive variables for registration form fields
const email = ref('');
const password = ref('');
const name = ref('');
const address = ref('');
const pin = ref('');
const authStore = useAuthStore();
const router = useRouter();

// Handle registration logic
const handleRegister = async () => {
  const userData = {
    email: email.value,
    password: password.value,
    name: name.value,
    address: address.value,
    pin: pin.value,
  };
  const success = await authStore.register(userData);
  if (success) {
    router.push('/login');
  }
};
</script>

<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="card p-4 shadow" style="min-width: 400px;">
      <h3 class="mb-4 text-center">Register</h3>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input v-model="name" type="text" id="name" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input v-model="email" type="email" id="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" id="password" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <input v-model="address" type="text" id="address" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="pin" class="form-label">Pin Code</label>
          <input v-model="pin" type="text" id="pin" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
      <hr>
      <p class="text-center mb-0">
        Already have an account? 
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>
