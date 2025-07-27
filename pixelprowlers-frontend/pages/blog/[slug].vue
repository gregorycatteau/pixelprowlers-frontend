<template>
  <div v-if="article" class="article-layout">
    <!-- ASIDE GAUCHE -->
    <aside class="article-sidebar-left">
      <BlogFilter
        :articles="[article]"
        :categories="categoriesList"
        @update:category="onCategoryChange"
        @update:sort="onSortChange"
      />
    </aside>

    <!-- CONTENU CENTRAL -->
    <main class="article-main-content">
      <section class="article-top relative">
        <img
          v-if="article.image"
          :src="article.image"
          alt="Image de couverture"
          class="article-cover"
        />
        <div class="article-title-overlay">
          <h1 class="article-title-text animate-fade-in-up">
            {{ article.title }}
          </h1>
        </div>
      </section>

      <section class="article-body">
        <SectionBlock
          v-for="section in article.sections"
          :key="section.order"
          :id="`section-${section.order}`"
          :title="section.title"
          :content="section.content"
          :image="section.image"
        />

        <Footnotes class="article-footnotes" :notes="article.footnotes || []" />

        <RelatedArticles
          class="article-related"
          :articles="article.related_articles || []"
        />
      </section>
    </main>

    <!-- ASIDE DROIT -->
    <aside class="article-sidebar-right">
      <!-- On passe slug à TableOfContents -->
      <TableOfContents
        :items="tocItems"
        :slug="slug"
      />
    </aside>
  </div>

  <p v-else class="article-error">
    Article introuvable ou en cours de chargement...
  </p>

  <!-- Mount du chatbot drawer en bas de page -->
  <GuardianBot
    v-if="drawer.isOpen"
    :slug="slug"
  />
</template>

<script setup lang="ts" define:pageMeta="{ layout: 'blog' }">
import { ref, watch, computed } from 'vue'
import { useRoute, useAsyncData, useRuntimeConfig } from 'nuxt/app'
import DOMPurify from 'dompurify'

import BlogFilter      from '@/components/blog/BlogFilters.vue'
import TableOfContents from '@/components/blog/article/TableOfContents.vue'
import GuardianBot     from '@/components/blog/ranking/GuardianBot.vue'
import SectionBlock    from '@/components/blog/article/SectionBlock.vue'
import Footnotes       from '@/components/blog/article/FootNotes.vue'
import RelatedArticles from '@/components/blog/article/RelatedArticles.vue'

import { useDrawerStore } from '@/stores/drawer'

/** Types */
interface Author {
  name:    string
  role?:   string
  avatar?: string
}
interface Section {
  title:   string
  content: string
  image?:  string
  order:   number
}
interface Footnote {
  text:  string
  order: number
}
interface Article {
  id:               number
  title:            string
  slug:             string
  summary:          string
  content:          string
  created_at:       string
  image?:           string
  category: {
    id:   number
    name: string
    slug: string
  }
  authors?:         Author[]
  sections?:        Section[]
  footnotes?:       Footnote[]
  related_articles?: any[]
}
interface Category {
  id:   number
  name: string
  slug: string
}

// Drawer pour le chatbot
const drawer = useDrawerStore()

// Route & slug  
const route = useRoute()
const slug  = ref(route.params.slug as string)

// Récupération de l’URL de base depuis le runtime config  
const config  = useRuntimeConfig()
const baseURL = (config.public as any).apiBaseUrl as string

// Chargement de l’article (avec typage garantissant Article)  
const { data: article, refresh } = useAsyncData<Article>(
  `article-${slug.value}`,
  () => $fetch<Article>(`${baseURL}/blog/articles/${slug.value}/`),
  { server: false, watch: [slug] }
)

// Chargement des catégories  
const { data: categories } = useAsyncData<Category[]>(
  'categories',
  () => $fetch<Category[]>(`${baseURL}/blog/categories/`),
  { server: false }
)

// Liste de noms pour le filtre  
const categoriesList = computed<string[]>(() =>
  categories.value?.map(c => c.name) || []
)

// Rechargement quand le slug change  
watch(
  () => route.params.slug,
  (newSlug) => {
    slug.value = newSlug as string
    refresh()
  }
)

// Construction du sommaire  
const tocItems = computed(() =>
  (article.value?.sections || []).map(s => ({
    id:    `section-${s.order}`,
    title: DOMPurify.sanitize(s.title),
  }))
)

// Handlers pour le filtre  
function onCategoryChange(newCategory: string) {
  console.log('Catégorie sélectionnée :', newCategory)
}
function onSortChange(newSort: string) {
  console.log('Tri sélectionné :', newSort)
}

// Helper de format de date  
function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR', {
    year:  'numeric',
    month: 'long',
    day:   'numeric',
  })
}
</script>



<style scoped>
@reference "@/assets/css/main.css";

.article-layout {
  @apply grid grid-cols-1 gap-8 max-w-7xl mx-auto px-4 pt-10 pb-20;
}

@media (min-width: 1024px) {
  .article-layout {
    grid-template-columns: 280px 1fr 280px;
  }
}

.article-sidebar-left {
  @apply hidden lg:block sticky top-20 self-start;
}

.article-sidebar-right {
  @apply hidden lg:block sticky top-20 self-start;
}

.article-main-content {
  @apply space-y-16 top-20 self-start mt-10;
}

/* ─────── TOP IMAGE + TITLE ─────── */
.article-top {
  @apply relative rounded-xl overflow-hidden;
}

.article-cover {
  @apply w-full max-h-[28rem] object-cover opacity-60;
}

.article-title-overlay {
  @apply absolute inset-0 flex items-center justify-center;
}

.article-title-text {
  @apply backdrop-blur-lg bg-black/40 text-white text-center px-6 py-4 rounded-xl font-bold text-3xl md:text-4xl leading-tight max-w-2xl mx-auto;
}

/* ─────── ANIMATION ─────── */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.98) blur(4px);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1) blur(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out both;
}

/* ─────── RESTE DU CORPS ─────── */
.article-body {
  @apply prose prose-invert prose-lg max-w-none text-accent;
}

.article-footnotes {
  @apply text-sm text-gray-400 border-t border-gray-700 pt-6 mt-12;
}

.article-related {
  @apply mt-20 pt-10 border-t border-gray-700;
}

.article-error {
  @apply text-center py-12 text-red-500 text-lg;
}
</style>
