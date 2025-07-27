<template>
  <div class="toc-block">
    <!-- Score dynamique (optionnel : à remplir via un store ou API) -->
    <p class="toc-score text-sm mb-2">
      {{ totalRaters }} membres ont contribué
      à noter cet article à {{ averageRating }}/5
    </p>

    <!-- Toggle de l’évaluation -->
    <div class="rating-toggle mb-4">
      <button @click="showRating = !showRating" class="rating-button">
        {{ showRating ? 'Fermer l’évaluation' : 'Exprimez-vous' }}
      </button>
    </div>

    <!-- Composant de notation -->
    <ArticleRating
      v-if="showRating"
      class="rating-component mb-6"
      :slug="slug"
    />

    <!-- Sommaire -->
    <h3 class="toc-title">Sommaire</h3>
    <ul class="toc-list mb-6">
      <li v-for="item in items" :key="item.id">
        <a :href="`#${item.id}`" class="toc-link">{{ item.title }}</a>
      </li>
    </ul>

    <!-- Commentaires validés -->
    <CommentsList
      :slug="slug"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import ArticleRating  from '@/components/blog/ranking/ArticleRating.vue'
import CommentsList   from '@/components/blog/ranking/CommentList.vue'
import { useCommentsStore } from '@/stores/comments'

/** Props reçues */
const props = defineProps<{
  items: { id: string; title: string }[]
  slug:  string
}>()

const showRating = ref(false)
const comments    = useCommentsStore()

// On charge les commentaires dès que le composant monte
onMounted(() => {
  comments.fetchComments(props.slug)
})

// Simples placeholders : adapte-les à ton propre flux de métriques
const totalRaters    = computed(() => comments.list.length)
const averageRating  = computed(() => {
  // si tu exposes avg via API, utilise-le, sinon retourne une valeur statique
  return comments.list.length
    ? (comments.list.reduce((sum, c) => sum + c.upvotes, 0) / comments.list.length).toFixed(1)
    : '0.0'
})

</script>

<style scoped>
@reference "@/assets/css/main.css";

.toc-block {
  @apply bg-gray-900/95 border border-white text-white rounded-xl p-4 shadow-md;
}

.toc-score {
  @apply text-center text-xs text-gray-300;
}

.rating-toggle {
  @apply text-center ring-2 ring-accent rounded-lg p-2;
}

.rating-button {
  @apply text-white hover:text-accent hover:underline transition-colors text-sm font-semibold;
}

.rating-component {
  @apply mb-6;
}

.toc-title {
  @apply font-bold text-lg mb-4 text-center text-white;
}

.toc-list {
  @apply flex flex-col space-y-2;
}

.toc-link {
  @apply text-sm text-accent hover:text-white transition-colors;
}
</style>

