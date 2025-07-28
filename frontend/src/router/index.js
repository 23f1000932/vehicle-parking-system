import { createRouter, createWebHistory } from 'vue-router'
import TheWelcome from '../components/TheWelcome.vue'
import LoginView from '../components/login.vue'
import RegisterView from '../components/register.vue'
import DashboardView from '../components/DashboardView.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // This is the default route
      path: '/',
      name: 'home',
      component: TheWelcome
    },
    {
      // Route for the login page
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      // Route for the registration page
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      // Route for the dashboard, which is protected
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true } // This route requires authentication
    }
  ]
})

// Navigation Guard to protect routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
