<template>
  <div v-if="isVisible" :class="['info-box', { expanded: isExpanded }]">
    <div :class="['handle', { expanded: isExpanded }]" @click="toggleExpand"></div>
    <div :class="['content', { expanded: isExpanded }]">
      <div class="header">
        <img :src="flagId" alt="flag" class="flag"/>
        <h2>{{ countryName }}</h2>
      </div>
      <div v-if="isExpanded" class="top-bar">
        <search-bar/>
        <div class="dropdown-container">
          <span>Measure by:</span>
          <select class="dropdown" v-model="selectedMeasure">
            <option :value="`line:co2/${countryName}`">Total Stats</option>
            <option :value="`line:gdp/${countryName}`">Per GDP</option>
            <option :value="`line:coal_co2`">Per Capita</option>
            <option :value="`bar:co2_growth_prct/${countryName}`">Growth %</option>
          </select>
        </div>
      </div>
      <template v-if="!isExpanded">
        <hr>
        <p>Population: {{ population }}</p>
        <p>Area: {{ area }} km²</p>
        <p>Capital: {{ capital }}</p>
      </template>
      <div class="chart" v-else>
        <component :is="selectedChartComponent" class="stats" :url="selectedMeasureUrl" :key="selectedMeasure"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import StatisticsOverview from "@/components/statistics_overview.vue";
import BarChartComponent from "@/components/bar_chart.vue";
import SearchBar from "@/components/SearchBar.vue";

const countryName = ref('');
const population = ref('');
const area = ref('');
const capital = ref('');
const isVisible = ref(false);
const isExpanded = ref(false);
const selectedMeasure = ref(`line:co2/${countryName.value}`);
const flagId = ref('');

const selectedChartComponent = computed(() => {
  const [chartType] = selectedMeasure.value.split(':');
  return chartType === 'bar' ? BarChartComponent : StatisticsOverview;
});

const selectedMeasureUrl = computed(() => {
  const [, measureUrl] = selectedMeasure.value.split(':');
  return measureUrl;
});

function updateCountryInfo(name, pop, areaSize, cap, id) {
  countryName.value = name;
  population.value = pop;
  area.value = areaSize;
  capital.value = cap;
  isVisible.value = true;
  selectedMeasure.value = `line:co2/${name}`;
  flagId.value = `public/countryflags/${id}.svg`;
  console.log("Country info updated:", name, pop, areaSize, cap, id);
}

function hideCountryInfo() {
  isVisible.value = false;
}

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
}

defineExpose({
  updateCountryInfo,
  hideCountryInfo,
  toggleExpand
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
}

.top-bar {
  display: flex;
  justify-content: start;
  align-items: center;
  width: 100%;
  margin-bottom: 14rem;
}

.search-bar {
  flex: 1;
}

.dropdown-container {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.dropdown {
  margin-left: 10px;
}

.info-box {
  position: absolute;
  right: 0;
  top: 70px;
  width: 25%;
  height: calc(100% - 70px);
  padding: 20px;
  background: linear-gradient(
      135deg,
      var(--color-background) 15%,
      var(--color-background) 15%,
      var(--color-background) 15%,
      var(--color-background) 85%,
      var(--vt-c-secondary) 85%,
      var(--vt-c-secondary) 100%
  );
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

h2 {
  color: #232323;
}

.stats {
  margin-top: 4rem;
}

.info-box.expanded {
  width: 97vw;
  height: calc(100% - 70px);
  right: 0;
  top: 70px;
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
  animation: pulse 2s infinite;
}

.handle::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: 30px;
  height: 30px;
  background: rgba(3, 218, 198, 0.5);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ripple 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: rotate(180deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.1);
  }
  100% {
    transform: rotate(180deg) scale(1);
  }
}

@keyframes ripple {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
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
  width: 65vw;
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
  color: #424242;
  font-family: Inter, sans-serif;
  font-weight: 900;
  font-size: 2rem;
}

p {
  font-family: Inter, sans-serif;
  font-weight: bold;
  margin: 5px 0;
  color: #525252;
}

.header {
  display: flex;
  align-items: center;
}

.flag {
  width: 60px;
  max-height: 100%;
  margin-right: 10px;
}
</style>