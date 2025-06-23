<template>
  <form class="filters flex flex-wrap items-center gap-4" @submit.prevent>
    <input
      v-model="localKeyword"
      @input="$emit('update:keyword', localKeyword)"
      type="search"
      placeholder="Rechercher..."
      class="input grow"
    />
    <select
      multiple
      v-model="localCategories"
      @change="emitCategories"
      class="input w-40 h-28"
    >
      <option
        v-for="cat in categories"
        :key="cat"
        :value="cat"
      >
        {{ cat }}
      </option>
    </select>
    <select
      v-model="localDate"
      @change="$emit('update:dateOrder', localDate)"
      class="input"
    >
      <option value="recent">Récents</option>
      <option value="old">Anciens</option>
    </select>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
const props = defineProps<{
  categories: string[]
  keyword: string
  selectedCategories: string[]
  dateOrder: string
}>()
const emit = defineEmits([
  'update:keyword',
  'update:selectedCategories',
  'update:dateOrder',
])
const localKeyword = ref(props.keyword)
const localCategories = ref([...props.selectedCategories])
const localDate = ref(props.dateOrder)
watch(
  () => props.keyword,
  (v) => (localKeyword.value = v)
)
watch(
  () => props.selectedCategories,
  (v) => (localCategories.value = [...v])
)
watch(
  () => props.dateOrder,
  (v) => (localDate.value = v)
)
function emitCategories() {
  emit('update:selectedCategories', localCategories.value)
}
</script>

<style scoped>
@reference "@/assets/css/main.css";
.filters {
  @apply bg-dark/80 text-secondary p-4 rounded-xl justify-center;
}
.input {
  @apply bg-white text-dark dark:bg-dark dark:text-secondary border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-accent;
}
</style>