<template>
  <transition name="menu-fade">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex bg-black/90 backdrop-blur-md"
    >
      <!-- Visuel à gauche -->
      <div class="w-1/3 p-4">
        <div class="h-full w-full overflow-hidden rounded-lg">
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
          @click="$emit('close')"
          class="self-end text-4xl mb-12 hover:text-accent transition"
          aria-label="Fermer le menu"
        >
          &times;
        </button>

        <nav class="flex flex-col space-y-6">
  <transition-group name="menu-item" tag="ul" class="flex flex-col space-y-6">
    <li v-for="(item, idx) in menu" :key="item.to">
      <NuxtLink
        :to="item.to"
        class="text-4xl font-light hover:font-semibold transition-all duration-300"
        @click="$emit('close')"
      >
        {{ item.label }}
      </NuxtLink>
    </li>
  </transition-group>
</nav>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
const props = defineProps<{
  open: boolean
}>()

const menu = [
  { to: '/', label: 'Accueil' },
  { to: '/services', label: 'Services' },
  { to: '/projets', label: 'Projets' },
  { to: '/contact', label: 'Contact' }
]
</script>

