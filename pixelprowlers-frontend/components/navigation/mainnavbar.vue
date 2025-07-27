<template>
  <nav ref="navbarRef" class="main-navbar">
    <div class="maincontainer">
      <!-- Logo à gauche -->
      <div class="logo flex items-center gap-2">
        <NuxtLink to="/" class="flex items-center gap-2 link">
          <img
            src="/photo_logo.png"
            alt="Logo PixelProwlers"
            class="h-10 w-10 object-contain rounded-full"
          />
          <span class="text">PixelProwlers</span>
        </NuxtLink>
      </div>

      <!-- Actions à droite -->
      <div class="nav-actions ml-auto">
        <button class="login-button">Connexion</button>
        <button @click="toggleMenu" class="hamburger" aria-label="Menu">
          <Icon name="material-symbols:menu-rounded" size="32" />
        </button>
      </div>
    </div>

    <NavMenu :open="isOpen" @close="isOpen = false" />
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Icon from '@/components/ui/Icon.vue'
import NavMenu from '@/components/navigation/NavMenu.vue'

const isOpen = ref(false)
const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const navbarRef = ref<HTMLElement | null>(null)
onMounted(() => {
  if (navbarRef.value) {
    document.documentElement.style.setProperty('--navbar-height', `${navbarRef.value.offsetHeight}px`)
  }
})
</script>

<style scoped>
@reference "@/assets/css/main.css";

.main-navbar {
  @apply bg-transparent shadow-2xl shadow-gray-600 fixed top-0 w-full z-50;
}

.maincontainer {
  @apply flex items-center justify-between w-full px-6 py-4;
}

.logo .link {
  @apply text-2xl font-bold text-orange-400 no-underline;
}

.logo img {
  @apply h-10 w-10 object-contain;
}

.nav-actions {
  @apply flex items-center gap-4;
}

.login-button {
  @apply bg-accent text-white font-semibold px-4 py-2 rounded-md hover:bg-cyan-800 transition-colors;
}

.hamburger {
  @apply text-accent hover:text-shadow-accent transition duration-300;
}
</style>
