<template>
  <header ref="heroRef" class="hero relative overflow-hidden mb-4">
    <div ref="bgRef" class="absolute inset-0 -z-10 bg-cover bg-center hero-bg" />
    <div class="py-24 text-center text-secondary">
      <h1 ref="titleRef" class="title">
        Explorations et Partages de PixelProwlers
      </h1>
      <p ref="subtitleRef" class="subtitle text-lg md:text-xl max-w-2xl mx-auto">
        Une voix, des engagements, une vision à transmettre chaque semaine.
      </p>
    </div>
  </header>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'

// Assure-toi que ScrollTrigger est bien enregistré
gsap.registerPlugin(ScrollTrigger)

const heroRef = ref<HTMLElement | null>(null)
const titleRef = ref<HTMLElement | null>(null)
const subtitleRef = ref<HTMLElement | null>(null)
const bgRef = ref<HTMLElement | null>(null)

onMounted(() => {
  const ctx = gsap.context(() => {
    // Animation d’entrée
    if (titleRef.value && subtitleRef.value) {
      gsap.from(titleRef.value, { opacity: 0, y: 30, duration: 1 })
      gsap.from(subtitleRef.value, { opacity: 0, y: 30, duration: 1, delay: 0.3 })
    }

    // Animation de fond avec scroll
    if (bgRef.value) {
      gsap.to(bgRef.value, {
        scale: 1.1,
        scrollTrigger: {
          trigger: heroRef.value,
          start: 'top top',
          scrub: true,
        },
      })
    }
  }, heroRef)

  return () => ctx.revert()
})
</script>

<style scoped>
@reference "@/assets/css/main.css";

.hero {
  @apply h-[20vh] flex items-center justify-center bg-dark;
}

.title {
  @apply text-accent text-4xl md:text-5xl font-bold mb-4;
}

.hero-bg {
  background-image: url('https://placehold.co/1600x900');
}
</style>
