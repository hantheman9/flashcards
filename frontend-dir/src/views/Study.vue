<template>
    <div>
      <button class="logout-button" @click="logout">Logout</button>

      <h1 class="display-3">Study</h1>
  
      <div v-if="flashcard">
        <h2>{{ flashcard.word }}</h2>
        
        <button @click="showDefinition = true">Show Definition</button>
  
        <div v-if="showDefinition">
        <h2>{{ flashcard.definition }}</h2>
          <button @click="answer(true)">I got it</button>
          <button @click="answer(false)">I did not get it</button>
        </div>
      </div>
  
      <div v-else>
        <p>You are temporarily done; please come back later to review more words.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { backend } from "@/backend.ts"
  
  export default {
    data() {
      return {
        flashcard: null,
        showDefinition: false
      }
    },
  
    async created() {
      this.nextFlashcard();
    },
  
    methods: {
      async nextFlashcard() {
        const result = await backend.reviewFlashcard();
        if (result.data) {
          this.flashcard = result.data;
        } else {
          this.flashcard = null;
        }
        this.showDefinition = false;
      },
  
      async answer(correct) {
        await backend.updateFlashcardStatus(this.flashcard.id, correct);
        this.nextFlashcard();
      },
      logout() {
      // Remove the token from local storage
      localStorage.removeItem('accessToken');

      // Redirect the user to a "Thank You" page
      this.$router.push('/logout');
    },
    }
  }
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