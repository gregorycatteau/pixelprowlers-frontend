<template>
  <section class="newsletter-container">
    <!-- Illustration -->
    <div class="newsletter-illustration-wrapper">
      <img
        src="/newsletter-illustration.png"
        alt="Illustration newsletter"
        class="newsletter-illustration"
        loading="lazy"
      />
    </div>

    <!-- Texte et formulaire -->
    <div class="newsletter-content">
      <h2 class="newsletter-title">
        Reste connecté·e à l'essentiel
      </h2>
      <p class="newsletter-text">
        Une fois par mois, reçois nos meilleures ressources, actus et conseils. Zéro spam, juste de la valeur.
      </p>

      <form @submit.prevent="subscribe" class="newsletter-form">
        <input
          v-model="email"
          type="email"
          placeholder="Ton adresse email"
          class="newsletter-input"
          required
        />
        <button type="submit" class="newsletter-button">
          Je m'abonne
        </button>
      </form>

      <p v-if="message" class="newsletter-message">{{ message }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * Composant NewsletterSignup.vue
 * Version compacte, fond transparent, border et shadow light
 */

import { ref } from 'vue'

const email = ref('')
const message = ref('')

const subscribe = () => {
  if (email.value.includes('@')) {
    message.value = 'Merci pour ton inscription 🙌'
    email.value = ''
  } else {
    message.value = "Hmm... Ton email semble incorrect 😅"
  }
}
</script>

<style scoped>
@reference "@/assets/css/main.css";

.newsletter-container {
  @apply flex flex-col md:flex-row items-center justify-between max-w-3xl mx-auto bg-transparent border border-gray-700 rounded-2xl p-6 md:p-8 shadow-lg shadow-gray-700/30 gap-6;
}

.newsletter-illustration-wrapper {
  @apply w-full md:w-1/3 flex justify-center;
}

.newsletter-illustration {
  @apply w-24 md:w-28 lg:w-32 object-contain;
}

.newsletter-content {
  @apply flex flex-col w-full md:w-2/3;
}

.newsletter-title {
  @apply text-xl md:text-2xl font-bold mb-2 text-gray-100;
}

.newsletter-text {
  @apply text-sm md:text-base text-gray-300 mb-4;
}

.newsletter-form {
  @apply flex flex-col sm:flex-row gap-3 items-start sm:items-center mb-2;
}

.newsletter-input {
  @apply flex-1 px-4 py-2 text-dark bg-gray-100 rounded-md placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent transition;
}

.newsletter-button {
  @apply px-4 py-2 bg-accent text-dark font-semibold rounded-md shadow hover:bg-accent/90 transition;
}

.newsletter-message {
  @apply text-sm mt-2 text-accent;
}
</style>

