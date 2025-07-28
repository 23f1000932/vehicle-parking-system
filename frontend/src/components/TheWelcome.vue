<script setup>
// import WelcomeItem from './WelcomeItem.vue'
// import DocumentationIcon from './icons/IconDocumentation.vue'
// import ToolingIcon from './icons/IconTooling.vue'
// import EcosystemIcon from './icons/IconEcosystem.vue'
// import CommunityIcon from './icons/IconCommunity.vue'
// import SupportIcon from './icons/IconSupport.vue'

// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-lg">
          <div class="card-body">
            <h1 class="card-title text-center mb-4">
              Welcome to Your Digital Parking Assistant
            </h1>
            <p class="card-text lead text-center">
              This is your all-in-one digital parking assistant that makes finding and managing parking spots effortless.
              Whether you're looking for a convenient place to park your 4-wheeler or you're a parking lot owner wanting to manage your facilities, this app has you covered.
            </p>
            <div class="d-flex justify-content-center mt-4">
              <router-link to="/login" class="btn btn-primary me-2">Login
              </router-link>
              <router-link to="/register" class="btn btn-outline-secondary">Register
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
