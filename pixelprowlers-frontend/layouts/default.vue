<template>
  <div class="default-layout">
    <MainNavbar />
    <div class="breadcrumb-bar">
      <GlobalBreadcrumb />
    </div>
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import MainNavbar from '~/components/navigation/mainnavbar.vue'
import GlobalBreadcrumb from '~/components/navigation/Breadcrumb.vue'
</script>

<style scoped>
@reference "@/assets/css/main.css";

:root {
  --navbar-height: 64px; /* Fallback statique si jamais le JS n'a pas encore injecté la hauteur réelle */
}

.default-layout {
  padding-top: var(--navbar-height);
  @apply flex flex-col min-h-screen bg-neutral-50 dark:bg-neutral-900 text-neutral-800 dark:text-neutral-200;
}

.breadcrumb-bar {
  @apply bg-neutral-100 dark:bg-neutral-800 border-b border-neutral-200 dark:border-neutral-700;
}

.main-content {
  @apply flex-grow px-4 md:px-8 lg:px-12 pt-6;
}
</style>




