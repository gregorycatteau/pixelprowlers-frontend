<template>
  <article ref="cardRef" class="article-card">
    <div class="img-wrapper overflow-hidden rounded-xl">
      <img
        :src="article.image || 'https://placehold.co/600x400'"
        :alt="article.title"
        class="img w-full h-48 object-cover"
      />
    </div>
    <div class="mt-4">
      <h3 class="title text-xl font-semibold mb-2">{{ article.title }}</h3>
      <p class="summary text-sm mb-3">{{ article.summary }}</p>
      <div class="flex justify-between items-center text-xs mb-4">
        <span v-if="article.category" class="badge bg-accent text-white px-2 py-1 rounded">
          {{ article.category.name }}
        </span>
        <span v-else class="badge bg-gray-300 text-gray-700 px-2 py-1 rounded">
          Sans catégorie
        </span>
        <span class="date text-gray-400">{{ formatDate(article.created_at) }}</span>
      </div>
      <NuxtLink :to="`/blog/${article.slug}`" class="btn-primary read">
        Lire l'article
      </NuxtLink>
    </div>
  </article>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import gsap from 'gsap'

interface Article {
  slug: string
  title: string
  summary: string
  image?: string | null
  category?: {
    name: string
    slug: string
  } | null
  created_at: string
}

defineProps<{
  article: Article
}>()

const cardRef = ref<HTMLElement | null>(null)

function formatDate(d: string) {
  return new Date(d).toLocaleDateString()
}

onMounted(() => {
  const el = cardRef.value
  if (!el) return
  const img = el.querySelector('.img')
  const tl = gsap.timeline({ paused: true })
  tl.to(img, { scale: 1.05, duration: 0.4 })
    .to('.title', { textDecoration: 'underline', duration: 0.2 }, 0)
    .to('.read', { boxShadow: '0 0 8px rgba(255,255,255,0.5)', duration: 0.4 }, 0)

  el.addEventListener('mouseenter', () => tl.play())
  el.addEventListener('mouseleave', () => tl.reverse())
})
</script>

<style scoped>
@reference "@/assets/css/main.css";
.article-card {
  @apply bg-dark text-secondary rounded-2xl p-4 hover:shadow-lg transition;
}
</style>


