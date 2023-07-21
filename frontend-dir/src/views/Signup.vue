<template>
    <div class="container">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required>
          <p v-if="!isValidEmail" class="error-message">Please enter a valid email address.</p>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
          <p v-if="!isValidPassword" class="error-message">Password must be at least 8 characters, containing at least one uppercase letter, one lowercase letter, and one number.</p>
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script>
  import { backend } from "@/backend.ts"
  
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
      };
    },
    computed: {
      isValidEmail() {
        // Simple validation for email pattern
        const emailPattern = '^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})|(([a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,}))$'; // eslint-disable-line
        const re = new RegExp(emailPattern);
        return re.test(this.email.toLowerCase());
      },
      isValidPassword() {
        // Password criteria: at least 8 characters, containing at least one uppercase letter, one lowercase letter, and one number
        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/; // eslint-disable-line
        return passwordPattern.test(this.password);
      }
    },
    methods: {
      async signup() {
        // Check for a valid email address
        if (!this.isValidEmail) {
          alert('Please enter a valid email address.');
          return;
        }
  
        // Check for a valid password
        if (!this.isValidPassword) {
          alert('Password must be at least 8 characters, containing at least one uppercase letter, one lowercase letter, and one number.');
          return;
        }
  
        // Create user data
        const user = {
          username: this.username,
          email: this.email,
          password: this.password,
        };
  
        // Make the sign up request to the backend
        try {
          const response = await backend.registerUser(user);
  
          // If successful, store the access token and redirect the user
          this.$router.push('/');
        } catch (error) {
          // If there was an error, display it
          console.error('Signup error:', error);
          alert('An error occurred during sign up. Please try again.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  button[type="submit"] {
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: #fff;
    border: none;
    cursor: pointer;
  }
  
  .error-message {
    color: red;
    margin-top: 0.5rem;
  }
  </style>
  