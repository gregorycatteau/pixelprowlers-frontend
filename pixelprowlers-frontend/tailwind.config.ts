import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.{vue,js,ts}',
    './pages/**/*.{vue,js,ts}',
    './app.vue',
    './nuxt.config.{js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#A8BBA2',
        secondary: '#F4F1EB',
        dark: '#2C2C2C',
        accent: '#56C4D2',
        alert: '#F4A261',
        text: '#2C2C2C',
        background: '#F4F1EB',
      },
      fontFamily: {
        sans: ['"Work Sans"', 'sans-serif'],
        display: ['"IBM Plex Mono"', 'monospace'],
      },
      fontSize: {
        heading: ['2rem', '2.5rem'],
        subheading: ['1.5rem', '2rem'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        card: '0 2px 20px rgba(0,0,0,0.05)',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}

export default config
