<template>
  <section class="sectioncontainer" ref="methodRef">
    <h2 class="maintitle">Notre méthode</h2>
    <p class="subtitle">Co-construction et accompagnement de chaque étape.</p>
    <ul class="methodlist">
      <li v-for="(step, i) in steps" :key="i" class="methoditem">{{ step }}</li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import gsap from 'gsap'

const props = defineProps<{ scrollFactor: number; isActive: boolean }>()
const methodRef = ref<HTMLElement | null>(null)
const wasVisible = ref(false)

const steps = [
  'Diagnostic partagé et objectifs clairs',
  'Ateliers de co-conception',
  'Accessibilité et sobriété numérique',
  'Formation continue de vos équipes'
]

watch(
  () => props.scrollFactor,
  async () => {
    const visible = props.isActive
    if (visible === wasVisible.value) return
    wasVisible.value = visible

    if (!methodRef.value) return
    gsap.to(methodRef.value, {
      opacity: visible ? 1 : 0,
      pointerEvents: visible ? 'auto' : 'none',
      duration: 0.8,
      ease: 'power2.out',
    })

    if (visible) {
      await nextTick()
      gsap.fromTo(
        methodRef.value.querySelectorAll('.methoditem'),
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.2, duration: 1.2, ease: 'power2.out' }
      )
    }
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";
.sectioncontainer {
  @apply absolute top-0 left-0 w-full min-h-screen flex flex-col items-center justify-center gap-8 px-6 py-24;
  background-image: url('/brume-fond.png');
  background-size: cover;
  background-position: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.8s ease-in-out;
}
.methodlist {
  @apply space-y-4 max-w-3xl text-center;
}
.methoditem {
  @apply text-lg text-gray-800;
}
</style>