import { vi } from 'vitest'

const gsapMock = {
  to: vi.fn(),
  from: vi.fn(),
  timeline: vi.fn(() => ({
    to: vi.fn().mockReturnThis(),
    from: vi.fn().mockReturnThis(),
    add: vi.fn().mockReturnThis(),
    play: vi.fn().mockReturnThis(),
  })),
  registerPlugin: vi.fn()
}

export default {
  ...gsapMock,
  default: gsapMock // 💡 Important pour les imports par défaut
}
