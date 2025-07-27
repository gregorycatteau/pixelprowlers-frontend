<template>
  <div class="rating-block">
    <h4 class="rating-title">Cet article est utile ?</h4>

    <!-- Boucle sur les critères -->
    <div
      v-for="criterion in criteria"
      :key="criterion.key"
      class="rating-criterion"
    >
      <span class="criterion-label">{{ criterion.label }}</span>
      <div class="stars">
        <button
          v-for="n in 5"
          :key="n"
          @click="setRating(criterion.key, n)"
          class="star-button"
          :class="{ active: feedback.ratings[criterion.key] >= n }"
        >
          ★
        </button>
      </div>
    </div>

    <!-- Bouton de validation / ouverture du drawer -->
    <button
      :disabled="!canSubmit"
      @click="onSubmit"
      class="action-button"
    >
      {{ feedback.hasRated ? 'Exprimez‑vous' : 'Valider mes notes' }}
    </button>
  </div>
</template>

<script setup lang="ts">
// Composables & stores
import { computed } from 'vue'
import { useFeedbackStore } from '@/stores/feedback'
import { useDrawerStore }   from '@/stores/drawer'

// Props (slug de l’article)
const props = defineProps<{ slug: string }>()

// Stores
const feedback = useFeedbackStore()
const drawer   = useDrawerStore()

// Critères à noter
interface Ratings {
  impact: number
  clarity: number
  utility: number
}

const criteria: { key: keyof Ratings; label: string }[] = [
  { key: 'impact',  label: 'Impact' },
  { key: 'clarity', label: 'Clarté' },
  { key: 'utility', label: 'Utilité' },
]

// Condition pour activer le bouton
const canSubmit = computed(() =>
  Object.values(feedback.ratings).some(v => v > 0)
)

/**
 * Met à jour la note d’un critère
 */
function setRating(key: keyof Ratings, value: number) {
  feedback.setRating(key, value)
}

/**
 * Soumet la note puis ouvre le drawer
 */
async function onSubmit() {
  if (!feedback.hasRated) {
    await feedback.submitFeedback(props.slug)
  }
  drawer.open()
}
</script>

<style scoped>
@reference "@/assets/css/main.css";

.rating-block {
  @apply bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-2xl text-white shadow-xl;
}

.rating-title {
  @apply text-2xl font-bold mb-4 text-center;
}

.rating-criterion {
  @apply mb-4;
}

.criterion-label {
  @apply block mb-2 text-base;
}

.stars {
  @apply flex gap-3;
}

.star-button {
  @apply text-3xl text-gray-400 hover:text-yellow-400 transition-transform transform hover:scale-110;
}

.star-button.active {
  @apply text-yellow-400;
}

.action-button {
  @apply w-full py-3 font-bold rounded-xl bg-yellow-500 hover:bg-yellow-600 text-black transition;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
}
</style>
