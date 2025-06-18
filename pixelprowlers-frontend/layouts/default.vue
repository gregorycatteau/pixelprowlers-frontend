<template>
  <div class="default-layout">
    <!-- Background image -->
    <div
      class="background"
      style="background-image: url('/background.jpg')"
    ></div>

    <!-- Supprime temporairement navbar/footer si animation full screen -->
    <MainNavbar v-if="!isFullPage" />
    
    <main class="content">
      <slot />
    </main>

    <Footer v-if="!isFullPage" />
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import MainNavbar from "~/components/navigation/mainnavbar.vue"
import Footer from "~/components/home/footer.vue"

const route = useRoute()

// Liste des pages avec expérience immersive (sans navbar/footer)
const fullPageRoutes = ['/', '/home']
const isFullPage = fullPageRoutes.includes(route.path)
</script>

<style scoped>
@reference "@/assets/css/main.css";
.default-layout {
  @apply fixed top-0 left-0 w-full h-screen overflow-hidden z-0;
}

.background {
  @apply absolute inset-0 bg-cover bg-center -z-10;
}

.content {
  @apply w-full h-full relative z-10;
}
</style>

