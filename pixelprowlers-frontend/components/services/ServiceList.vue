<template>
  <section class="sectioncontainer" ref="listRef">
    <h2 class="maintitle">Des services pensés pour vous</h2>
    <p class="subtitle">Des solutions ouvertes et solidaires, adaptées à chaque projet.</p>
    <div class="cardgrid">
      <div v-for="(svc, i) in services" :key="i" class="carditem">
        <h3 class="cardtitle">{{ svc.title }}</h3>
        <p class="cardtext">{{ svc.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import gsap from 'gsap'

const props = defineProps<{ scrollFactor: number; isActive: boolean }>()
const listRef = ref<HTMLElement | null>(null)
const wasVisible = ref(false)

const services = [
  { title: 'Site web', desc: 'Conception de vitrines accessibles et durables.' },
  { title: 'Outils collaboratifs', desc: 'Nextcloud, pads et wikis pour travailler ensemble.' },
  { title: 'Hébergement', desc: 'Serveurs éthiques pour vos données et vos applications.' },
  { title: 'Maintenance', desc: 'Suivi et mises à jour pour garder l’outil fiable.' },
  { title: 'Formation', desc: 'Ateliers pour prendre en main vos outils.' },
  { title: 'Cybersécurité', desc: 'Protection et bonnes pratiques pour votre structure.' },
]

watch(
  () => props.scrollFactor,
  async () => {
    const visible = props.isActive
    if (visible === wasVisible.value) return
    wasVisible.value = visible

    if (!listRef.value) return
    gsap.to(listRef.value, {
      opacity: visible ? 1 : 0,
      pointerEvents: visible ? 'auto' : 'none',
      duration: 0.8,
      ease: 'power2.out',
    })

    if (visible) {
      await nextTick()
      gsap.fromTo(
        listRef.value.querySelectorAll('.carditem'),
        { y: 40, opacity: 0, scale: 0.95 },
        { y: 0, opacity: 1, scale: 1, stagger: 0.2, duration: 1.2, ease: 'power3.out' }
      )
    }
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";
.sectioncontainer {
  @apply absolute top-0 left-0 w-full min-h-screen flex flex-col items-center justify-center gap-10 px-6 py-24;
  background: linear-gradient(to bottom, #f9f7f3, #eae3d9);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.8s ease-in-out;
}
.cardgrid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl;
}
.carditem {
  @apply bg-white border border-gray-200 p-6 rounded-2xl shadow-md;
}
.cardtitle {
  @apply text-lg font-semibold mb-2 text-center text-gray-800;
}
.cardtext {
  @apply text-base text-center text-gray-600;
}
</style>