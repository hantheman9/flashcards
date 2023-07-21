<template>
    <div>
      <h1>Thank you for using our app!</h1>
      <p>We hope to see you again soon.</p>
      <button @click="loginAgain">Log in again</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      loginAgain() {
        // Redirect the user to the login page
        this.$router.push('/');
      }
    }
  };
  </script>
  