// stores/auth.ts
import { defineStore } from 'pinia'
import { useRuntimeConfig } from 'nuxt/app'

/** Représentation d’un utilisateur */
interface User {
  id:     number
  email:  string
  name?:  string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    /** Est-ce que l’utilisateur·rice est authentifié·e ? */
    isAuthenticated: false,

    /** Données du profil */
    user: null as User | null,

    /** Indicateurs de chargement / erreur */
    loading: false,
    error:   null as string | null,
  }),

  actions: {
    /**
     * Envoie un magic link par email
     * @param email Adresse email de l’utilisateur·rice
     */
    async sendMagicLink(email: string) {
      this.loading = true
      this.error   = null
      const config = useRuntimeConfig()

      try {
        await $fetch(
          `${config.public.apiBaseUrl}/auth/magic-link/`,
          {
            method: 'POST',
            body:   { email },
          }
        )
      } catch (e: any) {
        this.error = e?.data?.message || 'Erreur lors de l’envoi du lien magique'
      } finally {
        this.loading = false
      }
    },

    /**
     * Vérifie le token du magic link et authentifie l’utilisateur·rice
     * @param token Token reçu par email
     */
    async handleMagicLink(token: string) {
      this.loading = true
      this.error   = null
      const config = useRuntimeConfig()

      try {
        const user = await $fetch<User>(
          `${config.public.apiBaseUrl}/auth/magic-link/verify/`,
          {
            method:      'POST',
            body:        { token },
            credentials: 'include', // pour le cookie de session
          }
        )
        this.user            = user
        this.isAuthenticated = true
      } catch (e: any) {
        this.error = e?.data?.message || 'Token invalide ou expiré'
      } finally {
        this.loading = false
      }
    },

    /**
     * Démarre le flow GitHub OAuth via redirection
     */
    loginWithGitHub() {
      window.location.href = `${useRuntimeConfig().public.apiBaseUrl}/auth/github/login/`
    },

    /**
     * Gère le callback GitHub (paramètre `code` dans l’URL)
     * @param code Code OAuth renvoyé par GitHub
     */
    async handleGitHubCallback(code: string) {
      this.loading = true
      this.error   = null
      const config = useRuntimeConfig()

      try {
        const user = await $fetch<User>(
          `${config.public.apiBaseUrl}/auth/github/callback/`,
          {
            method:      'POST',
            body:        { code },
            credentials: 'include',
          }
        )
        this.user            = user
        this.isAuthenticated = true
      } catch (e: any) {
        this.error = e?.data?.message || 'Échec de l’authentification GitHub'
      } finally {
        this.loading = false
      }
    },

    /**
     * Récupère le profil de l’utilisateur·rice si déjà authentifié·e
     */
    async fetchUser() {
      this.loading = true
      this.error   = null
      const config = useRuntimeConfig()

      try {
        const user = await $fetch<User>(
          `${config.public.apiBaseUrl}/auth/user/`,
          {
            method:      'GET',
            credentials: 'include',
          }
        )
        this.user            = user
        this.isAuthenticated = true
      } catch {
        this.user            = null
        this.isAuthenticated = false
      } finally {
        this.loading = false
      }
    },

    /**
     * Déconnecte l’utilisateur·rice (optionnel : appeler /logout/ sur le back)
     */
    logout() {
      this.user            = null
      this.isAuthenticated = false
    },
  },
})
