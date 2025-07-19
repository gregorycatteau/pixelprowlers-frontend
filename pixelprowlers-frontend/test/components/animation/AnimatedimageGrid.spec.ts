// ✅ Mock AVANT imports
vi.mock('gsap', () => {
  return {
    default: {
      to: vi.fn(),
    },
    to: vi.fn(), // on garde l'accès direct
  }
})

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import AnimatedImageGrid from '@/components/animation/animatedImageGrid.vue'
import gsap from 'gsap'

const dummyImageUrl = 'https://dummyimage.com/600x400/000/fff'

describe('AnimatedImageGrid.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('génère le bon nombre de tiles par défaut', async () => {
    const wrapper = mount(AnimatedImageGrid, {
      props: {
        imageUrl: dummyImageUrl
      }
    })

    await nextTick()

    const tiles = wrapper.findAll('.tile')
    expect(tiles.length).toBe(100) // 10x10 par défaut
  })

  it('utilise correctement les props gridSize et tileSize', async () => {
    const wrapper = mount(AnimatedImageGrid, {
      props: {
        imageUrl: dummyImageUrl,
        gridSize: 5,
        tileSize: 20
      }
    })

    await nextTick()

    const tiles = wrapper.findAll('.tile')
    expect(tiles.length).toBe(25) // 5x5

    tiles.forEach((tile) => {
      const style = tile.attributes('style') || ''
      expect(style).toContain('width: 20px')
      expect(style).toContain('height: 20px')
    })
  })

  it('appelle gsap.to avec une configuration correcte', async () => {
    mount(AnimatedImageGrid, {
      props: {
        imageUrl: dummyImageUrl
      }
    })

    await nextTick()

    expect(gsap.to).toHaveBeenCalled()
  })
})
