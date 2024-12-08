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
            <div id="left-top-bar">
              <p>Displaying greenhouse gas data for {{ countryName }}</p>
            </div>
            <div id="right-top-bar">
            </div>
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
          <div class="graphs">
          <component
              v-if="selectedMeasureUrl"
              :is="selectedChartComponent"
              :url="selectedMeasureUrl"
              :key="chartKey"/>
          <div class="comparison">
            <CountryComparisonChart
                :countries="comparisonCountries.join(',')"
                :comparisonData="selectedComparisonUrl.split(',')[1]"
                :start-year="comparisonStartYear"
                :end-year="comparisonEndYear"/>
            <div class="innerTextContainer">
              <div class="country-search">
                <input type="text" v-model="input" placeholder="Search for a country" @click="showDropdown = true"
                       @focus="showDropdown = true" @blur="hideDropdownWithDelay" @keydown.enter="selectFirstOption">
                <div class="country-list" v-if="showDropdown && filteredCountries.length" @mouseenter="preventHideDropdown"
                     @mouseleave="allowHideDropdown">
                  <div class="country-items">
                    <div class="country-item" v-for="country in filteredCountries" :key="country"
                         @click="addCountryToFilter(country)">
                      <p>{{ country }}</p>
                    </div>
                  </div>
                  <div class="item error" v-if="input && !filteredCountries.length">
                    <p>No results found!</p>
                  </div>
                </div>
                <div class="selected-filters">
                  <h3>Selected Countries</h3>
                  <ul>
                    <p id="comparison-error" v-if="comparisonCountries.length === 0">Search for a country to view their
                      data!</p>
                    <li v-for="country in comparisonCountries" :key="country">
                      {{ country }}
                      <button @click="removeCountryFromFilter(country)">x</button>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="year-slider">
                <Slider v-model="sliderValue" :min="2000" :max="2022" :step="1" range/>
              </div>
              <div class="button-group">
                <div v-for="(button, index) in barchartCompButtons" :key="index" class="button-container">
                  <input type="radio" :id="button.label" :value="button.url" v-model="selectedComparisonUrl"
                         @change="updateCompData(button.url)">
                  <label :for="button.label">{{ button.name }}</label>
                </div>
              </div>
            </div>
          </div>
          </div>
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
import {computed, onMounted, ref, watch} from 'vue';
import StatisticsOverview from "@/components/visualization tools/statistics_overview.vue";
import BarChartComponent from "@/components/visualization tools/bar_chart.vue";
import CountryComparisonChart from "@/components/visualization tools/CountryComparison.vue";
import Slider from "@vueform/slider";
import RingModule from "@/components/visualization tools/RingModule.vue";

const selectedItems = ref([]);
const isFuture = ref(false);

const barchartCompButtons = [
  {label: "Total Comparison", url: "Total Co2 emissions,cumulative_co2", selected: true, name: "Total"},
  {
    label: "Land Usage Comparison",
    url: "Total Co2 emissions including land use,cumulative_co2_including_luc",
    selected: false,
    name: "Land Usage"
  },
  {label: "Coal Comparison", url: "Total Coal Emissions,cumulative_coal_co2", selected: false, name: "Coal"},
  {label: "Oil Comparison", url: "Total Oil Emissions,cumulative_oil_co2", selected: false, name: "Oil"},
  {label: "Flaring Comparison", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Comparison", url: "Total Gas Emissions,cumulative_gas_co2", selected: false, name: "Gas"},
  {label: "Cement Comparison", url: "Total Cement Emissions,cumulative_cement_co2", selected: false, name: "Cement"}
];

const selectedComparisonUrl = ref("Total Co2 emissions,cumulative_co2");
const countryName = ref('');
const population = ref('');
const area = ref('');
const capital = ref('');
const isVisible = ref(false);
const isExpanded = ref(false);
const selectedMeasure = ref(`line:million tons,co2/${countryName.value}`);
const flagId = ref('');
const comparisonCountries = ref([countryName.value]);
const comparisonStartYear = ref(2000);
const comparisonEndYear = ref(2022);
const sliderValue = ref([2000, 2022]);
const input = ref('');
const fetchError = ref(null);
const showDropdown = ref(false);
const countries = ref([]);
let preventHide = false;

const filteredCountries = computed(() => {
  if (!input.value) return [];
  return countries.value.filter(country => country.toLowerCase().startsWith(input.value.toLowerCase()));
})

onMounted(async () => {
  countries.value = await fetchData('http://127.0.0.1:5000/countries'); // Assign fetched data
});

watch(selectedComparisonUrl, (newValue) => {
  if (!newValue.includes(',')) {
    selectedComparisonUrl.value = "Total Co2 emissions,cumulative_co2";
  }
});

async function fetchData(url) {
  try {
    fetchError.value = null; // Reset error
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Error: ${response.statusText}`);
    return await response.json();
  } catch (error) {
    fetchError.value = error.message;
    console.error("Failed to fetch data:", error);
    return [];
  }
}

watch(sliderValue, (newValue) => {
  comparisonStartYear.value = newValue[0];
  comparisonEndYear.value = newValue[1];

  sliderChange();
}, {immediate: true});

console.log(selectedComparisonUrl.value);

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

function sliderChange() {
  [comparisonStartYear.value, comparisonEndYear.value] = sliderValue.value;
}

function hideDropdownWithDelay() {
  if (!preventHide) {
    setTimeout(() => {
      showDropdown.value = false;
    }, 200);
  }
}

function selectFirstOption() {
  if (filteredCountries.value.length > 0) {
    addCountryToFilter(filteredCountries.value[0]);
  }
  showDropdown.value = true;
}

function preventHideDropdown() {
  preventHide = true;
}

function allowHideDropdown() {
  preventHide = false;
}

function addCountryToFilter(country) {
  if (!comparisonCountries.value.includes(country)) {
    comparisonCountries.value.push(country);
  }
  input.value = '';
  showDropdown.value = false;
}

function removeCountryFromFilter(country) {
  // Find the index of the country in the array
  const index = comparisonCountries.value.indexOf(country);

  // If the country exists in the array, remove it
  if (index !== -1) {
    comparisonCountries.value.splice(index, 1);
  }
}

function updateCompData(url) {
  selectedComparisonUrl.value = url;
  barchartCompButtons.forEach(button => button.selected = (button.url === url));
}

function updateCountryInfo(name, pop, areaSize, cap, id) {
  countryName.value = name;
  population.value = pop;
  area.value = areaSize;
  capital.value = cap;
  isVisible.value = true;
  selectedMeasure.value = `line:million tons,co2/${name}`;
  flagId.value = `public/countryflags/${id}.svg`;
  comparisonCountries.value = [name];
  selectedComparisonUrl.value = `co2`;
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
  width: 100%;
}

.search-bar {
  flex: 1;
}

.button-group {
  margin-top: 10px;
  justify-self: center;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.future-checkbox {
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.country-search {
  position: relative;
  width: 350px;
  margin: 0 auto;
}

.country-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.country-item:hover {
  background-color: #366e7a;
}

.country-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.country-item:hover {
  background-color: #366e7a;
}

.item.error {
  padding: 10px 15px;
  color: #FFA737;
  text-align: center;
}

.country-list {
  position: absolute;
  left: 0;
  width: 100%;
  background: #366e7a;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
}

input {
  display: block;
  width: 100%;
  padding: 10px 15px;
  background: white;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.year-slider {
  margin-top: 50px;
}

.selected-filters {
  margin-top: 20px;
  color: white;
}

.selected-filters h3 {
  margin-bottom: 10px;
  font-size: 16px;
}

.selected-filters ul {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Space between items */
  height: 150px;
  padding: 0;
  margin: 0;
  list-style: none;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #4e90a4 #1E555F;
}

.selected-filters li {
  background: #366e7a;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  font-family: "Corbel Light", serif;
  font-weight: 700;
}

.selected-filters li button {
  margin-top: 5px;
  background: #146168;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
}

.selected-filters li button:hover {
  background: firebrick;
}

#comparison-error {
  text-align: center;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + label {
  background-color: #4e90a4;
  width: 140px;
  height: 50px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  box-sizing: border-box;
  transition: background-color 0.3s ease;
  font-weight: bold;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

input[type="radio"]:checked + label {
  background-color: #366e7a;
}

input[type="radio"] + label:hover {
  background-color: #366e7a;
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
  height: auto;
  right: 0;
  top: 185vh;
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

.comparison {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: auto; /* Allow height to adjust dynamically */
  gap: 20px; /* Add some spacing between items */
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

h3 {
  justify-self: left;
  font-size: 1.6rem;
  font-weight: 900;
  color: #FFA737;
  margin: 0;
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

.graphs {
  width: 100%;
  height: 100%;
  gap: 100px;
}

span {
  color: #ffffff;
}

label {
  color: #ffffff;
}

.innerTextContainer {
  color: white;
  border-radius: 18px;
  padding: 40px;
  position: relative;
  font-size: 1.4rem;
  font-weight: 400;
  margin: 60px 0px 60px 0px;
  border: 2px dotted #FFA737;
  max-width: 30%;
  width: 100%;
  box-sizing: border-box;
  display: grid;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  align-content: center;
}

@media screen and (max-width: 1400px) {
  .button-group {
    margin-top: 0;
  }

  .innerTextContainer {
    max-width: 100%;
    width: 95%;
    margin: 80px auto 0 auto;
    gap: 20px;
  }

  .comparison {
    flex-direction: column-reverse;
    padding: 0 50px;
    gap: 0;
  }

  .info-box.expanded {
    top: 220vh;
  }
}
</style>