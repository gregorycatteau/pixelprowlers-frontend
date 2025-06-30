import { mount } from '@vue/test-utils'
import Breadcrumb from '../../components/navigation/Breadcrumb.vue'

// 🧪 Test du composant Breadcrumb

describe('Breadcrumb.vue', () => {
  // 📝 Vérifie que rien ne s'affiche sans items
  it('ne rend rien si aucune liste n\'est fournie', () => {
    const wrapper = mount(Breadcrumb)
    expect(wrapper.find('nav').exists()).toBe(false)
  })

  // 📝 Vérifie le rendu avec des items
  it('affiche correctement les liens et le texte', () => {
    const items = [
      { label: 'Accueil', href: '/' },
      { label: 'Article' }
    ]
    const wrapper = mount(Breadcrumb, {
      props: { items }
    })

    const li = wrapper.findAll('li')
    expect(li).toHaveLength(2)

    // ✅ Cherche maintenant les <a> (NuxtLink stubbé)
    expect(wrapper.findAll('a')).toHaveLength(1)
    expect(li[1].text()).toContain('Article')
  })
})
