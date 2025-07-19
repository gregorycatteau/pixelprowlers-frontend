import { mount } from '@vue/test-utils'
import ArticleHeader from '@/components/blog/article/ArticleHeader.vue'
import { describe, it, expect } from 'vitest'

describe('ArticleHeader.vue', () => {
  const defaultProps = {
    title: 'Titre Test',
    date: '2025-07-01',
  }

  it('se monte correctement', () => {
    const wrapper = mount(ArticleHeader, {
      props: defaultProps,
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('rend le contenu de base', () => {
    const wrapper = mount(ArticleHeader, {
      props: defaultProps,
    })
    expect(wrapper.text()).toContain(defaultProps.title)
    expect(wrapper.text()).toContain(defaultProps.date)
  })
})
