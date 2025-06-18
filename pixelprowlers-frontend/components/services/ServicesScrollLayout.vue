<template>
  <section class="scroll-section">
    <ServicesIntro :scrollFactor="scrollFactor" :isActive="currentSection === 'intro'" />
    <ServiceList :scrollFactor="scrollFactor" :isActive="currentSection === 'list'" />
    <ServiceMethod :scrollFactor="scrollFactor" :isActive="currentSection === 'method'" />
    <EthicalStack :scrollFactor="scrollFactor" :isActive="currentSection === 'stack'" />
    <CallToAction :scrollFactor="scrollFactor" :isActive="currentSection === 'cta'" />

    <div v-if="debugVisible" class="debug">
      <p>🎯 SF: {{ scrollFactor.toFixed(2) }}</p>
      <p>📍 Section: {{ currentSection }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onBeforeUnmount, provide } from 'vue'
import { useScrollLock } from '@vueuse/core'
import gsap from 'gsap'

import ServicesIntro from '@/components/services/ServicesIntro.vue'
import ServiceList from '@/components/services/ServiceList.vue'
import ServiceMethod from '@/components/services/ServiceMethod.vue'
import EthicalStack from '@/components/services/EthicalStack.vue'
import CallToAction from '@/components/services/CallToAction.vue'

const scrollFactor = ref(0)
const scrollUnlocked = ref(true)
const maxScrollFactor = 4
const debugVisible = ref(false)

const currentSection = computed(() => {
  const sf = scrollFactor.value
  if (sf < 1) return 'intro'
  if (sf >= 1 && sf < 2) return 'list'
  if (sf >= 2 && sf < 3) return 'method'
  if (sf >= 3 && sf < 3.5) return 'stack'
  return 'cta'
})

provide('scrollFactor', scrollFactor)

onMounted(() => {
  const scrollLock = useScrollLock(document.body)
  scrollLock.value = true

  watch(scrollUnlocked, v => {
    scrollLock.value = !v
  })

  window.addEventListener('wheel', onWheel, { passive: true })
  debugVisible.value = true
})

onBeforeUnmount(() => {
  window.removeEventListener('wheel', onWheel)
})

function onWheel(e: WheelEvent) {
  if (!scrollUnlocked.value) return
  const delta = e.deltaY
  const nextValue = scrollFactor.value + delta / 800
  scrollFactor.value = Math.min(Math.max(nextValue, 0), maxScrollFactor)
}

watch(scrollFactor, val => {
  if (val > 0.01 && !scrollUnlocked.value) {
    scrollUnlocked.value = true
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