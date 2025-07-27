// stores/drawer.ts
import { defineStore } from 'pinia'

export const useDrawerStore = defineStore('drawer', {
  state: () => ({
    /** État du drawer : ouvert ou fermé */
    isOpen: false,
  }),

  actions: {
    /** Ouvre le drawer */
    open() {
      this.isOpen = true
    },
    /** Ferme le drawer */
    close() {
      this.isOpen = false
    },
    /** Bascule l’état du drawer */
    toggle() {
      this.isOpen = !this.isOpen
    },
  },
})
