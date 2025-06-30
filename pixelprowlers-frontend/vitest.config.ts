import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    include: [
      '**/__tests__/**/*.test.{js,ts}',
      'test/**/*.{test,spec}.{js,ts}',
      'tests/**/*.{test,spec}.{js,ts}'
    ],
    setupFiles: './test/setup.ts',
    coverage: {
      reporter: ['text', 'html'],
      all: true,
      thresholds: {
        lines: 90,
        functions: 90,
        branches: 90,
        statements: 90,
      },
      exclude: [
        'node_modules/',
        'test/setup.ts',
        'dist/',
        '**/*.d.ts'
      ]
    }
  }
});

