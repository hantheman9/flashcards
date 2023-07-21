<template>
    <div class="home">
     <button class="logout-button" @click="goToLogout">Logout</button>
      <h2>Welcome to our Flashcards App!</h2>
      <button @click="goToAdmin">Admin</button>
      <button @click="goToStudy">Study</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: localStorage.getItem('username'),  // username was stored in local storage after login
      };
    },
    methods: {
      goToAdmin() {
        this.$router.push('/admin');
      },
      goToStudy() {
        this.$router.push('/study');
      },
      goToLogout() {
      // Remove the token from local storage
      localStorage.removeItem('accessToken');

      // Redirect the user to a "Thank You" page
      this.$router.push('/logout');
    },
    },
  };
  </script>
  
  <style scoped>
.logout-button {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>
