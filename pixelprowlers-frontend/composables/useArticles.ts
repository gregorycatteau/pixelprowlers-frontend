import { useRuntimeConfig } from '#imports'

export interface Article {
  id: number
  slug: string
  title: string
  summary: string
  content: string
  category: Category
  created_at: string
  image?: string | null
}

export interface Category {
  id: number
  name: string
  slug: string
}

export function getArticles() {
  const config = useRuntimeConfig()
  const url = `${config.public.apiBaseUrl}/blog/articles/`
  return $fetch<Article[]>(url)
}

export function getArticle(slug: string) {
  const config = useRuntimeConfig()
  const url = `${config.public.apiBaseUrl}/blog/articles/${slug}/`
  return $fetch<Article>(url)
}

export function getCategories() {
  const config = useRuntimeConfig()
  const url = `${config.public.apiBaseUrl}/blog/categories/`
  return $fetch<Category[]>(url)
}