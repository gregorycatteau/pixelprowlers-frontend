<template>
  <div class="contact-wrapper">
    <h1 ref="titleRef" class="main-title blur-target">Veuillez remplir le formulaire suivant</h1>
    <h2 ref="subtitleRef" class="sub-title blur-target">Afin que nous puissions traiter votre demande</h2>
    <div class="contact-content">
      <div ref="imageRef" class="image-wrapper blur-target">
        <img src="/contact.png" alt="Contact" class="mx-auto" />
      </div>
      <form ref="formRef" class="form" @submit.prevent="onSubmit">
        <div class="form-field blur-target" id="lastNameField">
          <label for="lastName" class="label">Nom *</label>
          <input id="lastName" v-model="lastName" type="text" class="input" />
          <p v-if="lastName && !isLastNameValid" class="error">Nom invalide</p>
        </div>
        <div class="form-field blur-target" id="firstNameField">
          <label for="firstName" class="label">Prénom *</label>
          <input id="firstName" v-model="firstName" type="text" class="input" />
          <p v-if="firstName && !isFirstNameValid" class="error">Prénom invalide</p>
        </div>
        <div class="form-field blur-target" id="companyField">
          <label for="company" class="label">Structure</label>
          <input id="company" v-model="company" type="text" class="input" />
        </div>
        <div class="form-field blur-target" id="emailField">
          <label for="email" class="label">Adresse mail *</label>
          <input id="email" v-model="email" type="email" class="input" />
          <p v-if="email && !isEmailValid" class="error">Email invalide</p>
        </div>
        <div class="form-field blur-target" id="phoneField">
          <label for="phone" class="label">Téléphone *</label>
          <input id="phone" v-model="phone" type="tel" class="input" />
          <p v-if="phone && !isPhoneValid" class="error">Téléphone invalide</p>
        </div>
        <div class="form-field blur-target" id="messageField">
          <label for="message" class="label">Message *</label>
          <textarea id="message" v-model="message" class="input h-32"></textarea>
          <p v-if="message && !isMessageValid" class="error">Message requis</p>
        </div>
        <button ref="submitBtn" type="submit" class="btn-primary w-full" :disabled="!isFormValid">
          Envoyer
        </button>
      </form>
    </div>
    <div v-if="success" ref="popupRef" class="popup">{{ popupMessage }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import gsap from 'gsap'

const config = useRuntimeConfig()

const titleRef = ref<HTMLElement | null>(null)
const subtitleRef = ref<HTMLElement | null>(null)
const imageRef = ref<HTMLElement | null>(null)
const formRef = ref<HTMLFormElement | null>(null)
const submitBtn = ref<HTMLButtonElement | null>(null)
const popupRef = ref<HTMLElement | null>(null)

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

onMounted(() => {
  const fields = formRef.value?.querySelectorAll('.form-field') ?? []

  const tl = gsap.timeline()
  tl.from(titleRef.value, { opacity: 0, y: -30, duration: 0.6 })
    .from(subtitleRef.value, { opacity: 0, y: -30, duration: 0.6 }, '-=0.4')
    .from(imageRef.value, { opacity: 0, scale: 0.9, duration: 0.8 }, '-=0.2')
    .from(fields, { opacity: 0, y: 20, duration: 0.4, stagger: 0.1 }, '-=0.6')

  gsap.to(imageRef.value, {
    y: -10,
    scale: 1.02,
    duration: 3,
    ease: 'power1.inOut',
    repeat: -1,
    yoyo: true,
  })

  const inputs = formRef.value?.querySelectorAll('input, textarea') || []
  inputs.forEach((input) => {
    input.addEventListener('focusin', handleFocus)
    input.addEventListener('focusout', handleBlur)
  })

  if (submitBtn.value) {
    submitBtn.value.addEventListener('mouseenter', () => {
      gsap.to(submitBtn.value, { scale: 1.05, duration: 0.2 })
    })
    submitBtn.value.addEventListener('mouseleave', () => {
      gsap.to(submitBtn.value, { scale: 1, duration: 0.2 })
    })
    submitBtn.value.addEventListener('click', () => {
      gsap.fromTo(submitBtn.value, { scale: 0.95 }, { scale: 1, duration: 0.3, yoyo: true, repeat: 1 })
    })
  }
})

function handleFocus(e: Event) {
  const field = (e.currentTarget as HTMLElement).closest('.form-field') as HTMLElement | null
  if (!field) return
  field.classList.add('input-focused')
  const blurTargets = document.querySelectorAll<HTMLElement>('.blur-target')
  blurTargets.forEach((el) => {
    if (el !== field) {
      gsap.to(el, { filter: 'blur(3px)', duration: 0.3 })
    }
  })
  gsap.to(field, { scale: 1.05, duration: 0.3 })
}

function handleBlur(e: Event) {
  const field = (e.currentTarget as HTMLElement).closest('.form-field') as HTMLElement | null
  if (!field) return
  field.classList.remove('input-focused')
  const blurTargets = document.querySelectorAll<HTMLElement>('.blur-target')
  blurTargets.forEach((el) => {
    gsap.to(el, { filter: 'blur(0px)', duration: 0.3 })
  })
  gsap.to(field, { scale: 1, duration: 0.3 })
}

function shakeField(selector: string) {
  const field = formRef.value?.querySelector(selector)?.closest('.form-field') as HTMLElement | null
  if (!field) return
  gsap.from(field, { x: -5, duration: 0.1, repeat: 3, yoyo: true })
  const error = field.querySelector('.error') as HTMLElement | null
  if (error) {
    gsap.fromTo(error, { opacity: 0 }, { opacity: 1, duration: 0.3 })
    gsap.fromTo(field, { boxShadow: '0 0 0 rgba(0,0,0,0)' }, { boxShadow: '0 0 6px rgba(255,0,0,0.5)', duration: 0.3, yoyo: true, repeat: 1 })
  }
}

watch(success, (v) => {
  if (v && popupRef.value) {
    gsap.fromTo(
      popupRef.value,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, ease: 'bounce.out' }
    )
    gsap.to(popupRef.value, { opacity: 0, duration: 0.5, delay: 3 })
  }
})

async function onSubmit() {
  if (!isFormValid.value) {
    if (!isLastNameValid.value) shakeField('#lastName')
    if (!isFirstNameValid.value) shakeField('#firstName')
    if (!isEmailValid.value) shakeField('#email')
    if (!isPhoneValid.value) shakeField('#phone')
    if (!isMessageValid.value) shakeField('#message')
    return
  }

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
  @apply flex flex-col items-center justify-center min-h-screen p-6 space-y-4;
}
.main-title {
  @apply text-3xl font-bold text-center text-accent;
}
.sub-title {
  @apply text-lg text-center text-accent mb-4;
}
.contact-content {
  @apply flex flex-col md:flex-row items-center w-full max-w-5xl gap-8;
}
.image-wrapper {
  @apply md:w-1/3 w-full flex justify-center;
}
.form {
  @apply md:w-2/3 w-full bg-white p-6 rounded-xl shadow-xl space-y-4 flex flex-col justify-center;
}
.label {
  @apply block text-sm font-medium mb-1;
}
.input {
  @apply w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-accent;
}
.input-focused {
  @apply bg-accent p-5 rounded-md;
}
.error {
  @apply text-red-500 text-sm mt-1;
}
.popup {
  @apply fixed bottom-4 left-1/2 -translate-x-1/2 bg-accent text-white px-4 py-2 rounded-xl shadow-lg;
}
</style>

