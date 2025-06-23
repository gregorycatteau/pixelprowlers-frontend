<template>
  <div class="blog-page dark">
    <BlogHero />
    <div class="max-w-6xl mx-auto px-4">
      <BlogFilters
        v-model:keyword="keyword"
        v-model:selectedCategories="selectedCategories"
        v-model:dateOrder="dateOrder"
        :categories="categories"
        class="mb-8"
      />
      <div
        ref="articlesRef"
        class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3"
      >
        <ArticleCard
          v-for="article in filteredArticles"
          :key="article.id"
          :article="article"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import gsap from 'gsap'
import BlogHero from '@/components/blog/BlogHero.vue'
import BlogFilters from '@/components/blog/BlogFilters.vue'
import ArticleCard from '@/components/blog/ArticleCard.vue'

interface Article {
  id: number
  slug: string // Optional for filtering purposes
  title: string
  summary: string
  category: string
  date: string
  image: string
}

const articlesMock: Article[] = [
  {
    id: 1,
    slug: 'premiers-pas-avec-nuxt-3',
    title: 'Premiers pas avec Nuxt 3',
    summary: "Découvrez comment démarrer un projet Nuxt 3 et pourquoi l'utiliser.",
    category: 'techniques',
    date: '2024-05-05',
    image: 'https://placehold.co/600x400',
  },
  {
    id: 2,
    slug: 'partenariat-associatif-en-2025',
    title: 'Partenariat associatif en 2025',
    summary: 'Retour sur nos collaborations et ce que cela apporte à la communauté.',
    category: 'partenariats',
    date: '2024-05-12',
    image: 'https://placehold.co/600x400',
  },
  {
    id: 3,
    slug: 'reflexions-societales',
    title: 'Réflexions sociétales',
    summary: 'Comment le numérique peut servir un futur plus solidaire et durable.',
    category: 'sociétales',
    date: '2024-05-19',
    image: 'https://placehold.co/600x400',
  },
]

const keyword = ref('')
const selectedCategories = ref<string[]>([])
const dateOrder = ref<'recent' | 'old'>('recent')

const categories = Array.from(new Set(articlesMock.map((a) => a.category)))

const filteredArticles = computed(() => {
  const kw = keyword.value.toLowerCase()
  let list = articlesMock.filter((a) =>
    a.title.toLowerCase().includes(kw)
  )
  if (selectedCategories.value.length) {
    list = list.filter((a) =>
      selectedCategories.value.includes(a.category)
    )
  }
  list = list.sort((a, b) => {
    return dateOrder.value === 'recent'
      ? Number(new Date(b.date)) - Number(new Date(a.date))
      : Number(new Date(a.date)) - Number(new Date(b.date))
  })
  return list
})

const articlesRef = ref<HTMLElement | null>(null)

onMounted(async () => {
  await nextTick()
  if (articlesRef.value) {
    gsap.fromTo(
      articlesRef.value.children,
      { opacity: 0, y: 40 },
      { opacity: 1, y: 0, stagger: 0.1, duration: 0.8, ease: 'power2.out' }
    )
  }
})
</script>

<style scoped>
@reference "@/assets/css/main.css";
.blog-page {
  @apply min-h-screen bg-dark text-secondary pt-10 pb-20;
}
</style>