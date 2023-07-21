<template>
  <div class="container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
      <button type="button" @click="signup">Sign Up</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { backend } from "@/backend.ts"

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      const user = {
        username: this.username,
        password: this.password,
      };

      try {

        await backend.loginUser(user);
        this.$router.push('/home');
      } catch (error) {
        console.error('Login error:', error);
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'Authentication failed. Please check your username and password.';
        } else if (error.response && error.response.status != 200){
          this.errorMessage = 'An error occurred during login.';
        }
        this.password = ''; // Clear the password field
      }
    },
    signup() {
      this.$router.push('/signup');
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

button {
  padding: 0.5rem 1rem;
  margin-right: 1rem;
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
