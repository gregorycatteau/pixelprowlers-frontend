// stores/feedback.ts
import { defineStore } from 'pinia'
import { useRuntimeConfig } from 'nuxt/app'

interface FeedbackPayload {
  article:  string
  impact:   number
  clarity:  number
  utility:  number
  comment?: string
}
interface Scores {
  solidarity: number
  resilience: number
  respect:    number
}

export const useFeedbackStore = defineStore('feedback', {
  state: () => ({
    ratings: {
      impact:  0,
      clarity: 0,
      utility: 0,
    } as Record<'impact'|'clarity'|'utility', number>,

    hasRated: false,

    scores: {
      solidarity: 0,
      resilience: 0,
      respect:    0,
    } as Scores,
  }),

  actions: {
    setRating(key: keyof typeof this.ratings, value: number) {
      this.ratings[key] = value
    },

    async submitFeedback(articleSlug: string, comment = '') {
      const config = useRuntimeConfig()
      const payload: FeedbackPayload = {
        article:  articleSlug,
        impact:   this.ratings.impact,
        clarity:  this.ratings.clarity,
        utility:  this.ratings.utility,
        comment:  comment || undefined,
      }

      // ← On appelle /api/feedback/feedback/ et non /api/feedback/
      const res = await $fetch<Scores>(
        `${config.public.apiBaseUrl}/feedback/`,
        {
          method:      'POST',
          credentials: 'include',
          body:        payload,
        }
      )

      this.hasRated = true
      this.scores   = {
        solidarity: res.solidarity,
        resilience: res.resilience,
        respect:    res.respect,
      }

      return res
    },
  },
})
