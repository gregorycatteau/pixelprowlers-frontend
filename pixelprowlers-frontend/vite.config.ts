import { defineConfig } from 'vitest/config'

export default defineConfig({
  // ✅ Config générale des tests
  test: {
    globals: true,                   // → utiliser expect, describe, it sans import
    environment: 'jsdom',           // → simuler le DOM pour tes composants Vue
    setupFiles: './tests/setup.ts', // → fichier de setup global (mocks, stubs, etc.)

    // 💡 Inliner certaines dépendances (utile avec certains modules Nuxt ou VueUse)
    deps: {
      inline: ['@vueuse', '@hypernym/nuxt-gsap']
    },

    // 🛡️ Optionnel : couverture
    coverage: {
      reporter: ['text', 'json', 'html'],
      all: true,
      exclude: [
        'tests/setup.ts',
        '**/*.d.ts',
        'node_modules/',
        '.nuxt/',
        'dist/',
        '**/__mocks__/**'
      ]
    }
  }
})
