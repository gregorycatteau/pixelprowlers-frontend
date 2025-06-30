<template>
  <nav v-if="computedItems.length" aria-label="Breadcrumb" class="breadcrumb-nav">
    <ol class="breadcrumb-list">
      <li v-for="(item, index) in computedItems" :key="index" class="breadcrumb-item">
        <NuxtLink v-if="item.href" :to="item.href" class="breadcrumb-link">
          {{ item.label }}
        </NuxtLink>
        <span v-else class="breadcrumb-current">{{ item.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface BreadcrumbItem {
  label: string
  href?: string
}

const props = defineProps<{ items?: BreadcrumbItem[] }>()

const computedItems = computed(() => props.items ?? [])
</script>

<style scoped>
@reference "@/assets/css/main.css";
.breadcrumb-nav {
  @apply text-sm text-accent ;
  
}

.breadcrumb-list {
  @apply flex flex-wrap gap-2;
}

.breadcrumb-item::after {
  content: "/";
  @apply mx-1 text-gray-400;
}

.breadcrumb-item:last-child::after {
  content: "";
}

.breadcrumb-link {
  @apply hover:underline;
}

.breadcrumb-current {
  @apply font-semibold text-gray-800 dark:text-gray-200;
}
</style>

