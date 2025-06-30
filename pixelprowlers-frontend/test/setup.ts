import { config } from '@vue/test-utils'
import '@testing-library/jest-dom'

// 👉 Ici, tu peux stuber des composants globaux si nécessaire
config.global.stubs = {
  // Exemple : tu veux ignorer <NuxtLink> dans les snapshots ou tests
  NuxtLink: {
    template: '<a><slot /></a>'
  },
  // Exemple : tu veux ignorer les icônes ou composants tiers lourds
  IconComponent: true
}

// 👉 Si tu as des plugins Vue globaux, tu peux aussi ajouter ici
// config.global.plugins = [monPluginVue, monAutrePlugin]

// 👉 Configurer un wrapper global si tu as besoin de mocks d'injection, etc.
config.global.mocks = {
  $t: (msg: string) => msg,  // Exemple si tu utilises i18n
}

// 👉 Exemple pour désactiver warnings sur les transitions
config.global.renderStubDefaultSlot = true

// 💬 Tu peux aussi ajouter des extensions custom à Jest-DOM si besoin
// ex : expect.extend(...)
;
