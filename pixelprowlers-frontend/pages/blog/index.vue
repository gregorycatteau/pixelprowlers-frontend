<template>
  <div class="blog-page dark flex">
    <!-- Aside avec filtres -->
    <aside class="hidden lg:block fixed top-20 left-0 w-64 min-h-screen overflow-y-auto p-4 bg-dark border-r border-gray-700">

      <BlogFilters
        v-model:keyword="keyword"
        v-model:selectedCategories="selectedCategories"
        v-model:dateOrder="dateOrder"
        :categories="categories"
      />
    </aside>

    <!-- Contenu principal -->
    <main class="flex-1 ml-0 lg:ml-64 px-4 max-w-7xl mx-auto">
      <!-- Hero Article -->
      <HeroArticle :article="formattedLatestArticle" class="mb-12" />

      <!-- Newsletter -->
      <NewsletterSignup class="mb-16" />

      <!-- Articles -->
      <div v-if="pending" class="text-center py-6">Chargement...</div>
      <template v-else>
        <div
          v-if="paginatedArticles.length"
          ref="articlesRef"
          class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3"
        >
          <ArticleCard
            v-for="article in paginatedArticles"
            :key="article.id"
            :article="formatArticle(article)"
          />
        </div>
        <p v-else class="text-center py-6">Aucun article disponible.</p>

        <nav v-if="totalPages > 1" class="flex justify-center mt-8 space-x-2">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="currentPage = page"
            class="px-3 py-1 rounded"
            :class="{
              'bg-accent text-white': currentPage === page,
              'bg-dark text-secondary': currentPage !== page,
            }"
          >
            {{ page }}
          </button>
        </nav>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import gsap from 'gsap'
import BlogFilters from '@/components/blog/BlogFilters.vue'
import ArticleCard from '@/components/blog/ArticleCard.vue'
import HeroArticle from '@/components/blog/article/HeroArticle.vue'
import NewsletterSignup from '@/components/blog/article/NewsletterSignup.vue'
import { getArticles, getCategories, type Article, type Category } from '@/composables/useArticles'

const keyword = ref('')
const selectedCategories = ref<string[]>([])
const dateOrder = ref<'recent' | 'old'>('recent')

const { data: articles, pending } = await useAsyncData<Article[]>(getArticles)
const { data: catData } = await useAsyncData<Category[]>(getCategories)

const categories = computed(() => catData.value?.map((c) => c.name) ?? [])

const currentPage = ref(1)

const formatArticle = (a: Article) => ({
  ...a,
  date: a.created_at,
  image: a.image || 'https://placehold.co/600x400',
  category: typeof a.category === 'string' ? { name: a.category, slug: '' } : a.category,
})

const filteredArticles = computed(() => {
  const kw = keyword.value.toLowerCase()
  let list = (articles.value ?? []).filter((a) =>
    a.title.toLowerCase().includes(kw)
  )
  if (selectedCategories.value.length) {
    list = list.filter((a) =>
      selectedCategories.value.includes(
        typeof a.category === 'string' ? a.category : a.category.name
      )
    )
  }
  list = list.sort((a, b) => {
    return dateOrder.value === 'recent'
      ? Number(new Date(b.created_at)) - Number(new Date(a.created_at))
      : Number(new Date(a.created_at)) - Number(new Date(b.created_at))
  })
  return list
})

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * 10
  return filteredArticles.value.slice(start, start + 10)
})

const latestArticle = computed(() => filteredArticles.value[0])

const formattedLatestArticle = computed(() => latestArticle.value ? formatArticle(latestArticle.value) : null)

const totalPages = computed(() => Math.max(1, Math.ceil(filteredArticles.value.length / 10)))

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
  @apply min-h-screen bg-dark text-shadow-accent pt-10 pb-20;
}
</style>
