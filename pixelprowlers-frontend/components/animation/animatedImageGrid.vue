<template>
  <div class="image-grid" ref="gridRef" :style="{
    gridTemplateColumns: `repeat(${gridSize}, ${tileSize}px)`,
  }" >
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
    />
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

const gridSize = props.gridSize || 10 // 10x10
const tileSize = props.tileSize || 20 // 20px × 20px
const tiles = ref<any[]>([])
const gridRef = ref<HTMLElement | null>(null)

onMounted(async () => {
  const tempTiles = []
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      tempTiles.push({
        bgPosition: `-${x * tileSize}px -${y * tileSize}px`,
        randomX: (Math.random() - 0.5) * 300,
        randomY: (Math.random() - 0.5) * 300,
      })
    }
  }

  tiles.value = tempTiles

  // Attendre que le DOM soit mis à jour
  await nextTick()

  // Lancer l’animation une fois les .tile rendus
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
.image-grid {
  position: relative;
  display: grid;
  grid-template-columns: repeat(10, 20px); /* <= adapter dynamiquement ensuite */
  width: fit-content;
  height: fit-content;
  overflow: hidden;
}
.tile {
  background-size: calc(var(--tile-size) * 10);/* 10 * 20px si 10x10 */
  will-change: transform, opacity;
}

</style>
