// 📁 test/components/ScrollLayout.spec.ts

import { mount } from '@vue/test-utils'
import ScrollLayout from '@/components/animation/ScrollLayout.vue'
import Hero from '@/components/home/hero.vue'
import Problems from '@/components/home/problems.vue'
import WhoIAm from '@/components/home/whoIAm.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('ScrollLayout.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = mount(ScrollLayout, {
      props: {
        debugVisible: true
      }
    })
  })

  it('se monte correctement', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('rend les sections enfants Hero, Problems et WhoIAm', () => {
    expect(wrapper.findComponent(Hero).exists()).toBe(true)
    expect(wrapper.findComponent(Problems).exists()).toBe(true)
    expect(wrapper.findComponent(WhoIAm).exists()).toBe(true)
  })

  it('affiche la section debug si debugVisible est true', () => {
    const debug = wrapper.find('.debug')
    expect(debug.exists()).toBe(true)
    expect(debug.text()).toContain('SF')
  })

  it('cache la section debug si debugVisible est false', async () => {
    await wrapper.setProps({ debugVisible: false })
    expect(wrapper.find('.debug').exists()).toBe(false)
  })

  it('calcule correctement la section active selon scrollFactor', async () => {
    wrapper.vm.scrollFactor = 0.5
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('hero')

    wrapper.vm.scrollFactor = 1.2
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('problems')

    wrapper.vm.scrollFactor = 1.8
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('whoiam')

    wrapper.vm.scrollFactor = 2.5
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('next')
  })

  it('gère les valeurs extrêmes de scrollFactor', async () => {
    wrapper.vm.scrollFactor = -1
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('hero')

    wrapper.vm.scrollFactor = 99
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.currentSection).toBe('next')
  })

  it('bloque le scroll si scrollUnlocked est false', async () => {
    wrapper.vm.scrollUnlocked = false
    const initialFactor = wrapper.vm.scrollFactor

    // Simuler appel direct
    if (typeof wrapper.vm.onWheel === 'function') {
      wrapper.vm.onWheel({ deltaY: 100 })
    } else {
      const event = new Event('wheel')
      window.dispatchEvent(event)
    }

    expect(wrapper.vm.scrollFactor).toBe(initialFactor)
  })

  it('snapshot global du HTML', () => {
    expect(wrapper.html()).toMatchSnapshot()
  })
})
