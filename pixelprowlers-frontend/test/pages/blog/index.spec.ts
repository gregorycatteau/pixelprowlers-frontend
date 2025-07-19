import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import BlogPage from '@/pages/blog/index.vue'

import { getArticles, getCategories } from '@/composables/useArticles'

// On mocke #app automatiquement grâce au fichier __mocks__/#app.ts
vi.mock('#app')

vi.mock('@/composables/useArticles', () => ({
  getArticles: vi.fn(),
  getCategories: vi.fn(),
}))

const fakeArticles = [
  {
    id: 1,
    title: 'Article Test 1',
    created_at: '2023-01-01',
    image: '',
    category: 'Dev',
  },
  {
    id: 2,
    title: 'Article Test 2',
    created_at: '2023-02-01',
    image: '',
    category: 'Design',
  },
]

const fakeCategories = [
  { name: 'Dev', slug: 'dev' },
  { name: 'Design', slug: 'design' },
]