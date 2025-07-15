<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';


const email = ref('');
const password = ref('');

console.log(email.value, password.value);

const onSubmit = function(){
  
}

</script>

<template>
    
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card p-4 shadow" style="min-width: 350px;">
      <h3 class="mb-4 text-center">Register</h3>
      <form @submit.prevent="register" >
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

        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input
            v-model="name"
            type="text"
            id="name"
            class="form-control"
            placeholder="Enter your Full Name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <input
            v-model="address"
            type="text"
            id="address"
            class="form-control"
            placeholder="Enter your Address"
            required
          />
        </div>

        

        <div class="mb-3">
          <label for="pin" class="form-label">Pin Code</label>
          <input
            v-model="pin"
            type="integer"
            id="pin"
            class="form-control"
            placeholder="Enter your Pin Code"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
      <br>
      <router-link to="/login" class="btn btn-outline-secondary">Login
              </router-link>
    </div>
  </div>
</template>
