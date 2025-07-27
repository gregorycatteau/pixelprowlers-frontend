<template>
  <aside class="comments-aside mt-8">
    <!-- Bouton d'ouverture avec compteur -->
    <button @click="toggle" class="text-blue-500 font-medium focus:outline-none">
      {{ isOpen ? 'Cacher' : 'Afficher' }} les commentaires ({{ totalValidated }} validés)
    </button>

    <transition name="fade">
      <div v-if="isOpen" class="mt-4 space-y-6">
        <!-- Commentaires paginés -->
        <div
          v-for="c in paginatedComments"
          :key="c.id"
          class="comment-item p-4 rounded"
        >
          <header class="flex items-center mb-2">
            <h4 class="font-semibold text-gray-900 dark:text-white">{{ c.author }}</h4>
            <div class="ml-auto flex space-x-1">
              <!-- Icônes de pertinence -->
              <svg v-if="c.tags.includes('humour')" class="w-5 h-5 text-yellow-400" title="Humour" fill="currentColor" viewBox="0 0 20 20">
                <!-- Heroicon : face-smile -->
                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm-3-7a1 1 0 112 0 1 1 0 01-2 0zm6 0a1 1 0 112 0 1 1 0 01-2 0zm-6.832 2.445a.75.75 0 01.06-1.06 4.5 4.5 0 016.544 0 .75.75 0 11-1.12 1.004 3 3 0 00-4.304 0 .75.75 0 01-1.06-.06z"/>
              </svg>
              <svg v-if="c.tags.includes('emotion')" class="w-5 h-5 text-red-400" title="Émotion" fill="currentColor" viewBox="0 0 20 20">
                <!-- Heroicon : heart -->
                <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 015.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
              </svg>
              <svg v-if="c.tags.includes('a-mediter')" class="w-5 h-5 text-blue-400" title="À méditer" fill="currentColor" viewBox="0 0 20 20">
                <!-- Heroicon : light-bulb -->
                <path d="M11 3a1 1 0 10-2 0c0 .628.252 1.237.707 1.707A4.002 4.002 0 007 11a4 4 0 004 4 4 4 0 004-4 4.002 4.002 0 00-2.293-6.293A1.993 1.993 0 0111 3z"/>
              </svg>
              <svg v-if="c.tags.includes('pertinence')" class="w-5 h-5 text-green-400" title="Pertinent" fill="currentColor" viewBox="0 0 20 20">
                <!-- Heroicon : badge-check -->
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.707a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414L9 13.414l4.707-4.707z" clip-rule="evenodd"/>
              </svg>
            </div>
          </header>

          <p class="text-gray-800 dark:text-gray-200 mb-2">{{ c.text }}</p>

          <div>
            <button
              v-if="auth.isAuthenticated && !c.userUpvoted"
              @click="upvote(c.id)"
              class="text-sm text-green-600 hover:underline focus:outline-none"
            >
              👍 Upvote ({{ c.upvotes }})
            </button>
            <span v-else class="text-sm text-gray-500">
              👍 {{ c.upvotes }}
            </span>
          </div>
        </div>

        <!-- Pagination -->
        <nav class="flex justify-center items-center space-x-2">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-3 py-1 rounded border disabled:opacity-50 focus:outline-none"
          >
            Précédent
          </button>
          <span class="text-sm text-gray-700 dark:text-gray-300">
            Page {{ currentPage }} / {{ totalPages }}
          </span>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 rounded border disabled:opacity-50 focus:outline-none"
          >
            Suivant
          </button>
        </nav>
      </div>
    </transition>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCommentsStore } from '@/stores/comments'

const props = defineProps<{ slug: string }>()

// Stores
const auth     = useAuthStore()
const comments = useCommentsStore()

// État du drawer
const isOpen = ref(false)
function toggle() {
  isOpen.value = !isOpen.value
}

// Récupération des commentaires au montage
onMounted(() => {
  comments.fetchComments(props.slug)
})

// Seuil de validation
const VALIDATION_THRESHOLD = 3

// Commentaires validés
const approvedComments = computed(() =>
  comments.list.filter(c => c.upvotes >= VALIDATION_THRESHOLD)
)

// Compteur total
const totalValidated = computed(() => approvedComments.value.length)

// Pagination
const PER_PAGE    = 5
const currentPage = ref(1)
const totalPages  = computed(() =>
  Math.max(Math.ceil(totalValidated.value / PER_PAGE), 1)
)
const paginatedComments = computed(() =>
  approvedComments.value.slice(
    (currentPage.value - 1) * PER_PAGE,
    currentPage.value * PER_PAGE
  )
)
function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}
function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

// Action d’upvote
async function upvote(commentId: number) {
  await comments.upvote(commentId)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";

.fade-enter-active,
.fade-leave-active {
  transition: opacity .3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.comment-item {
  @apply bg-white dark:bg-gray-800;
}
</style>
