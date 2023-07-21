<template>
  <div>
    <form @submit.prevent="createCard">
      <label>Word:</label>
      <input v-model="card.word" required>
      <label>Definition:</label>
      <input v-model="card.definition" required>
      <button type="submit">Create</button>
      <!-- Display error message -->
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <!-- Display success message -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script>
import { backend } from "@/backend.ts"
import { EventBus } from '@/event-bus.js';

export default {
  name: 'CreateCard',
  data() {
    return {
      card: {
        word: '',
        definition: '',
      },
      errorMessage: '',
      successMessage: '',
    }
  },
  methods: {
    async createCard() {
      try {
        const response = await backend.createFlashcard(this.card);
        if (response === null) {
          this.errorMessage = 'A flashcard with this word already exists';
          this.successMessage = ''; // Reset success message when an error occurs
          return;
        }
        this.card.word = '';
        this.card.definition = '';
        this.errorMessage = '';
        this.successMessage = 'Flashcard created successfully';
        EventBus.$emit('flashcard-created');
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Failed to create Flashcard';
        this.successMessage = ''; // Reset success message when an error occurs
      }
    }
  }
}
</script>

<style scoped>
.error-message {
  color: red;
}

.success-message {
  color: green;
}
</style>
