<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';


const email = ref('');
const password = ref('');

console.log(email.value, password.value);

</script>

<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow" style="min-width: 350px;">
      <h3 class="mb-4 text-center">Login</h3>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            v-model="email"
            type="text"
            id="email"
            class="form-control"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="form-control"
            placeholder="Enter your password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <br>
      <router-link to="/register" class="btn btn-outline-secondary">Register
              </router-link>
    </div>
  </div>
</template>
