<template>
  <div class="cta-mainwrapper">
    <h3 class="cta-title">Rejoignez notre mission</h3>
    <p class="cta-subtitle">Ensemble, faisons avancer vos projets vers le succès.</p>
    <button class="cta-button">
      Découvrir nos solutions
    </button>
  </div>
</template>
     

<script setup lang="ts">
// Aucun script nécessaire pour le moment
</script>

<style scoped>
@reference "@/assets/css/main.css";
.cta-mainwrapper {
  @apply bg-gradient-to-r from-blue-500 to-purple-600 text-white text-center py-12 px-4 sm:px-6 lg:px-8 rounded-lg shadow-lg;
}
.cta-title {
  @apply text-3xl font-bold mb-4;
} 
.cta-subtitle {
  @apply text-xl mb-6;
}
.cta-button {
  @apply bg-white text-blue-600 font-semibold py-2 px-4 rounded-lg shadow hover:bg-gray-100 transition-colors duration-300;
}
.cta-button:hover {
  @apply bg-gray-100;
}
</style>