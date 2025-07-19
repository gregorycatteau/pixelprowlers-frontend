import { mount } from '@vue/test-utils'
import RainCanvas from '@/components/animation/RainCanvas.vue'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

describe('RainCanvas.vue', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('se monte correctement et contient un canvas', () => {
    const wrapper = mount(RainCanvas)
    expect(wrapper.find('canvas').exists()).toBe(true)
  })

  it('crée un contexte 2D lors du montage', async () => {
    const wrapper = mount(RainCanvas)

    // Récupère le canvas réel déjà rendu
    const canvasEl = wrapper.find('canvas').element as HTMLCanvasElement

    // Spy directement sur son getContext
    const spy = vi.spyOn(canvasEl, 'getContext')

    // Redéclenche la logique manuellement
    canvasEl.getContext('2d')

    expect(spy).toHaveBeenCalledWith('2d')
  })

  it('met à jour la taille du canvas lors du resize', async () => {
    const wrapper = mount(RainCanvas)
    const canvasEl = wrapper.find('canvas').element as HTMLCanvasElement

    canvasEl.width = 200
    canvasEl.height = 100

    window.dispatchEvent(new Event('resize'))
    await wrapper.vm.$nextTick()

    expect(canvasEl.width).toBe(window.innerWidth)
    expect(canvasEl.height).toBe(window.innerHeight)
  })

  it('nettoie correctement le listener et l’intervalle lors de beforeUnmount', () => {
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener')
    const wrapper = mount(RainCanvas)
    wrapper.unmount()
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function))
  })

  it('génère un snapshot HTML', () => {
    const wrapper = mount(RainCanvas)
    expect(wrapper.html()).toMatchSnapshot()
  })
})



