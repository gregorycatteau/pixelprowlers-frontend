<template>
  <div class="blog-layout">
    <MainNavbar />
    <div class="breadcrumb-bar">
      <GlobalBreadcrumb />
    </div>
    <div class="blog-content-wrapper">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import MainNavbar from '@/components/navigation/mainnavbar.vue'
import GlobalBreadcrumb from '~/components/navigation/Breadcrumb.vue'
</script>

<style scoped>
@reference "@/assets/css/main.css";

:root {
  --navbar-height: 64px; /* fallback statique, ou tu peux ajuster si besoin */
}

.blog-layout {
  @apply flex flex-col min-h-screen bg-neutral-50 dark:bg-neutral-900 text-neutral-800 dark:text-neutral-200;
}

.breadcrumb-bar {
  @apply bg-neutral-100 dark:bg-neutral-800 border-b border-neutral-200 dark:border-neutral-700;
}

.blog-content-wrapper {
  @apply grid lg:grid-cols-[1fr_3fr_1fr] gap-8 w-full max-w-7xl mx-auto flex-1 h-[calc(100vh-var(--navbar-height))];
  padding-top: var(--navbar-height);
}

.blog-content-wrapper > main {
  @apply flex flex-col overflow-y-auto h-full;
}

.blog-content-wrapper > aside {
  @apply hidden lg:block sticky top-[var(--navbar-height)] h-fit;
}
</style>
