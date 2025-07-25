<template>
  <div class="hero-wrapper" ref="heroWrapper">
    <div class="hero-panels">
      <div class="panel panel-left"></div>
      <div class="panel panel-center"></div>
      <div class="panel panel-right"></div>
      <div class="cta">
        <button class="cta-button">Parlez-nous de vous</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import gsap from 'gsap'

const props = defineProps<{
  scrollFactor: number
  isActive: boolean
}>()

const heroWrapper = ref<HTMLElement | null>(null)

watch(
  () => props.scrollFactor,
  (progress) => {
    if (!heroWrapper.value) return

    const maxHeroProgress = 0.9
    const clamped = Math.min(progress, maxHeroProgress)
    const normalized = clamped / maxHeroProgress

    // Panel gauche
    gsap.to(heroWrapper.value.querySelector(".panel-left"), {
      rotateY: normalized * 90,
      xPercent: -normalized * 100,
      duration: 0.3,
      ease: 'power2.out'
    })

    // Panel droit
    gsap.to(heroWrapper.value.querySelector(".panel-right"), {
      rotateY: -normalized * 90,
      xPercent: normalized * 100,
      duration: 0.3,
      ease: 'power2.out'
    })

    // Panel centre
    gsap.to(heroWrapper.value.querySelector(".panel-center"), {
      rotateX: normalized * 60,
      yPercent: normalized * 20,
      opacity: 1 - normalized,
      duration: 0.3,
      ease: 'power2.out'
    })

    // CTA
    gsap.to(heroWrapper.value.querySelector(".cta"), {
      opacity: 1 - normalized,
      scale: 1 - normalized * 0.3,
      duration: 0.3,
      ease: 'power2.out'
    })

    // Wrapper global
    gsap.to(heroWrapper.value, {
      opacity: 1 - normalized,
      pointerEvents: normalized >= 1 ? "none" : "auto",
      duration: 0.5,
      ease: 'power2.out'
    })
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";

.hero-wrapper {
  @apply fixed top-0 left-0 w-full h-screen overflow-hidden;
  perspective: 2000px;
  z-index: 10;
  opacity: 1;
  pointer-events: auto;
}

.hero-panels {
  @apply flex w-full h-full relative;
  transform-style: preserve-3d;
}

.panel {
  @apply flex-1 h-full;
  background-image: url("/hero-background.png");
  background-size: 300% 100%;
  background-repeat: no-repeat;
  transform-style: preserve-3d;
  will-change: transform;
}

.panel-left {
  background-position: left center;
  transform-origin: right center;
}

.panel-center {
  background-position: center center;
  transform-origin: top center;
}

.panel-right {
  background-position: right center;
  transform-origin: left center;
}

.cta {
  @apply absolute bottom-8 left-1/2 transform -translate-x-1/2;
}

.cta-button {
  @apply bg-accent text-white px-6 py-3 rounded-full font-semibold shadow-lg hover:bg-cyan-800 transition;
}
</style>

