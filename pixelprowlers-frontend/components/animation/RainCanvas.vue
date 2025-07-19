<template>
  <canvas ref="canvas" class="rain-canvas"></canvas>
</template>

<script setup lang="ts">
// Import des hooks Vue
import { onMounted, ref, onBeforeUnmount } from 'vue'

/**
 * Référence au canvas
 */
const canvas = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  const ctx = canvas.value?.getContext('2d')
  if (!ctx || !canvas.value) return

  const fontSize = 24
  const drops: number[] = []

  // Nombre de colonnes basé sur la largeur
  const columns = Math.floor(window.innerWidth / fontSize)
  for (let i = 0; i < columns; i++) drops[i] = Math.random() * 40

  /**
   * Fonction pour adapter la taille du canvas lors du resize
   */
  const resizeCanvas = () => {
    if (canvas.value) {
      canvas.value.width = window.innerWidth
      canvas.value.height = window.innerHeight
    }
  }

  // Initialisation de la taille
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)

  /**
   * Fonction de dessin des gouttes
   */
  const draw = () => {
    // Nettoie sans remplir
    ctx.clearRect(0, 0, canvas.value!.width, canvas.value!.height)

    // Paramètres visuels des gouttes
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)'
    ctx.shadowColor = 'rgba(255, 255, 255, 0.2)'
    ctx.shadowBlur = 4
    ctx.font = `${fontSize}px monospace`

    for (let i = 0; i < drops.length; i++) {
      const text = '|'
      const x = i * fontSize
      const y = drops[i] * fontSize

      ctx.fillText(text, x, y)

      if (y > canvas.value!.height || Math.random() > 0.95) {
        drops[i] = 0
      }
      drops[i] += 1
    }
  }

  // Interval de rafraîchissement
  const interval = setInterval(draw, 33)

  onBeforeUnmount(() => {
    clearInterval(interval)
    window.removeEventListener('resize', resizeCanvas)
  })
})
</script>

<style scoped>
.rain-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
  mix-blend-mode: screen; /* Ou 'lighten' si ton fond est sombre */
}
</style>
