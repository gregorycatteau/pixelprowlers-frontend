<template>
  <footer class="footer">
    <div class="mainwrapper">
      <p class="rights">&copy; 2025 PixelProwlers. Tous droits réservés.</p>
      <ul class="list">
        <li>
          <NuxtLink to="/mentions-legales" class="link"
            >Mentions légales</NuxtLink
          >
        </li>
        <li>
          <NuxtLink to="/politique-confidentialite" class="link"
            >Politique de confidentialité</NuxtLink
          >
        </li>
        <li><NuxtLink to="/contact" class="link">Contact</NuxtLink></li>
      </ul>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Aucun script nécessaire pour le moment
</script>

<style scoped>
@reference "@/assets/css/main.css";
.fgooter {
  @apply bg-gray-800 text-white py-6;
}
.mainwrapper {
  @apply max-w-6xl mx-auto px-8 py-8 sm:px-6 lg:px-8 flex items-center justify-between;
}
.rights {
  @apply text-sm;
}
.list {
  @apply flex space-x-4;
}
.list li {
  @apply list-none;
}
.link {
  @apply text-gray-400 hover:text-white transition-colors duration-300;
}
.link:hover {
  @apply underline;
}
</style>
