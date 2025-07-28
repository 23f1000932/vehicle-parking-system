<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue'; // Import computed

const authStore = useAuthStore();
const router = useRouter();

const userName = computed(() => {

  return authStore.user?.name || authStore.user?.email || 'User';
});

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">Vehicle Parking System</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Logged OUT links -->
        <ul v-if="!authStore.token" class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>
        </ul>

        <!-- Logged IN links -->
        <ul v-else class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-center">
           <li class="nav-item">
            <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
          </li>
          <li class="nav-item">
            <!-- Use the safe computed property here -->
            <a class="nav-link" href="#">Welcome, {{ userName }}</a>
          </li>
          <li class="nav-item ms-2">
            <button @click="handleLogout" class="btn btn-outline-light">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
