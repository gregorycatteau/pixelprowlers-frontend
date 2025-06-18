<template>
  <section class="sectioncontainer" ref="ctaRef">
    <blockquote class="quote-text">Prêt à donner vie à vos idées&nbsp;?</blockquote>
    <a href="https://calendly.com" class="cta-button" target="_blank" rel="noopener">Planifier un échange</a>
  </section>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import gsap from 'gsap'

const props = defineProps<{ scrollFactor: number; isActive: boolean }>()
const ctaRef = ref<HTMLElement | null>(null)

watch(
  () => props.scrollFactor,
  () => {
    if (!ctaRef.value) return
    gsap.to(ctaRef.value, {
      opacity: props.isActive ? 1 : 0,
      pointerEvents: props.isActive ? 'auto' : 'none',
      duration: 0.8,
      ease: 'power2.out',
    })
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";
.sectioncontainer {
  @apply absolute top-0 left-0 w-full min-h-screen flex flex-col items-center justify-center gap-6 px-6 py-24;
  background: linear-gradient(to bottom, #f9f7f3, #eae3d9);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.8s ease-in-out;
}
.quote-text {
  @apply italic text-xl text-gray-700 text-center;
  font-family: 'Georgia', serif;
}
.cta-button {
  @apply bg-accent text-white px-6 py-3 rounded-full font-semibold shadow-lg hover:bg-cyan-800 transition;
}
</style>