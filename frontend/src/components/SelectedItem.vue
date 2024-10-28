<script setup>
import { ref, computed } from 'vue';

// Define component props
const props = defineProps({
  item: String,
  onRemove: Function
});

// Define reactive properties for the selected years
const selectedYear1 = ref(null);
const selectedYear2 = ref(null);

// Create an array of years from 1900 to 2023
const years = Array.from({ length: 2023 - 1900 + 1 }, (_, i) => 1900 + i);

// Compute the available years for the second select
const availableYearsForSecondSelect = computed(() => {
  return years.filter(year => year > selectedYear1.value);
});
</script>

<template>
  <div class="selected-item">
    <template v-if="item === 'Year'">
      <span>From:</span>
      <select v-model="selectedYear1">
        <option disabled value="">Select Year</option>
        <option v-for="year in years" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
      <span>To:</span>
      <select v-model="selectedYear2" :disabled="!selectedYear1">
        <option disabled value="">Select Year</option>
        <option v-for="year in availableYearsForSecondSelect" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </template>
    <template v-else>
      {{ item }}
    </template>
    <button @click="onRemove(item)">x</button>
  </div>
</template>

<style scoped>
.selected-item {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  margin: 5px;
  background-color: #03DAC6;
  color: white;
  border-radius: 5px;
  gap: 5px;
}

button {
  margin-left: 10px;
  background: none;
  border: none;
  cursor: pointer;
  color: red;
}

select {
  font-size: 14px;
  background: none;
  border: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
  height: 24px;
  color: white;
}

select:focus {
  outline: none;
}

select option {
  background: white;
  color: black;
}
</style>