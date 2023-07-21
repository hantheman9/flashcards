<template>
  <div>
    <div>
      <button v-if="selectedCard && !selectedCard.editMode" @click="editFlashcard(selectedCard)">Edit Selected Card</button>
      <button v-if="selectedCard && selectedCard.editMode" @click="updateFlashcard(selectedCard)">Save Changes</button>
      <button v-if="selectedCard" @click="deleteFlashcard(selectedCard.id)">Delete Selected Card</button>
    </div>
    <table id="flashcards-table" class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>Select</th>
          <th>Word</th>
          <th>Definition</th>
          <th>Bin</th>
          <th>Next Review Time</th>
          <th># of Incorrect Answers</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="card in cards" :key="card.id">
          <td>
            <input type="radio" v-model="selectedCard" :value="card">
          </td>
          <td>
            <input v-if="card.editMode" v-model="card.word" type="text">
            <span v-else>{{ card.word }}</span>
          </td>
          <td>
            <input v-if="card.editMode" v-model="card.definition" type="text">
            <span v-else>{{ card.definition }}</span>
          </td>
          <td>
            <input v-if="card.editMode" v-model="card.bin" type="text">
            <span v-else>{{ card.bin }}</span>
          </td>
          <td>
            <input v-if="card.editMode" v-model="card.next_review_time" type="text">
            <span v-else>{{ card.next_review_time }}</span>
          </td>
          <td>
            <input v-if="card.editMode" v-model="card.incorrect_count" type="text">
            <span v-else>{{ card.incorrect_count }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { backend } from "@/backend.ts";
import { EventBus } from '@/event-bus.js';

const binToSeconds = {
  0: 2,
  1: 5,
  2: 25,
  3: 2 * 60,
  4: 10 * 60,
  5: 1 * 60 * 60,
  6: 5 * 60 * 60,
  7: 24 * 60 * 60,
  8: 5 * 24 * 60 * 60,
  9: 25 * 24 * 60 * 60,
  10: 120 * 24 * 60 * 60,
  11: Infinity
};

export default {
  data() {
    return {
      cards: [],
      selectedCard: null,
      timer: null
    };
  },
  
  created() {
    this.refreshCards();
    EventBus.$on('flashcard-created', this.refreshCards);
  },

  beforeDestroy() {
    EventBus.$off('flashcard-created', this.refreshCards);
  },
  
  methods: {
    refreshCards() {
      backend.getFlashcards().then(cards => {
        this.cards = cards.data.map(card => ({ ...card, editMode: false }));
      }).catch(error => {
        console.error(error);
        alert('Failed to load cards');
      });
    },
    editFlashcard(card) {
      card.editMode = true;
    },
    updateFlashcard(card) {
      backend.updateFlashcard(card.id, { word: card.word, definition: card.definition, next_review_time: card.next_review_time, bin: card.bin, incorrect_count: card.incorrect_count })
        .then(() => {
          card.editMode = false;
        })
        .catch(error => {
          console.error(error);
          alert('Failed to update card');
        });
    },
    deleteFlashcard(id) {
      backend.deleteFlashcard(id).then(() => {
        this.refreshCards();
      }).catch(error => {
        console.error(error);
        alert('Failed to delete card');
      });
    },
    timeUntilNextReview(card) {
      const nextReviewTime = new Date(card.next_review_time).getTime();  // convert to milliseconds
      const currentTime = new Date().getTime();  // current time in milliseconds
      const timeRemaining = nextReviewTime - currentTime;  // calculate time remaining
      return Math.max(timeRemaining / 1000, 0);  // convert back to seconds and ensure it's not negative
    },
  },

  filters: {
    timeFormat(seconds) {
      const days = Math.floor(seconds / 86400);
      seconds -= days * 86400;
      const hours = Math.floor(seconds / 3600);
      seconds -= hours * 3600;
      const minutes = Math.floor(seconds / 60);
      seconds -= minutes * 60;
      return `${days}d ${hours}h ${minutes}m ${Math.floor(seconds)}s`;
    },
  },
}
</script>
