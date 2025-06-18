<template>
  <div class="video-wrapper">
    <client-only>
      <video
        class="video-background"
        src="/hero.mp4"
        autoplay
        muted
        loop
        playsinline
        aria-hidden="true"
      ></video>
    </client-only>
  </div>
</template>

<script setup lang="ts">
// Aucun script nécessaire pour ce composant de fond vidéo
</script>

<style scoped>
@reference "@/assets/css/main.css";
.video-wrapper {
  @apply relative w-full h-screen overflow-hidden;
  
}

.video-background {
  @apply absolute  w-full h-full object-cover z-[-1];
}
</style>
