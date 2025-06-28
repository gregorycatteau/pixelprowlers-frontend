<template>
  <div v-if="pending" class="text-center py-6">Chargement...</div>
  <article v-else-if="article" class="article-wrapper">
    <section class="cover-image" ref="coverRef">
      <img
        :src="article.image || 'https://placehold.co/1200x600'"
        alt="Image de couverture"
        class="cover-img"
      />
    </section>

    <section class="body-section">
      <NuxtLink to="/blog" ref="backBtnRef" class="back-btn">
        &larr; Tous les articles
      </NuxtLink>
      <h1 ref="titleRef" class="article-title">
        {{ article.title }}
      </h1>
      <p class="meta">
        {{ formatDate(article.created_at) }} • {{ article.category.name }}
      </p>
      <div
        ref="contentRef"
        class="article-content"
        v-html="article.content"
      />
    </section>
  </article>
  <p v-else class="text-center py-6 text-red-400">Article introuvable</p>
</template>

<script setup lang="ts">
import { useRoute, useRuntimeConfig } from '#imports'
import { ref, onMounted, watch } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

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
}

const route = useRoute()
const slug = ref(route.params.slug as string)

const { data: article, pending, error, refresh } = useFetch<Article>(
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
  return new Date(date).toLocaleDateString()
}

const titleRef = ref<HTMLElement | null>(null)
const coverRef = ref<HTMLElement | null>(null)
const contentRef = ref<HTMLElement | null>(null)
const backBtnRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!process.client || !article.value) return

  const ctx = gsap.context(() => {
    if (titleRef.value) {
      gsap.from(titleRef.value, {
        y: 40,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out',
      })
    }

    if (contentRef.value) {
      const paragraphs = contentRef.value.querySelectorAll('p, blockquote')
      if (paragraphs.length > 0) {
        gsap.from(paragraphs, {
          opacity: 0,
          y: 20,
          stagger: 0.2,
          duration: 0.6,
          ease: 'power2.out',
        })
      }
    }

    if (coverRef.value) {
      const img = coverRef.value.querySelector('img')
      if (img) {
        gsap.to(img, {
          scale: 1.1,
          scrollTrigger: {
            trigger: coverRef.value,
            start: 'top top',
            scrub: true,
          },
        })
      }
    }

    if (backBtnRef.value) {
      backBtnRef.value.addEventListener('mouseenter', () => {
        gsap.to(backBtnRef.value!, { scale: 1.05, duration: 0.2 })
      })
      backBtnRef.value.addEventListener('mouseleave', () => {
        gsap.to(backBtnRef.value!, { scale: 1, duration: 0.2 })
      })
    }
  })

  return () => ctx.revert()
})
</script>



<style scoped>
@reference "@/assets/css/main.css";

.article-wrapper {
  @apply bg-transparent dark:text-secondary flex flex-col min-h-screen;
}

.cover-image {
  @apply w-full h-72 md:h-[60vh] overflow-hidden;
}

.cover-img {
  @apply w-full h-full object-cover;
}

.body-section {
  @apply mx-auto px-4 py-8 md:py-12 w-full max-w-3xl space-y-6;
}

.article-title {
  @apply font-display text-4xl md:text-5xl font-bold;
}

.meta {
  @apply text-sm text-gray-400 mb-4;
}

.article-content {
  @apply max-w-[65ch] leading-relaxed space-y-6;
}

.article-content blockquote {
  @apply border-l-4 border-violet-400 pl-4 italic text-violet-300;
}

.back-btn {
  @apply text-accent mb-6 inline-block transition-transform;
}
</style>

