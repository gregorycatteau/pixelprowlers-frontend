<template>
  <section class="whoiam-container" ref="whoIAmRef">
    <!-- Texte d'intro par lettre -->
    <div class="intro-wrapper">
      <div
        v-for="(line, i) in introLines"
        :key="'whoiam-intro-' + i"
        class="intro-line"
      >
        <span
          v-for="(char, j) in line.split('')"
          :key="'char-' + i + '-' + j"
          class="intro-char"
        >
          {{ char === ' ' ? '\u00A0' : char }}
        </span>
      </div>
    </div>

    <!-- Cartes -->
    <div class="cards-wrapper">
      <div
        v-for="(card, index) in cards"
        :key="'whoiam-card-' + index"
        class="whoiam-card"
      >
        <div class="card-icon">
          <img :src="card.img" alt="" class="card-img" />
        </div>
        <h3 class="card-title">{{ card.title }}</h3>
        <p class="card-description">{{ card.description }}</p>
      </div>
    </div>

    <!-- Citation finale -->
    <div class="quote-wrapper">
      <blockquote class="quote-text">
        « Je code pour aimer, pour croire, pour bâtir. »
      </blockquote>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { gsap } from 'gsap'

const props = defineProps<{
  scrollFactor: number
  isActive: boolean
}>()

const whoIAmRef = ref<HTMLElement | null>(null)
const wasVisible = ref(false)

const introLines = [
  "Je ne suis pas une agence.",
  "Je suis un artisan du web. Un développeur qui a longtemps été de l'autre côté.",
  "J’ai monté des assos, vendu sur les marchés, soigné des gens, formé des groupes.",
  "Je sais ce que c’est de vouloir changer les choses, sans le temps ni les moyens.",
  "Aujourd’hui, je mets mon savoir-faire au service de ceux qui bâtissent du lien."
]

interface Card {
  img: string
  title: string
  description: string
}

const cards: Card[] = [
  {
    img: "/companion.jpg",
    title: "Un compagnon de route",
    description: "PixelProwlers, c’est une main tendue, pas une prestation froide. Une vraie aventure humaine."
  },
  {
    img: "/solidarity.png",
    title: "Une offre solidaire",
    description: "Tarifs éthiques, solutions évolutives, accompagnement patient. Ici, on avance ensemble."
  },
  {
    img: "/roots.png",
    title: "Des racines communes",
    description: "Je viens de là où vous êtes : terrain, terrain, terrain. Ce que je propose, je l’ai éprouvé."
  }
]

watch(
  () => props.scrollFactor,
  async () => {
    const visible = props.isActive
    if (visible === wasVisible.value) return
    wasVisible.value = visible

    if (!whoIAmRef.value) return

    if (typeof gsap.to === 'function') {
      gsap.to(whoIAmRef.value, {
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? 'auto' : 'none',
        duration: 0.8,
        ease: 'power2.out'
      })
    }

    if (visible && typeof gsap.fromTo === 'function') {
      await nextTick()
      const el = whoIAmRef.value

      gsap.fromTo(
        el.querySelectorAll('.intro-char'),
        { y: 40, opacity: 0, rotationX: -90 },
        {
          y: 0,
          opacity: 1,
          rotationX: 0,
          stagger: {
            amount: 1.2,
            from: "start"
          },
          duration: 0.8,
          ease: 'power2.out'
        }
      )

      gsap.fromTo(
        el.querySelectorAll('.whoiam-card'),
        { y: 40, opacity: 0, scale: 0.95 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          stagger: 0.3,
          duration: 1.5,
          ease: 'power3.out'
        }
      )

      gsap.fromTo(
        el.querySelector('.quote-text'),
        { opacity: 0, y: 10 },
        {
          opacity: 1,
          y: 0,
          delay: 1.2,
          duration: 1,
          ease: 'power1.out'
        }
      )
    }
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";

.whoiam-container {
  @apply absolute top-0 left-0 w-full min-h-screen flex flex-col items-center justify-center px-6 py-24 gap-20;
  background: linear-gradient(to bottom, #f9f7f3, #eae3d9);
  z-index: 30;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.8s ease-in-out;
}

.intro-wrapper {
  @apply max-w-4xl text-center space-y-4;
}

.intro-line {
  @apply text-xl md:text-2xl font-light text-gray-800 leading-relaxed;
  font-family: 'Merriweather', serif;
  display: inline-block;
  white-space: pre-wrap;
}

.intro-char {
  display: inline-block;
  transform-origin: bottom left;
  will-change: transform, opacity;
}

.cards-wrapper {
  @apply flex flex-wrap gap-10 justify-center;
}

.whoiam-card {
  @apply w-80 bg-white border border-gray-200 p-6 rounded-2xl shadow-md transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-lg;
  background-color: rgba(255, 255, 255, 0.92);
  will-change: transform, opacity;
}

.card-icon {
  @apply mb-4 flex justify-center;
}

.card-img {
  @apply w-full h-48 object-contain rounded-xl;
  filter: brightness(0.96) contrast(1.1);
}

.card-title {
  @apply text-lg font-semibold mb-2 text-center text-gray-800;
}

.card-description {
  @apply text-base text-center text-gray-600;
}

.quote-wrapper {
  @apply mt-10 text-center;
}

.quote-text {
  @apply italic text-lg text-gray-700;
  font-family: 'Georgia', serif;
}
</style>
