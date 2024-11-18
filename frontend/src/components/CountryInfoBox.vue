<script setup>
import { ref } from 'vue';
import Statistics_overview from "@/components/statistics_overview.vue";
import SearchBar from "@/components/SearchBar.vue";

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

defineExpose({
  updateCountryInfo,
  hideCountryInfo,
  toggleExpand
});
</script>


<template>
  <div v-if="isVisible" :class="['info-box', { expanded: isExpanded }]">
    <div :class="['handle', { expanded: isExpanded }]" @click="toggleExpand"></div>
    <div :class="['content', { expanded: isExpanded }]">
      <h2>{{ countryName }}</h2>
      <div v-if="isExpanded" class="top-bar">
        <search-bar class="search-bar" />
        <div class="dropdown-container">
          <span>Measure by:</span>
          <select class="dropdown">
            <option value="co2">CO2</option>
            <option value="co2_including_luc">CO2 w/Land Use Change</option>
            <option value="coal_co2">Coal</option>
            <option value="consumption_co2">Consumption</option>
            <option value="cement_co2">Cement</option>
            <option value="flaring_co2">Flaring</option>
            <option value="gas_co2">Gas</option>
            <option value="land_use_change_co2">Land Use Change</option>
            <option value="oil_co2">Oil</option>
            <option value="other_industry_co2">Other Industry</option>
            <option value="temperature_change_from_co2">Temperature Change from CO2</option>
            <option value="trade_co2">Trade</option>
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
        <statistics_overview class="stats"  :url="`co2/${countryName}`"/>
      </div>
    </div>
  </div>
</template>

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

/* Existing styles */
.info-box {
  position: absolute;
  right: 0;
  top: 70px;
  width: 25%;
  height: calc(100% - 70px);
  padding: 20px;
  background: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

h2 {
  color: #232323;
}

.stats {
  margin-top: 8rem;
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
</style>