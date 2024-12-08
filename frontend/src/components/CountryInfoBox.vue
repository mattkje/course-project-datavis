<template>
  <div v-if="isVisible" :class="['info-box', { expanded: isExpanded }]">
    <div :class="['handle', { expanded: isExpanded }]" @click="toggleExpand"></div>
    <div :class="['content', { expanded: isExpanded }]">
      <div v-if="isExpanded" class="wholeContainer">
        <div class="panel-1">
          <div class="header">
            <img :src="flagId" alt="flag" class="flag"/>
            <h2>{{ countryName }}</h2>
          </div>

          <div class="top-bar">
            <p>Displaying greenhouse gas data for {{ countryName }}</p>
            <div class="user-interactive-items">
              <div class="future-checkbox">
                <label for="futureCheckbox">Show future predictions:</label>
                <input type="checkbox" id="futureCheckbox" v-model="isFuture">
              </div>
              <div class="dropdown-container">
                <span>Measure by:</span>
                <select class="dropdown" v-model="selectedMeasure">
                  <option :value="`line:million tons,co2/${countryName}`">Total Stats</option>
                  <option :value="`line:kg/dollar of GDP,gdp/${countryName}`">Per GDP</option>
                  <option :value="`line:Per/Capita,per_capita/${countryName}`">Per Capita</option>
                  <option :value="`bar:%,co2_growth_prct/${countryName}`">Growth %</option>
                </select>
              </div>
            </div>
          </div>
          <component
              v-if="selectedMeasureUrl"
              :is="selectedChartComponent"
              :url="selectedMeasureUrl"
              :key="chartKey"/>
          <CountryComparisonChart
              :countries="comparisonCountries.join(',')"
              :comparisonData="selectedCompUrl"
              :start-year="comparisonStartYear"
              :end-year="comparisonEndYear"/>
        </div>
        <div class="spacings"></div>
      </div>

      <template v-if="!isExpanded">
        <div class="header">
          <img :src="flagId" alt="flag" class="flag"/>
          <h2>{{ countryName }}</h2>
        </div>
        <hr>
        <p>Population: {{ population }}</p>
        <p>Area: {{ area }} km²</p>
        <p>Capital: {{ capital }}</p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import StatisticsOverview from "@/components/visualization tools/statistics_overview.vue";
import BarChartComponent from "@/components/visualization tools/bar_chart.vue";
import CountryComparisonChart from "@/components/visualization tools/CountryComparison.vue";

const selectedItems = ref([]);
const isFuture = ref(false);

const countryName = ref('');
const population = ref('');
const area = ref('');
const capital = ref('');
const isVisible = ref(false);
const isExpanded = ref(false);
const selectedMeasure = ref(`line:million tons,co2/${countryName.value}`);
const flagId = ref('');
const comparisonCountries = ref([countryName.value]);
const comparisonStartYear = ref(1990);
const comparisonEndYear = ref(2020);
const selectedCompUrl = ref(`co2/${countryName.value}`);

const handleSelectedItems = (items) => {
  selectedItems.value = items;
};

const selectedChartComponent = computed(() => {
  const [chartType] = selectedMeasure.value.split(':');
  return chartType === 'bar' ? BarChartComponent : StatisticsOverview;
});

const selectedMeasureUrl = computed(() => {
  const [, measureUrl] = selectedMeasure.value.split(':');
  return isFuture.value ? `${measureUrl}/predict` : measureUrl;
});

const chartKey = computed(() => `${selectedMeasure.value}-${isFuture.value}`);

function updateCountryInfo(name, pop, areaSize, cap, id) {
  countryName.value = name;
  population.value = pop;
  area.value = areaSize;
  capital.value = cap;
  isVisible.value = true;
  selectedMeasure.value = `line:million tons,co2/${name}`;
  flagId.value = `public/countryflags/${id}.svg`;
  comparisonCountries.value = [name];
  selectedCompUrl.value = `co2`;
}

function hideCountryInfo() {
  isVisible.value = false;
}

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
    setTimeout(() => {
      window.scrollBy({
        top: window.innerHeight * 1.1,
        behavior: 'smooth'
      });
    }, 300);
}

defineExpose({
  updateCountryInfo,
  hideCountryInfo,
  toggleExpand
});
</script>

<style scoped>
.wholeContainer {
  display: flex;
  flex-direction: column;
  gap: 2%;
  height: 100%;
}

.chart {
  width: 100%;
  height: 100%;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.search-bar {
  flex: 1;
}

.future-checkbox {
  display: flex;
  align-items: center;
  color: black;
}

.user-interactive-items {
  display: flex;
  flex-flow: column;
  align-items: center;
}

.dropdown-container {
  display: flex;
  align-items: center;
  margin-left: auto;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  color: black;
}

.dropdown {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
  background-color: #fff;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.dropdown:focus {
  border-color: #03dac6;
  box-shadow: 0 0 5px rgba(3, 218, 198, 0.5);
}

.info-box {
  position: absolute;
  right: 0;
  top: 50%;
  width: 25%;
  height: 60%;
  padding: 20px;
  background: #1E555F;
  border: 2px dotted #FFA737;
  border-radius: 18px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
  transform: translateY(-50%);
}

h2 {
  color: #232323;
}

.stats {
  margin-top: 10rem;
}

.info-box.expanded {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 180vh;
  right: 0;
  top: 200vh;
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
  width: 100%;
  padding: 20px;
  height: 100%;
}

.content:not(.expanded) {
  align-items: center;
  padding-left: 0;
}

.spacings {
  height: 100px;
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
  color: #ffffff;
  font-family: Inter, sans-serif;
  font-weight: 900;
  font-size: 2rem;
}

p {
  font-family: Inter, sans-serif;
  font-weight: bold;
  margin: 5px 0;
  color: #ffffff;
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

.expandedContainer {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 4%;
  width: 100%;
  height: 100%;
}

.panel-1 {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: start;
}

.future-checkbox {
  margin-right: 5px;
  gap: 5px;
}

span {
  color: #ffffff;
}

label {
  color: #ffffff;
}
</style>