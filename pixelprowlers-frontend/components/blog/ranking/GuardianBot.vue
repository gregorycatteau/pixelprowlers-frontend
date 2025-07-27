<template>
  <div class="guardian-bot flex flex-col h-full">
    <!-- Barre de titre -->
    <header class="px-4 py-2 bg-green-600 text-white font-bold">
      Gardien du Vivant 💚
    </header>

    <!-- Zone de conversation -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="[
          'chat-bubble',
          msg.sender === 'bot' ? 'bot' : 'user'
        ]"
      >
        {{ msg.text }}
      </div>
    </div>

    <!-- Zone d’interaction -->
    <div class="p-4 border-t bg-gray-50 dark:bg-gray-800">
      <!-- Avant acceptation -->
      <div v-if="!challengeAccepted">
        <p class="mb-3">🗒️ <strong>Défi :</strong> {{ currentChallenge }}</p>
        <div class="flex gap-2">
          <button @click="accept" class="btn-primary flex-1">J’accepte</button>
          <button @click="later" class="btn-secondary flex-1">Plus tard</button>
          <button @click="skip" class="btn-secondary flex-1">Je passe</button>
        </div>
      </div>

      <!-- Saisie du retour -->
      <div v-else-if="!feedbackSent">
        <textarea
          v-model="userResponse"
          rows="3"
          class="w-full p-2 rounded border mb-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          placeholder="Raconte-nous comment ça s’est passé…"
        ></textarea>
        <button
          :disabled="userResponse.trim().length < 10"
          @click="sendFeedback"
          class="btn-primary w-full"
        >
          Envoyer mon retour
        </button>
      </div>

      <!-- Remerciement -->
      <div v-else>
        <p class="text-center text-green-700 dark:text-green-300">
          Merci pour ton retour ! 🙏
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFeedbackStore } from '@/stores/feedback'
import { useRuntimeConfig } from 'nuxt/app'

// Slug de l’article pour l’API
const props = defineProps<{ slug: string }>()

// Stores & config
const feedback = useFeedbackStore()
const config   = useRuntimeConfig()

// Messages de la conversation
const messages = ref<{ sender: 'bot' | 'user'; text: string }[]>([])

// Défis par axe
const challengeMap: Record<'solidarity' | 'resilience' | 'respect', string[]> = {
  solidarity: [
    "Partage une ressource gratuite pour soutenir une asso locale.",
    "Invite une personne de ton réseau à rejoindre notre communauté."
  ],
  resilience: [
    "Décris en 3 lignes un défi que tu as surmonté récemment.",
    "Envoie une astuce pour rebondir après un échec."
  ],
  respect: [
    "Prends en photo une scène de nature que tu admires et explique pourquoi.",
    "Liste 3 actions quotidiennes pour réduire ton empreinte carbone."
  ],
}

// État du défi et du retour
const currentAxis      = ref<'solidarity' | 'resilience' | 'respect'>('solidarity')
const currentChallenge = ref('')
const challengeAccepted = ref(false)
const feedbackSent      = ref(false)
const userResponse      = ref('')

/** Ajoute un message du bot */
function addBotMessage(text: string) {
  messages.value.push({ sender: 'bot', text })
}

/** Ajoute un message de l’utilisateur */
function addUserMessage(text: string) {
  messages.value.push({ sender: 'user', text })
}

/** Sélectionne un défi selon l’axe dominant */
function pickChallenge() {
  const scores = feedback.scores
  // Trouve l’axe avec le score le plus élevé
  const axis = (['solidarity', 'resilience', 'respect'] as const)
    .reduce((a, b) => scores[a] > scores[b] ? a : b)
  currentAxis.value = axis
  // Choisit un défi aléatoire
  const pool = challengeMap[axis]
  currentChallenge.value = pool[Math.floor(Math.random() * pool.length)]
}

// Au montage (ouverture du drawer), initie la conversation
onMounted(() => {
  addBotMessage("Salut ! Je suis ton Gardien du Vivant.")
  addBotMessage("Je te propose un défi basé sur tes notes.")
  pickChallenge()
  addBotMessage(`📝 Voici ton défi : ${currentChallenge.value}`)
})

/** L’utilisateur accepte le défi */
function accept() {
  challengeAccepted.value = true
  addUserMessage(`J’accepte : ${currentChallenge.value}`)
  addBotMessage('Super ! Raconte-moi comment ça s’est passé.')
}

/** L’utilisateur veut reporter */
function later() {
  addUserMessage('Plus tard...')
  addBotMessage('Pas de souci ! Je te proposerai un autre défi plus tard.')
}

/** L’utilisateur ignore cette fois */
function skip() {
  addUserMessage('Je passe.')
  addBotMessage('OK, on passe à autre chose.')
}

/** Envoi du retour de défi au backend */
async function sendFeedback() {
  addUserMessage(userResponse.value)

  // Appel à ton endpoint de stockage des retours
  await $fetch(
    `${config.public.apiBaseUrl}/chat-feedback/`,
    {
      method: 'POST',
      body: {
        article:  props.slug,
        axis:     currentAxis.value,
        challenge: currentChallenge.value,
        response:  userResponse.value,
      },
      credentials: 'include',
    }
  )

  feedbackSent.value = true
  addBotMessage('Merci pour ton retour ! 🙏')
}
</script>

<style scoped>
@reference "@/assets/css/main.css";
.guardian-bot {
  @apply flex flex-col h-full bg-white dark:bg-gray-900;
}

.chat-bubble {
  @apply max-w-[80%] px-4 py-2 rounded-lg;
}
.chat-bubble.bot {
  @apply bg-gray-200 dark:bg-gray-800 self-start;
}
.chat-bubble.user {
  @apply bg-green-500 text-white self-end;
}

/* Boutons */
.btn-primary {
  @apply bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded;
}
.btn-secondary {
  @apply bg-gray-300 hover:bg-gray-400 text-black font-medium py-2 px-4 rounded;
}
</style>
