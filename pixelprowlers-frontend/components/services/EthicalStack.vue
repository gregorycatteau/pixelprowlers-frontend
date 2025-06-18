<template>
  <section class="sectioncontainer" ref="stackRef">
    <h2 class="maintitle">Outils libres recommandés</h2>
    <p class="subtitle">Une sélection pour un écosystème respectueux.</p>
    <div class="cardgrid">
      <div v-for="(tool, i) in tools" :key="i" class="carditem">
        <p class="cardtitle">{{ tool }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import gsap from 'gsap'

const props = defineProps<{ scrollFactor: number; isActive: boolean }>()
const stackRef = ref<HTMLElement | null>(null)
const wasVisible = ref(false)

const tools = ['Nextcloud', 'RocketChat', 'OnlyOffice', 'Peertube', 'Jitsi', 'Dolibarr']

watch(
  () => props.scrollFactor,
  async () => {
    const visible = props.isActive
    if (visible === wasVisible.value) return
    wasVisible.value = visible

    if (!stackRef.value) return
    gsap.to(stackRef.value, {
      opacity: visible ? 1 : 0,
      pointerEvents: visible ? 'auto' : 'none',
      duration: 0.8,
      ease: 'power2.out',
    })

    if (visible) {
      await nextTick()
      gsap.fromTo(
        stackRef.value.querySelectorAll('.carditem'),
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.15, duration: 1, ease: 'power2.out' }
      )
    }
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";
.sectioncontainer {
  @apply absolute top-0 left-0 w-full min-h-screen flex flex-col items-center justify-center gap-10 px-6 py-24;
  background: linear-gradient(to bottom, #eef2f5, #d7e0e7);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.8s ease-in-out;
}
.cardgrid {
  @apply grid grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl;
}
.carditem {
  @apply bg-white border border-gray-200 p-4 rounded-xl text-center shadow-sm;
}
.cardtitle {
  @apply text-base font-semibold text-gray-800;
}
</style>