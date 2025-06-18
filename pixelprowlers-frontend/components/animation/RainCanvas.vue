<template>
  <canvas ref="canvas" class="rain-canvas"></canvas>
</template>

<script setup lang="ts">
import { onMounted, ref, onBeforeUnmount } from 'vue'

const canvas = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  const ctx = canvas.value?.getContext('2d')
  if (!ctx || !canvas.value) return

  const fontSize = 24
  const drops: number[] = []
  const columns = Math.floor(window.innerWidth / fontSize)
  for (let i = 0; i < columns; i++) drops[i] = Math.random() * 40

  const resizeCanvas = () => {
    if (canvas.value) {
      canvas.value.width = window.innerWidth
      canvas.value.height = window.innerHeight
    }
  }

  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)

  const draw = () => {
  // Nettoie le canvas SANS le remplir de blanc
  ctx.clearRect(0, 0, canvas.value!.width, canvas.value!.height)

  // Gouttes fines blanches
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
  mix-blend-mode: screen; /* Ou 'lighten' si ton fond est très sombre */
}
</style>
