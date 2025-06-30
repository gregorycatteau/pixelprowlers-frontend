<template>
  <div v-if="pending" class="text-center py-8">Chargement...</div>

  <div v-else-if="article" class="blog-article-page">
    <Breadcrumb :items="breadcrumbItems" class="mb-4" />

    <section class="article-top">
      <img
        v-if="article.image"
        :src="article.image"
        alt="Image de couverture"
        class="cover-img"
      />
      <ArticleHeader
        :title="article.title"
        :date="formatDate(article.created_at)"
        :category="article.category.name"
        :authors="article.authors"
      />
    </section>

    <div class="article-body-wrapper">
      <aside class="toc-sidebar">
        <TableOfContents :items="tocItems" />
      </aside>

      <main class="article-sections">
        <template v-for="section in article.sections" :key="section.order">
          <SectionBlock
            :id="`section-${section.order}`"
            :title="section.title"
            :content="section.content"
            :image="section.image"
          />
        </template>

        <Footnotes :notes="article.footnotes || []" />
        <RelatedArticles :articles="article.related_articles || []" />
      </main>
    </div>
  </div>

  <p v-else class="text-center py-8 text-red-500">Article introuvable</p>
</template>

<script setup lang="ts">
import { useRoute, useRuntimeConfig } from '#imports'
import { ref, watch, computed } from 'vue'
import DOMPurify from 'dompurify'

import Breadcrumb from '@/components/navigation/Breadcrumb.vue'
import ArticleHeader from '@/components/blog/article/ArticleHeader.vue'
import TableOfContents from '@/components/blog/article/TableOfContents.vue'
import SectionBlock from '@/components/blog/article/SectionBlock.vue'
import Footnotes from '@/components/blog/article/FootNotes.vue'
import RelatedArticles from '@/components/blog/article/RelatedArticles.vue'

interface Author {
  name: string
  role?: string
  avatar?: string
}

interface Section {
  title: string
  content: string
  image?: string
  order: number
}

interface Footnote {
  text: string
  order: number
}

interface Article {
  id: number
  title: string
  slug: string
  summary: string
  content: string
  created_at: string
  image?: string
  category: {
    id: number
    name: string
    slug: string
  }
  authors?: Author[]
  sections?: Section[]
  footnotes?: Footnote[]
  related_articles?: any[]
}

const route = useRoute()
const slug = ref(route.params.slug as string)

const { data: article, pending, refresh } = useFetch<Article>(
  `/blog/articles/${slug.value}/`,
  {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    key: `article-${slug.value}`,
    server: false,
    watch: [slug],
  }
)

watch(
  () => route.params.slug,
  (newSlug) => {
    slug.value = newSlug as string
    refresh()
  }
)

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Breadcrumb réactif sur article
const breadcrumbItems = computed(() => {
  if (!article.value) return [{ label: 'Blog', to: '/blog' }]
  return [
    { label: 'Blog', to: '/blog' },
    { label: article.value.title }
  ]
})

// TOC items
const tocItems = computed(() =>
  (article.value?.sections || []).map((s) => ({
    id: `section-${s.order}`,
    title: DOMPurify.sanitize(s.title),
  }))
)
</script>

<style scoped>
@reference "@/assets/css/main.css";

.blog-article-page {
  @apply px-4 md:px-8 lg:px-16 mt-12;
}

.article-top {
  @apply max-w-4xl mx-auto mb-12;
}

.cover-img {
  @apply w-full max-h-96 object-cover rounded-xl shadow-lg mb-6;
}

.article-body-wrapper {
  @apply flex flex-col lg:flex-row gap-8 w-full max-w-6xl mx-auto;
}

.toc-sidebar {
  @apply w-full lg:w-1/4 sticky top-28 h-fit;
}

.article-sections {
  @apply flex-1 space-y-12 pb-20;
}
</style>

