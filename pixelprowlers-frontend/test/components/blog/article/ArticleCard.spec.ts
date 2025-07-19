import { mount } from '@vue/test-utils'
import ArticleCard from '@/components/blog/ArticleCard.vue'
import { describe, it, expect } from 'vitest'

const sampleArticle = {
  slug: 'test-article',
  title: 'Titre test',
  summary: 'Résumé test',
  image: null,
  category: { name: 'Catégorie test', slug: 'cat-test' },
  created_at: '2023-01-01',
}

const stubs = {
  NuxtLink: {
    template: '<a :href="to"><slot /></a>',
    props: ['to'],
  },
}

describe('ArticleCard.vue', () => {
  it("affiche correctement les informations de l’article", () => {
    const wrapper = mount(ArticleCard, {
      props: { article: sampleArticle },
      global: { stubs },
    })

    expect(wrapper.text()).toContain(sampleArticle.title)
    expect(wrapper.text()).toContain(sampleArticle.summary)
    expect(wrapper.text()).toContain(sampleArticle.category.name)

    const link = wrapper.find('a')
    expect(link.exists()).toBe(true)
    expect(link.attributes('href')).toBe(`/blog/${sampleArticle.slug}`)
  })

  it('affiche un placeholder si aucune image n’est fournie', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: { ...sampleArticle, image: null } },
      global: { stubs },
    })

    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe('https://placehold.co/600x400')
  })
})

