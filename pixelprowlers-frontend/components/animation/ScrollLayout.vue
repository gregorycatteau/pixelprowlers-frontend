<template>
  <section class="scroll-section">
    <Hero :scrollFactor="scrollFactor" :isActive="currentSection === 'hero'" />
    <Problems :scrollFactor="scrollFactor" :isActive="currentSection === 'problems'" />
    <WhoIAm :scrollFactor="scrollFactor" :isActive="currentSection === 'whoiam'" />

    <div v-if="props.debugVisible" class="debug">
      <p>🎯 SF: {{ scrollFactor.toFixed(2) }}</p>
      <p>📍 Section: {{ currentSection }}</p>
    </div>
  </section>
</template>


<script setup lang="ts">
import { ref, watch, computed, onMounted, onBeforeUnmount, provide } from 'vue'
import { useScrollLock } from '@vueuse/core'
import gsap from 'gsap'
import Hero from '@/components/home/hero.vue'
import Problems from '@/components/home/problems.vue'
import WhoIAm from '@/components/home/whoIAm.vue'

const props = withDefaults(defineProps<{
  debugVisible?: boolean
}>(), {
  debugVisible: false
})

const scrollFactor = ref(0)
const scrollUnlocked = ref(true)
const maxScrollFactor = 3

const currentSection = computed(() => {
  const sf = scrollFactor.value
  if (sf < 1) return 'hero'
  if (sf >= 1 && sf < 1.5) return 'problems'
  if (sf >= 1.5 && sf < 2.2) return 'whoiam'
  return 'next'
})

provide('scrollFactor', scrollFactor)

onMounted(() => {
  const scrollLock = useScrollLock(document.body)
  scrollLock.value = true

  watch(scrollUnlocked, (v) => {
    scrollLock.value = !v
  })

  window.addEventListener('wheel', onWheel, { passive: true })
  console.log('📦 scrollLayout mounted – scrollFactor is ready to rock')
})

onBeforeUnmount(() => {
  window.removeEventListener('wheel', onWheel)
})

function onWheel(e: WheelEvent) {
  if (!scrollUnlocked.value) {
    console.warn("⛔ Scroll is locked")
    return
  }

  const delta = e.deltaY
  const nextValue = scrollFactor.value + delta / 800
  scrollFactor.value = Math.min(Math.max(nextValue, 0), maxScrollFactor)
}

watch(scrollFactor, (val) => {
  if (val > 0.01 && !scrollUnlocked.value) {
    scrollUnlocked.value = true
    console.log('🔓 Scroll unlocked via mouvement')
  }
})
</script>


<style scoped>
@reference "@/assets/css/main.css";

.scroll-section {
  @apply fixed top-0 left-0 w-full h-screen overflow-hidden;
  z-index: 0;
  background: transparent;
}

.debug {
  @apply fixed top-2 left-2 text-sm bg-black/80 text-green-400 px-4 py-2 rounded z-50;
  font-family: monospace;
  pointer-events: none;
}
</style>
