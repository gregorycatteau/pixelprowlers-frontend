import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NewsletterSignup from '@/components/blog/article/NewsletterSignup.vue'

describe('NewsletterSignup.vue', () => {
  it('rend correctement le formulaire', () => {
    const wrapper = mount(NewsletterSignup)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
    expect(wrapper.find('h2').text()).toContain("Reste connecté·e à l'essentiel")
  })

  it("affiche un message d'erreur si l'email est invalide", async () => {
    const wrapper = mount(NewsletterSignup)
    await wrapper.find('input[type="email"]').setValue('pasunemail')
    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.text()).toContain("Hmm... Ton email semble incorrect 😅")
  })

  it('affiche un message de succès et vide le champ après un email valide', async () => {
    const wrapper = mount(NewsletterSignup)
    const emailInput = wrapper.find('input[type="email"]')

    await emailInput.setValue('test@example.com')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.text()).toContain('Merci pour ton inscription 🙌')
    expect((emailInput.element as HTMLInputElement).value).toBe('')
  })
})
