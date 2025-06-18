<template>
  <div class="contact-wrapper">
    <form class="form" @submit.prevent="onSubmit">
      <div>
        <label for="lastName" class="label">Nom *</label>
        <input id="lastName" v-model="lastName" type="text" class="input" />
        <p v-if="lastName && !isLastNameValid" class="error">Nom invalide</p>
      </div>
      <div>
        <label for="firstName" class="label">Prénom *</label>
        <input id="firstName" v-model="firstName" type="text" class="input" />
        <p v-if="firstName && !isFirstNameValid" class="error">Prénom invalide</p>
      </div>
      <div>
        <label for="company" class="label">Structure</label>
        <input id="company" v-model="company" type="text" class="input" />
      </div>
      <div>
        <label for="email" class="label">Adresse mail *</label>
        <input id="email" v-model="email" type="email" class="input" />
        <p v-if="email && !isEmailValid" class="error">Email invalide</p>
      </div>
      <div>
        <label for="phone" class="label">Téléphone *</label>
        <input id="phone" v-model="phone" type="tel" class="input" />
        <p v-if="phone && !isPhoneValid" class="error">Téléphone invalide</p>
      </div>
      <div>
        <label for="message" class="label">Message *</label>
        <textarea id="message" v-model="message" class="input h-32"></textarea>
        <p v-if="message && !isMessageValid" class="error">Message requis</p>
      </div>
      <button type="submit" class="btn-primary w-full" :disabled="!isFormValid">Envoyer</button>
    </form>
    <div v-if="success" class="popup">{{ popupMessage }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const config = useRuntimeConfig()

const lastName = ref('')
const firstName = ref('')
const company = ref('')
const email = ref('')
const phone = ref('')
const message = ref('')

const nameRegex = /^[A-Za-zÀ-ÖØ-öø-ÿ\- ]+$/
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
const phoneRegex = /^(0|\+33)[1-9](\d{2}){4}$/

const isLastNameValid = computed(() => nameRegex.test(lastName.value))
const isFirstNameValid = computed(() => nameRegex.test(firstName.value))
const isEmailValid = computed(() => emailRegex.test(email.value))
const isPhoneValid = computed(() => phoneRegex.test(phone.value))
const isMessageValid = computed(() => message.value.trim().length > 0)

const isFormValid = computed(
  () =>
    isLastNameValid.value &&
    isFirstNameValid.value &&
    isEmailValid.value &&
    isPhoneValid.value &&
    isMessageValid.value
)

const success = ref(false)
const popupMessage = ref('')

async function onSubmit() {
  if (!isFormValid.value) return

  await $fetch('/contact/', {
    baseURL: config.public.apiBaseUrl,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      last_name: lastName.value,
      first_name: firstName.value,
      company: company.value,
      email: email.value,
      phone: phone.value,
      message: message.value,
    },
  })

  lastName.value = ''
  firstName.value = ''
  company.value = ''
  email.value = ''
  phone.value = ''
  message.value = ''

  popupMessage.value =
    'Votre message a bien été transmis, nous vous recontacterons dans les plus brefs délais.'
  success.value = true
  setTimeout(() => {
    success.value = false
  }, 4000)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";
.contact-wrapper {
  @apply flex items-center justify-center min-h-screen p-6;
}
.form {
  @apply w-full max-w-lg space-y-4 bg-white p-6 rounded-xl shadow-xl;
}
.label {
  @apply block text-sm font-medium mb-1;
}
.input {
  @apply w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-accent;
}
.error {
  @apply text-red-500 text-sm mt-1;
}
.popup {
  @apply fixed bottom-4 left-1/2 -translate-x-1/2 bg-accent text-white px-4 py-2 rounded-xl shadow-lg;
}
</style>
