<script setup>
import {ref} from 'vue';

const countryName = ref('');
const population = ref('');
const area = ref('');
const capital = ref('');
const isVisible = ref(false);

function updateCountryInfo(name, pop, areaSize, cap) {
  countryName.value = name;
  population.value = pop;
  area.value = areaSize;
  capital.value = cap;
  isVisible.value = true;
  console.log("updated");
}

function hideCountryInfo() {
  isVisible.value = false;
}

// Expose functions so they can be accessed outside the component
defineExpose({
  updateCountryInfo,
  hideCountryInfo
});
</script>

<template>
  <div v-if="isVisible" class="info-box">
    <h2>{{ countryName }}</h2>
    <hr>
    <p>Population: {{ population }}</p>
    <p>Area: {{ area }} km²</p>
    <p>Capital: {{ capital }}</p>
  </div>
</template>

<style scoped>
.info-box {
  position: absolute;
  right: 0;
  top: 70px;
  width: 25vw;
  height: calc(100% - 70px - 3rem);
  padding: 20px;
  margin: 1.5rem;
  background: rgba(30, 30, 30, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  color: #f2f2f2;
  font-family: Inter, sans-serif;
  font-weight: 900;
  font-size: 2rem;
}

p {
  font-family: Inter, sans-serif;
  font-weight: bold;
  margin: 5px 0;
  color: #f2f2f2;
}
</style>
