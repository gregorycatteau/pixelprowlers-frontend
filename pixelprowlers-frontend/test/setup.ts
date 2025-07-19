import { config } from '@vue/test-utils'
import '@testing-library/jest-dom'
import { createCanvas } from 'canvas'
import { vi } from 'vitest'

// 👉 Ici, tu peux stuber des composants globaux si nécessaire
config.global.stubs = {
  NuxtLink: {
    template: '<a><slot /></a>',
  },
  IconComponent: true,
}

// 👉 Si tu as des plugins Vue globaux
// config.global.plugins = [monPluginVue]

// 👉 Configurer des mocks globaux
config.global.mocks = {
  $t: (msg: string) => msg,
}

// 👉 Désactiver warnings sur les transitions
config.global.renderStubDefaultSlot = true

// ✅ 💣 Fix Canvas pour JSDOM
Object.defineProperty(global, 'HTMLCanvasElement', {
  value: class {
    getContext() {
      return createCanvas(200, 200).getContext('2d')
    }
  },
})

// ✅ 💣 Mock complet de GSAP
vi.mock('gsap', async (importOriginal) => {
  const actual = await importOriginal()
  const fakeTimeline = () => ({
    to: vi.fn().mockReturnThis(),
    from: vi.fn().mockReturnThis(),
    add: vi.fn().mockReturnThis(),
    play: vi.fn().mockReturnThis(),
  })

  return {
    ...actual,
    to: vi.fn(),
    from: vi.fn(),
    timeline: vi.fn(fakeTimeline),
    registerPlugin: vi.fn(),
    // ⚡ Voici la clé qui corrige tout
    default: {
      ...actual,
      to: vi.fn(),
      from: vi.fn(),
      timeline: vi.fn(fakeTimeline),
      registerPlugin: vi.fn(),
    },
  }
})

// 💬 Tu peux aussi ajouter des extensions custom à Jest-DOM ici
// ex : expect.extend(...)


