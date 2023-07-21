import axios, { AxiosError } from 'axios'

let $axios = axios.create({
  baseURL: 'localhost:5000/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' },
})

// Error handler
function handleErrors<T>(err: AxiosError): T {
  console.error(err.message);
  // Add any error tracking service here if needed
  return null;  // Replace null with a default response if needed
}

export interface Flashcard {
  id: string,
  word: string,
  definition: string,
  bin: number,
  next_review_time: string,
  incorrect_count: number,
  user_id: string,
}

export interface FlashcardInput {
  word: string,
  definition: string,
}

export interface User {
  username: string,
  email: string,
  password: string,
}

export let backend = {
    registerUser(user: User) {
      return $axios.post(`flashcards/register`, user).then((response) => response.data).catch(handleErrors);
    },

    loginUser(data: User) {
      return $axios.post(`flashcards/login`, data)
        .then((response) => {
          // Clear any old token
          localStorage.removeItem('accessToken');
          // Save the new token
          localStorage.setItem('accessToken', response.data.access_token);
          // Update axios headers
          return response.data;
        })
        .catch(error => {
          handleErrors(error);
          throw error;
        });
    },
    
    getFlashcards() {
      // localStorage.removeItem('accessToken');
      return $axios.get<Flashcard[]>(`flashcards/`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    getFlashcard(id: string) {
      return $axios.get<Flashcard>(`flashcards/${id}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    createFlashcard(data: FlashcardInput) {
      return $axios.post<Flashcard>(`flashcards/`, data, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    updateFlashcard(id: string, data: FlashcardInput) {
      return $axios.put<Flashcard>(`flashcards/${id}`, data, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    deleteFlashcard(id: string) {
      return $axios.delete(`flashcards/${id}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    reviewFlashcard() {
      return $axios.get<Flashcard[]>(`flashcards/review`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    },
  
    updateFlashcardStatus(id: string, status: number) {
      return $axios.put(`flashcards/${id}/status/${status}`, {}, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') }
      }).then((response) => response.data).catch(handleErrors);
    }
}
