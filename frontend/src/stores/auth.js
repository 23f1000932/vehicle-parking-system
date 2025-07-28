import { defineStore } from 'pinia';
import axios from 'axios';
import { ref } from 'vue';

// Define the base URL for your API
const API_URL = 'http://127.0.0.1:5000';

const getInitialUser = () => {
    const userString = localStorage.getItem('user');
    if (userString && userString !== 'undefined') {
        try {
            return JSON.parse(userString);
        } catch (e) {
            console.error("Failed to parse user from localStorage", e);
            localStorage.removeItem('user');
            return null;
        }
    }
    return null;
};

export const useAuthStore = defineStore('auth', () => {
    const user = ref(getInitialUser());
    const token = ref(localStorage.getItem('token') || null);

    async function login(email, password) {
        try {
            const response = await axios.post(`${API_URL}/api/auth/login`, { email, password });
            
            const data = response.data;
            console.log("Data received sucessfully :", data);

            user.value = data.user;
            token.value = data.auth_token;
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('token', data.auth_token);

            axios.defaults.headers.common['Authentication-Token'] = data.auth_token;
            return true;
        } catch (error) {
            console.error('Login failed:', error.response?.data?.message || error.message);
            alert('Login Failed: ' + (error.response?.data?.message || 'Server error'));
            return false;
        }
    }

    async function register(userData) {
        try {
            await axios.post(`${API_URL}/api/auth/register`, userData);
            alert('Registration successful...!! Now you can Login.');
            return true;
        } catch (error) {
            console.error('Registration failed:', error.response?.data?.message || error.message);
            alert('Registration Failed: ' + (error.response?.data?.message || 'Server error'));
            return false;
        }
    }
    // Function to log out the user
    // and clear the local storage
    function logout() {
        user.value = null;
        token.value = null;
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authentication-Token'];
        window.location.reload();
    }

    if (token.value) {
        axios.defaults.headers.common['Authentication-Token'] = token.value;
    }

    return { user, token, login, register, logout };
});
