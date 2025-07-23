<script setup>
// --- Start of Correction ---
// 1. Import 'computed' from Vue
import { computed } from 'vue';
// --- End of Correction ---

import { useAuthStore } from '@/stores/auth';
import AdminDashboard from './AdminDashboard.vue';
import UserDashboard from './UserDashboard.vue';

const authStore = useAuthStore();

// --- Start of Correction ---
// 2. Wrap the isAdmin check in a 'computed' property.
// This makes it reactive and prevents errors if authStore.user is initially null.
const isAdmin = computed(() => {
  return authStore.user?.roles?.includes('admin');
});
// --- End of Correction ---

</script>

<template>
  <div>
    <!-- This template now safely renders the correct dashboard -->
    <AdminDashboard v-if="isAdmin" />
    <UserDashboard v-else />
  </div>
</template>
