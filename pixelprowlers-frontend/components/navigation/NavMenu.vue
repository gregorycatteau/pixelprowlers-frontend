<template>
  <div
    v-show="isVisible"
    ref="menuContainer"
    class="fixed inset-0 z-50 flex bg-black/90 backdrop-blur-md"
  >
      <!-- Visuel à gauche -->
      <div class="w-1/3 p-4">
        <div ref="imageContainer" class="h-full w-full overflow-hidden rounded-lg">
          <img
            src="/menu-photo.png"
            alt="Illustration menu"
            class="h-full w-full object-cover"
          />
        </div>
      </div>

      <!-- Navigation à droite -->
      <div class="w-2/3 flex flex-col justify-center px-12 py-16 text-white">
        <button
          ref="closeBtn"
          @mouseenter="hoverClose"
          @mouseleave="leaveClose"
          @click="closeMenu"
          class="self-end text-4xl mb-12 hover:text-accent transition"
          aria-label="Fermer le menu"
        >
          &times;
        </button>

        <nav class="flex flex-col space-y-6">
          <ul class="flex flex-col space-y-6">
            <li v-for="(item, idx) in menu" :key="item.to">
              <NuxtLink
                :to="item.to"
                ref="setNavItem"
                @click="closeMenu"
                @mouseenter="hoverLink(idx)"
                @mouseleave="leaveLink(idx)"
                class="relative text-4xl font-light hover:font-semibold transition-all duration-300"
              >
                <span>{{ item.label }}</span>
                <span class="underline absolute bottom-0 left-0 h-px w-full bg-current origin-left scale-x-0" />
              </NuxtLink>
            </li>
          </ul>
        </nav>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import gsap from 'gsap'

const emit = defineEmits(['close'])

const props = defineProps<{
  open: boolean
}>()

const menu = [
  { to: '/', label: 'Accueil' },
  { to: '/services', label: 'Services' },
  { to: '/projets', label: 'Projets' },
  { to: '/contact', label: 'Contact' },
  { to: '/a-propos', label: 'À propos' },
  { to: '/blog', label: 'Blog' }
]

const menuContainer = ref<HTMLElement | null>(null)
const imageContainer = ref<HTMLElement | null>(null)
const closeBtn = ref<HTMLElement | null>(null)
const navItems = ref<HTMLElement[]>([])

const isVisible = ref(false)
const prefersReducedMotion = ref(false)

let menuTl: gsap.core.Timeline | null = null
let idleAnim: gsap.core.Tween | null = null

const setNavItem = (el: HTMLElement | null) => {
  if (el) navItems.value.push(el)
}

onMounted(() => {
  // ✅ Vérifie la préférence utilisateur seulement côté client
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  isVisible.value = props.open

  if (prefersReducedMotion.value) return

  menuTl = gsap.timeline({ paused: true })
    .fromTo(
      menuContainer.value,
      { x: '-100vw', opacity: 0 },
      { x: 0, opacity: 1, duration: 1, ease: 'power2.out' }
    )
    .fromTo(
      imageContainer.value,
      { y: 50, opacity: 0, scale: 0.95 },
      { y: 0, opacity: 1, scale: 1, duration: 1, ease: 'power2.out' },
      '-=0.8'
    )
    .fromTo(
      navItems.value,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, stagger: 0.1, duration: 0.6, ease: 'power2.out' },
      '-=0.8'
    )
})

watch(
  () => props.open,
  async (val) => {
    if (prefersReducedMotion.value) {
      isVisible.value = val
      return
    }

    if (val) {
      isVisible.value = true
      await nextTick()
      menuTl?.play(0)
      idleAnim = gsap.to(imageContainer.value, {
        y: 2,
        duration: 4,
        yoyo: true,
        repeat: -1,
        ease: 'sine.inOut'
      })
    } else {
      idleAnim?.kill()
      menuTl?.reverse()
      menuTl?.eventCallback('onReverseComplete', () => {
        isVisible.value = false
      })
    }
  },
  { immediate: true }
)

const hoverLink = (idx: number) => {
  if (prefersReducedMotion.value) return
  const link = navItems.value[idx]
  const underline = link.querySelector('.underline') as HTMLElement | null
  gsap.to(link, { letterSpacing: '0.05em', duration: 0.2 })
  if (underline) {
    gsap.to(underline, { scaleX: 1, transformOrigin: 'left', duration: 0.3 })
  }
}

const leaveLink = (idx: number) => {
  if (prefersReducedMotion.value) return
  const link = navItems.value[idx]
  const underline = link.querySelector('.underline') as HTMLElement | null
  gsap.to(link, { letterSpacing: '0em', duration: 0.2 })
  if (underline) {
    gsap.to(underline, { scaleX: 0, transformOrigin: 'left', duration: 0.3 })
  }
}

const hoverClose = () => {
  if (prefersReducedMotion.value) return
  gsap.to(closeBtn.value, {
    rotation: 20,
    yoyo: true,
    repeat: 1,
    duration: 0.3
  })
}

const leaveClose = () => {
  if (prefersReducedMotion.value) return
  gsap.to(closeBtn.value, { rotation: 0, duration: 0.3 })
}

const closeMenu = () => {
  if (prefersReducedMotion.value) {
    isVisible.value = false
    emit('close')
    return
  }

  idleAnim?.kill()
  menuTl?.reverse()
  menuTl?.eventCallback('onReverseComplete', () => {
    isVisible.value = false
    emit('close')
  })
}
</script>


