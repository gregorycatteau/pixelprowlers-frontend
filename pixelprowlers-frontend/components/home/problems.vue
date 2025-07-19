<template>
  <section class="problems-container" ref="problemsRef">
    <div class="parallax-background" ref="parallaxRef"></div>
    <RainCanvas />

    <!-- Lignes d’intro -->
    <div class="intro-wrapper">
      <p
        v-for="(line, i) in introLinesBefore"
        :key="'intro-' + i"
        class="intro-line"
      >
        {{ line }}
      </p>
    </div>

    <!-- Cartes -->
    <div class="cards-wrapper">
      <div
        v-for="(card, index) in cardsBefore"
        :key="'card-' + index"
        class="problem-card"
      >
        <div class="card-icon">
          <img :src="card.img" alt="" class="card-img" />
        </div>
        <h3 class="card-title">{{ card.title }}</h3>
        <p class="card-description">{{ card.description }}</p>
      </div>
    </div>

    <!-- CTA -->
    <div class="cta-container">
      <button class="cta-button">
        Brisez la glace. Reprenez le contrôle.
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue"
import { gsap } from "gsap"
import RainCanvas from '@/components/animation/RainCanvas.vue'

const props = defineProps<{
  scrollFactor: number
  isActive: boolean
}>()

const problemsRef = ref<HTMLElement | null>(null)
const parallaxRef = ref<HTMLElement | null>(null)

const introLinesBefore = [
  "Un froid silence entoure vos actions.",
  "Personne ne voit. Personne n’entend.",
  "Vous avancez dans la brume, seul, figé entre urgence et épuisement.",
  "Et les outils censés aider ? Aussi glacés qu’inaccessibles."
]

interface Card {
  img: string
  title: string
  description: string
}

const cardsBefore: Card[] = [
  {
    img: "/invisible.png",
    title: "Impact gelé",
    description:
      "Ce que vous bâtissez est réel, mais enseveli sous la neige de l’indifférence."
  },
  {
    img: "/time-missing.png",
    title: "Temps figé",
    description:
      "Chaque instant se fige dans le givre des urgences. Le sens se perd dans le froid."
  },
  {
    img: "/complexity.png",
    title: "Technologie inhospitalière",
    description:
      "Des interfaces glaciales, conçues sans vous. Un labyrinthe gelé où rien ne pousse."
  }
]

watch(
  () => props.scrollFactor,
  async (val) => {
    if (!problemsRef.value) return

    const visible = val >= 1 && val < 1.5

    // Apparition / disparition de la section
    if (typeof gsap.to === 'function') {
      gsap.to(problemsRef.value, {
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? "auto" : "none",
        duration: 0.8,
        ease: "power2.out"
      })
    }

    // Parallax background
    if (parallaxRef.value && typeof gsap.to === 'function') {
      gsap.to(parallaxRef.value, {
        y: -val * 100,
        scale: 1.05,
        duration: 0.6,
        ease: "power2.out"
      })
    }

    if (visible) {
      await nextTick()

      if (typeof gsap.fromTo === 'function') {
        gsap.fromTo(
          ".intro-line",
          { y: 30, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            stagger: 0.3,
            duration: 1.5,
            ease: "power3.out"
          }
        )

        gsap.fromTo(
          ".problem-card",
          { y: 60, opacity: 0, scale: 0.95 },
          {
            y: 0,
            opacity: 1,
            scale: 1,
            stagger: 0.4,
            duration: 1.8,
            ease: "power4.out"
          }
        )

        gsap.fromTo(
          ".cta-container",
          { opacity: 0, y: 20 },
          {
            opacity: 1,
            y: 0,
            duration: 1.2,
            delay: 2,
            ease: "power2.out"
          }
        )
      }
    }
  }
)
</script>

<style scoped>
@reference "@/assets/css/main.css";

.problems-container {
  @apply relative w-full min-h-screen flex flex-col items-center justify-center px-6 py-24 gap-16;
  background-image: url("/brume-fond.png"), linear-gradient(to bottom, #1c1f23dd, #0a0d11cc);
  background-size: cover;
  background-position: center;
  backdrop-filter: blur(6px) brightness(0.7);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.5s ease-in-out;
}

.intro-wrapper {
  @apply max-w-3xl text-center space-y-4;
}

.intro-line {
  @apply text-2xl md:text-3xl font-light leading-snug;
  font-family: 'Orbitron', sans-serif;
  color: #032369;
  text-shadow: 
    0 0 4px rgba(163, 196, 224, 0.6),
    0 0 12px rgba(255, 255, 255, 0.1);
}

.cards-wrapper {
  @apply flex flex-wrap gap-10 justify-center;
}

.problem-card {
  @apply w-80 p-6 rounded-2xl transition-transform;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease-in-out;
}

.problem-card:hover {
  transform: scale(1.05);
  box-shadow: 0 0 32px rgba(173, 216, 230, 0.3);
}

.card-icon {
  @apply mb-4;
}

.card-img {
  @apply w-full h-48 object-cover rounded-xl;
  filter: brightness(0.75) contrast(1.1) grayscale(30%);
  transition: filter 0.3s ease;
}

.card-title {
  @apply text-xl font-semibold mb-2 text-center;
  font-family: 'Orbitron', sans-serif;
  color: #04266b;
  letter-spacing: 0.03em;
  text-shadow: 0 0 6px rgba(200, 220, 255, 0.15);
}

.card-description {
  @apply text-base text-center;
  font-family: 'Exo 2', sans-serif;
  color: #032369;
}

.cta-container {
  @apply mt-2;
}

.cta-button {
  @apply px-6 py-3 rounded-full font-semibold transition;
  background: linear-gradient(to right, #6dd5fa, #2980b9);
  color: #f8f9ff;
  box-shadow: 0 4px 20px rgba(0, 130, 255, 0.4);
  backdrop-filter: blur(4px);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.cta-button:hover {
  background: linear-gradient(to right, #5ac8fa, #1e5b91);
  box-shadow: 0 6px 28px rgba(100, 180, 255, 0.5);
}

.parallax-background {
  @apply absolute inset-0 z-0;
  background-image: url("/brumes.png");
  background-size: cover;
  background-position: center;
  will-change: transform;
  pointer-events: none;
  filter: brightness(0.7) blur(4px);
  transition: transform 0.1s linear;
}
</style>
