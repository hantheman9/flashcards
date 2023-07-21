<template>
  <div>
    <button class="logout-button" @click="logout">Logout</button>

    <div class="hero">
      <div>
        <h1 class="display-3">Flashcards Manager</h1>
      </div>
    </div>

    <div class="container-fluid mt-4">
      <h1 class="h1">Create a Flashcard</h1>
      <CreateCard />
    </div>

    <div class="container-fluid mt-4">
      <h1 class="h1">View/ Edit Flashcards</h1>
      <ViewCards />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import CreateCard from "@/components/CreateCard.vue";
import ViewCards from "@/components/ViewCards.vue";

@Component({
  components: {
    CreateCard,
    ViewCards,
  }
})
export default class Admin extends Vue {

    logout() {
      // Remove the token from local storage
      localStorage.removeItem('accessToken');

      // Redirect the user to a "Thank You" page
      this.$router.push('/logout');
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
 
