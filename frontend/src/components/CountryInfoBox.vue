<script setup>
import { ref } from 'vue';
import Statistics_overview from "@/components/statistics_overview.vue";

const countryName = ref('');
const population = ref('');
const area = ref('');
const capital = ref('');
const isVisible = ref(false);
const isExpanded = ref(false);

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

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
}

// Expose functions so they can be accessed outside the component
defineExpose({
  updateCountryInfo,
  hideCountryInfo,
  toggleExpand
});
</script>

<template>
  <div v-if="isVisible" :class="['info-box', { expanded: isExpanded }]">
    <div class="handle" @click="toggleExpand"></div>
    <div :class="['content', { expanded: isExpanded }]">
      <h2>{{ countryName }}</h2>
      <template v-if="!isExpanded">
        <hr>
        <p>Population: {{ population }}</p>
        <p>Area: {{ area }} km²</p>
        <p>Capital: {{ capital }}</p>
      </template>
      <statistics_overview v-else :countryName="countryName"/>
    </div>
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
  transition: all 0.5s ease;
}

.info-box.expanded {
  width: 97vw;
  height: calc(100% - 70px - 3rem);
  top: 90px;
  right: 0;
  border-radius: 0;
  padding: 20px;
  margin: 0;
}

.handle {
  position: absolute;
  left: -20px;
  top: 50%;
  width: 0;
  height: 0;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
  border-left: 15px solid #03dac6;
  cursor: pointer;
  transform: rotate(180deg);
}

.handle:hover {
  border-left-color: #ffffff;
}

.content {
  display: flex;
  flex-direction: column;
  transition: all 0.5s ease;
}

.content.expanded {
  align-items: flex-start;
  padding-left: 20px;
}

.content:not(.expanded) {
  align-items: center;
  padding-left: 0;
}

.close-btn {
  position: absolute;
  right: 20px;
  top: 20px;
  background: #03dac6;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
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