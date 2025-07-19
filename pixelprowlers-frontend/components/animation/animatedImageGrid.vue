<template>
  <div
    class="image-grid"
    ref="gridRef"
    :style="{
      gridTemplateColumns: `repeat(${gridSize}, ${tileSize}px)`,
    }"
  >
    <div
      v-for="(tile, i) in tiles"
      :key="i"
      class="tile"
      :style="{
        width: `${tileSize}px`,
        height: `${tileSize}px`,
        backgroundImage: `url(${imageUrl})`,
        backgroundPosition: tile.bgPosition,
        transform: `translate(${tile.randomX}px, ${tile.randomY}px)`,
        opacity: 0,
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import gsap from 'gsap'

const props = defineProps<{
  imageUrl: string
  gridSize?: number
  tileSize?: number
}>()

const gridSize = props.gridSize ?? 10
const tileSize = props.tileSize ?? 20
const tiles = ref<any[]>([])
const gridRef = ref<HTMLElement | null>(null)

onMounted(async () => {
  const tempTiles = []
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      tempTiles.push({
        bgPosition: `${-x * tileSize}px ${-y * tileSize}px`,
        randomX: (Math.random() - 0.5) * 300,
        randomY: (Math.random() - 0.5) * 300,
      })
    }
  }

  tiles.value = tempTiles

  await nextTick()

  gsap.to('.tile', {
    x: 0,
    y: 0,
    opacity: 1,
    stagger: 0.01,
    duration: 1,
    ease: 'power2.out',
  })
})
</script>

<style scoped>
@reference "@/assets/css/main.css";
.image-grid {
  position: relative;
  display: grid;
  width: fit-content;
  height: fit-content;
  overflow: hidden;
}
.tile {
  background-size: cover;
  will-change: transform, opacity;
}
</style>

