<template>
  <div class="home-layout">
    <MainNavbar />
    <main class="content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import MainNavbar from '~/components/navigation/mainnavbar.vue'
</script>

<style scoped>
.home-layout {
  @apply min-h-screen flex flex-col;
}
.content {
  @apply flex-grow;
}
</style>

