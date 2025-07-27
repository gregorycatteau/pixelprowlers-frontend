// stores/comments.ts
import { defineStore } from 'pinia'
import { useRuntimeConfig } from 'nuxt/app'

export interface Comment {
  id:          number
  author:      string
  text:        string
  tags:        string[]
  upvotes:     number
  userUpvoted: boolean
}

export const useCommentsStore = defineStore('comments', {
  state: () => ({
    list: [] as Comment[],
  }),

  actions: {
    async fetchComments(articleSlug: string) {
      const config = useRuntimeConfig()
      const data = await $fetch<Comment[]>(
        // <-- on pointe maintenant vers /feedback/comments/
        `${config.public.apiBaseUrl}/feedback/comments/`,
        {
          method:      'GET',
          credentials: 'include',
          params:      { article: articleSlug },
        }
      )
      this.list = data
    },

    async upvote(commentId: number) {
      const config = useRuntimeConfig()
      const res = await $fetch<{ upvotes: number }>(
        // <-- idem pour l'upvote
        `${config.public.apiBaseUrl}/feedback/comments/${commentId}/upvote/`,
        {
          method:      'POST',
          credentials: 'include',
        }
      )
      const idx = this.list.findIndex(c => c.id === commentId)
      if (idx !== -1) {
        this.list[idx].upvotes     = res.upvotes
        this.list[idx].userUpvoted = true
      }
    },
  },
})
