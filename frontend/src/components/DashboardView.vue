<script setup>
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import AdminDashboard from './AdminDashboard.vue';
import UserDashboard from './UserDashboard.vue';

const authStore = useAuthStore();

// Determine if the user is an admin
const isAdmin = computed(() => {
  return authStore.user?.roles?.includes('admin');
});

</script>

<template>
  <div>
    <AdminDashboard v-if="isAdmin" />
    <UserDashboard v-else />
  </div>
</template>
