import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BlogFilters from '@/components/blog/BlogFilters.vue'

const dummyProps = {
  categories: ['Sécurité', 'Dev', 'Design'],
  keyword: '',
  selectedCategories: [],
  dateOrder: 'asc'
}

describe('BlogFilters.vue', () => {
  it('se monte correctement', () => {
    const wrapper = mount(BlogFilters, {
      props: dummyProps
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('rend le contenu de base', () => {
    const wrapper = mount(BlogFilters, {
      props: dummyProps
    })
    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('gère correctement les props', () => {
    const wrapper = mount(BlogFilters, {
      props: dummyProps
    })
    expect(wrapper.props().categories).toEqual(dummyProps.categories)
    expect(wrapper.props().selectedCategories).toEqual([])
  })
})
