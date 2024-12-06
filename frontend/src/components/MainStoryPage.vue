<script setup>
import '@vueform/slider/themes/default.css';
import ContinentMap from './visualization tools/ContinentMap.vue';
import ToolBar from "@/components/ToolBar.vue";
import {computed, onMounted, ref, watch} from "vue";
import PinMap from "@/components/visualization tools/pinMap.vue";
import ContinentChartComponent from "@/components/visualization tools/ContinentCountryBarChart.vue";
import CountryComparisonChart from "@/components/visualization tools/CountryComparison.vue";
import MotionChartComponent from "@/components/visualization tools/MotionChart.vue";
import InformationalBox from "@/components/visualization tools/InformationalBox.vue";
import Slider from "@vueform/slider";

const TextWidth = ref('65%');
const TextMaxWidth = ref('1000px');
const selectedContinent = ref('Europe');
const comparisonCountries = ref(["Norway", "Sweden"]);
const comparisonData = ref("co2");
const comparisonStartYear = ref(2000);
const comparisonEndYear = ref(2022);
const sliderValue = ref([2000, 2022]);
const input = ref('');

watch(sliderValue, (newValue) => {
  comparisonStartYear.value = newValue[0];
  comparisonEndYear.value = newValue[1];
  console.log('Updated Years:', comparisonStartYear.value, comparisonEndYear.value);

 sliderChange();
}, { immediate: true });

const buttons = [
  {label: "Total", url: "Total Co2 emissions,cumulative_co2", selected: true},
  {label: "Land Usage", url: "Total Co2 emissions including land use,cumulative_co2_including_luc", selected: false},
  {label: "Coal", url: "Total Coal Emissions,cumulative_coal_co2", selected: false},
  {label: "Oil", url: "Total Oil Emissions,cumulative_oil_co2", selected: false},
  {label: "Flaring", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false},
  {label: "Gas", url: "Total Gas Emissions,cumulative_gas_co2", selected: false},
  {label: "Cement", url: "Total Cement Emissions,cumulative_cement_co2", selected: false}
];

const barchartButtons = [
  {label: "Total Bar", url: "Total Co2 emissions,cumulative_co2", selected: true, name:"Total"},
  {label: "Land Usage Bar", url: "Total Co2 emissions including land use,cumulative_co2_including_luc", selected: false, name:"Land Usage"},
  {label: "Coal Bar", url: "Total Coal Emissions,cumulative_coal_co2", selected: false, name:"Coal"},
  {label: "Oil Bar", url: "Total Oil Emissions,cumulative_oil_co2", selected: false, name:"Oil"},
  {label: "Flaring Bar", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Bar", url: "Total Gas Emissions,cumulative_gas_co2", selected: false, name: "Gas"},
  {label: "Cement Bar", url: "Total Cement Emissions,cumulative_cement_co2", selected: false, name: "Cement"}
]

const barchartCompButtons = [
  {label: "Total Comp", url: "Total Co2 emissions,cumulative_co2", selected: true, name:"Total"},
  {label: "Land Usage Comp", url: "Total Co2 emissions including land use,cumulative_co2_including_luc", selected: false, name:"Land Usage"},
  {label: "Coal Comp", url: "Total Coal Emissions,cumulative_coal_co2", selected: false, name:"Coal"},
  {label: "Oil Comp", url: "Total Oil Emissions,cumulative_oil_co2", selected: false, name:"Oil"},
  {label: "Flaring Comp", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Comp", url: "Total Gas Emissions,cumulative_gas_co2", selected: false, name: "Gas"},
  {label: "Cement Comp", url: "Total Cement Emissions,cumulative_cement_co2", selected: false, name: "Cement"}
]

const selectedUrl = ref(buttons[0].url);
const selectedBarUrl = ref(buttons[0].url);
const selectedCompUrl = ref(barchartButtons[0].url);
const countries = ref([]);
const selectedCountryFilter = ref('');
const fetchError = ref(null);
const showDropdown = ref(false);
let preventHide = false;

const filteredCountries = computed(() => {
  if (!input.value) return [];
  return countries.value.filter(country => country.toLowerCase().startsWith(input.value.toLowerCase()));
})

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

onMounted(async () => {
  const data = await fetchData('http://127.0.0.1:5000/countries');
  countries.value = data; // Assign fetched data
  console.log("Fetched countries:", data);
});

function addCountryToFilter(country) {
  if (!comparisonCountries.value.includes(country)) {
    comparisonCountries.value.push(country);
  }
  input.value = '';
  showDropdown.value = false;
}

function removeCountryFromFilter(country) {
  comparisonCountries.value = comparisonCountries.value.filter(c => c !== country);
}

function hideDropdownWithDelay() {
  if (!preventHide) {
    setTimeout(() => {
      showDropdown.value = false;
    }, 200);
  }
}

function preventHideDropdown() {
  preventHide = true;
}

function allowHideDropdown() {
  preventHide = false;
}

function updateUrl(url) {
  selectedUrl.value = url;
  buttons.forEach(button => button.selected = (button.url === url));
}

function handleContinentClick(continent) {
  selectedContinent.value = continent;
  const targetElement = document.getElementById("scroll-point");
  targetElement.scrollIntoView({behavior: "smooth"});
}

function updateBarUrl(url) {
  selectedBarUrl.value = url;
  barchartButtons.forEach(button => button.selected = (button.url === url));
}

function updateCompData(url) {
  selectedCompUrl.value = url;
  barchartCompButtons.forEach(button => button.selected = (button.url === url));
}

function sliderChange() {
  [comparisonStartYear.value, comparisonEndYear.value] = sliderValue.value;
  console.log("Slider value changed:", sliderValue.value);
}
</script>

<template>
  <ToolBar/>
  <div class="main-container">
    <h1 :style="{ width: TextWidth, maxWidth: TextMaxWidth }">Let's dive into the story of our greenhouse gas
      emissions</h1>
    <div class="textcontainer" :style="{ width: TextWidth, maxWidth: TextMaxWidth }">
      <p>
        The world is facing the ever-important challenge of climate change. How can we solve it? This question has
        become increasingly urgent as we witness the devastating impacts of global warming, from rising sea levels to
        extreme weather events. Addressing climate change requires a multifaceted approach, including reducing
        greenhouse gas emissions, transitioning to renewable energy sources, and implementing sustainable practices in
        agriculture and industry. Governments, businesses, and individuals all have a role to play in this global
        effort. By investing in clean technologies, promoting energy efficiency, and supporting policies that protect
        the environment, we can work together to mitigate the effects of climate change and build a more sustainable
        future for generations to come. </p>
    </div>

    <div class="map-container">
      <div class="mapHeader">
        <h2>Co2 Emissions Per Continent as Percentage</h2>
      </div>
      <pin-map :url="selectedUrl"/>

      <div class="innerTextContainer">
        <h3>Historic Superpowers Dominate Emissions</h3>
        <p>The history of our emissions follow the empires of old.
          <span style="font-weight: 900; color: #FFA737;">Europe</span>,
          <span style="font-weight: 900; color: #BA7BA1;">North America</span> and
          <span style="font-weight: 900; color: #5BC0EB;">Asia</span> lead the way for total CO<sub>2</sub>
          emissions throughout history, while other continents have struggled to keep up. Although there has been a
          shift in emissions contributions as of late, it is still important to take into account our history when
          comparing today's numbers. Below you can select
          categories to see which regions dominate which sectors of emissions. Try it!
        </p>
        <div class="button-group">
          <div v-for="(button, index) in buttons" :key="index" class="button-container">
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedUrl"
                   @change="updateUrl(button.url)">
            <label :for="button.label">{{ button.label }}</label>
          </div>
        </div>
      </div>
    </div>

    <div class="map-container">
      <div class="mapHeader">
        <h2>Co2 Emissions Per Continent as Percentage</h2>
      </div>
      <MotionChartComponent url="Total Co2 emissions,cumulative_co2"/>
      <div class="innerTextContainer">
        <p>Explore the greenhouse gas emissions data by continent</p>
      </div>
    </div>

    <InformationalBox></InformationalBox>

    <div class="map-container">
      <div class="mapHeader">
        <h2>Explore the greenhouse gas emissions data by country</h2>
      </div>
      <ContinentMap @continent-clicked="handleContinentClick"/>
      <div class="innerTextContainer">
        <p>Explore the greenhouse gas emissions data by continent</p>
      </div>
    </div>
    <br id="scroll-point">
    <div class="bar-container" id="bar-chart">
      <div class="mapHeader">
        <h2>Cumulative data of {{ selectedBarUrl.split(",")[0] }} in {{ selectedContinent }}</h2>
      </div>
      <ContinentChartComponent :continent="selectedContinent" :url="selectedBarUrl"/>
      <div class="innerTextContainer">
        <h3>Country Data</h3>
        <p>This chart highlights data from the continent: <span style="font-weight: 900; color: #FFA737">{{ selectedContinent }}</span>.
          It displays the top 10 countries within a selected category, showcasing cumulative values
          accumulated over the years. Choose a category to explore detailed statistics!</p>
        <div class="button-group">
          <div v-for="(button, index) in barchartButtons" :key="index" class="button-container">
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedBarUrl"
                   @change="updateBarUrl(button.url)">
            <label :for="button.label">{{ button.name }}</label>
          </div>
        </div>
      </div>
    </div>
    <div class="bar-container">
      <div class="mapHeader">
        <h2>Explore the greenhouse gas emissions data by country</h2>
      </div>
      <CountryComparisonChart :countries="comparisonCountries" :comparisonData="selectedCompUrl.split(',')[1]" :start-year="comparisonStartYear" :end-year="comparisonEndYear"/>
      <div class="innerTextContainer">
          <div class="country-search">
            <input type="text" v-model="input" placeholder="Search for a country" @click="showDropdown = true" @focus="showDropdown = true" @blur="hideDropdownWithDelay">
            <div class="country-list" v-if="showDropdown && filteredCountries.length" @mouseenter="preventHideDropdown" @mouseleave="allowHideDropdown">
              <div class="country-items">
              <div class="country-item" v-for="country in filteredCountries" :key="country" @click="addCountryToFilter(country)">
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
        <p>Explore the greenhouse gas emissions data by country</p>
        <div class="button-group">
          <div v-for="(button, index) in barchartCompButtons" :key="index" class="button-container">
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedCompUrl"
                   @change="updateCompData(button.url)">
            <label :for="button.label">{{ button.name }}</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  margin: 70px auto;
  text-align: left;
  height: 100%;
  width: 100%;
  gap: 50px;
}

h1 {
  text-align: left;
  font-size: 4.5rem;
  font-weight: 900;
  background: linear-gradient(to bottom, rgb(74, 118, 136), rgb(21, 79, 87));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
  margin: auto;
}

h2 {
  font-size: 1.8rem;
  font-weight: 900;
  color: white;
  margin: 0;
}

h3 {
  justify-self: left;
  font-size: 1.6rem;
  font-weight: 900;
  color: #FFA737;
  margin: 0;
}

p {
  text-align: left;
  color: white;
  font-weight: 100;
  font-family: "Corbel Light", serif;
  font-size: 20px;
}

.map-container {
  display: flex;
  justify-content: center;
  background-color: #1E555F;
  position: relative; /* Add this line */
  gap: 20px;
  padding-right: 100px;
}

.map-container::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 0;
  right: 0;
  bottom: 10px;
  border-top: 2px dotted #FFA737;
  border-bottom: 2px dotted #FFA737;
  pointer-events: none;
}

.textcontainer {
  background-color: #1E555F;
  color: white;
  border-radius: 20px;
  padding: 40px;
  position: relative;
  font-size: 1.4rem;
  font-weight: 400;
  margin: auto;

}

.textcontainer::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 2px dotted #FFA737;
  border-radius: 16px;
  pointer-events: none;
}

.innerTextContainer {
  color: white;
  border-radius: 18px;
  padding: 40px;
  position: relative;
  font-size: 1.4rem;
  font-weight: 400;
  margin: 60px 0px 60px 20px;
  border: 2px dotted #FFA737;
  max-width: 30%;
  width: 100%;
  box-sizing: border-box;
  display: grid;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.mapHeader {
  position: absolute;
  color: white;
  top: 10px;
  left: 10px;
  padding: 10px;
  z-index: 1;
}

.bar-container {
  display: flex;
  justify-content: center;
  background-color: #1E555F;
  position: relative; /* Add this line */
  gap: 20px;
  padding-left: 25px;
  padding-top: 100px;
  padding-right: 100px;
}

.bar-container::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 0;
  right: 0;
  bottom: 10px;
  border-top: 2px dotted #FFA737;
  border-bottom: 2px dotted #FFA737;
  pointer-events: none;
}

.comparison-container {
  display: flex;
  justify-content: center;
  background-color: #1E555F;
  position: relative; /* Add this line */
  gap: 20px;
  padding-left: 25px;
  padding-top: 50px;
  padding-bottom: 100px;
}

.comparison-container::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 0;
  right: 0;
  bottom: 10px;
  border-top: 2px dotted #FFA737;
  border-bottom: 2px dotted #FFA737;
  pointer-events: none;
}

.button-group {
  margin-top: 10px;
  justify-self: center;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.country-search {
  position:relative;
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
  margin-top: 30px;
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
  height: 200px;
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

@media screen and (max-width: 1400px) {
  .map-container {
    flex-direction: column-reverse;
    padding: 0 100px;
    gap: 0;
  }

  .innerTextContainer {
    max-width: 100%;
    width: 100%;
    margin: 80px 0 0 0;
    gap: 20px;
  }

  .mapHeader {
    display: none;
  }

  .bar-container {
    flex-direction: column-reverse;
    padding: 0 100px;
    gap: 0;
  }

  .comparison-container {
    flex-direction: column-reverse;
    padding: 0 100px;
    gap: 0;
  }

  .button-group {
    margin-top: 0;
  }
}
</style>