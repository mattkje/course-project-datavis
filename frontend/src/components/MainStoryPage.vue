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
import Globe from "@/components/Globe.vue";
import StackedLineGraph from "@/components/visualization tools/StackedLineGraph.vue";
import AmChartComponent from "@/components/visualization tools/statistics_overview.vue";
import WorldClimateGoals from "@/components/WorldClimateGoals.vue";
import OurData from "@/components/OurData.vue";

const TextWidth = ref('65%');
const TextMaxWidth = ref('1000px');
const selectedContinent = ref('Europe');
const comparisonCountries = ref(["China", "United States", "India"]);
const comparisonData = ref("co2");
const comparisonStartYear = ref(2000);
const comparisonEndYear = ref(2022);
const sliderValue = ref([2000, 2022]);
const input = ref('');

watch(sliderValue, (newValue) => {
  comparisonStartYear.value = newValue[0];
  comparisonEndYear.value = newValue[1];

  sliderChange();
}, {immediate: true});

const buttons = [
  {label: "Total", url: "Total Co2 Emissions,cumulative_co2", selected: true},
  {label: "Land Usage", url: "Total Co2 Emissions including land use,cumulative_co2_including_luc", selected: false},
  {label: "Coal", url: "Total Coal Emissions,cumulative_coal_co2", selected: false},
  {label: "Oil", url: "Total Oil Emissions,cumulative_oil_co2", selected: false},
  {label: "Flaring", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false},
  {label: "Gas", url: "Total Gas Emissions,cumulative_gas_co2", selected: false},
  {label: "Cement", url: "Total Cement Emissions,cumulative_cement_co2", selected: false}
];

const barchartButtons = [
  {label: "Total Bar", url: "Total Co2 emissions,cumulative_co2", selected: true, name: "Total"},
  {
    label: "Land Usage Bar",
    url: "Total Co2 emissions including land use,cumulative_co2_including_luc",
    selected: false,
    name: "Land Usage"
  },
  {label: "Coal Bar", url: "Total Coal Emissions,cumulative_coal_co2", selected: false, name: "Coal"},
  {label: "Oil Bar", url: "Total Oil Emissions,cumulative_oil_co2", selected: false, name: "Oil"},
  {label: "Flaring Bar", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Bar", url: "Total Gas Emissions,cumulative_gas_co2", selected: false, name: "Gas"},
  {label: "Cement Bar", url: "Total Cement Emissions,cumulative_cement_co2", selected: false, name: "Cement"}
]

const barchartCompButtons = [
  {label: "Total Comp", url: "Total Co2 emissions,cumulative_co2", selected: true, name: "Total"},
  {
    label: "Land Usage Comp",
    url: "Total Co2 emissions including land use,cumulative_co2_including_luc",
    selected: false,
    name: "Land Usage"
  },
  {label: "Coal Comp", url: "Total Coal Emissions,cumulative_coal_co2", selected: false, name: "Coal"},
  {label: "Oil Comp", url: "Total Oil Emissions,cumulative_oil_co2", selected: false, name: "Oil"},
  {label: "Flaring Comp", url: "Total Flaring Emissions,cumulative_flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Comp", url: "Total Gas Emissions,cumulative_gas_co2", selected: false, name: "Gas"},
  {label: "Cement Comp", url: "Total Cement Emissions,cumulative_cement_co2", selected: false, name: "Cement"}
]

const linechartContinentButtons = [
  {label: "Total Line", url: "million tonnes,predictContinents/co2", selected: true, name: "Total"},
  {
    label: "Land Usage Line",
    url: "million tonnes,predictContinents/co2_including_luc",
    selected: false,
    name: "Land Usage"
  },
  {label: "Coal Line", url: "million tonnes,predictContinents/coal_co2", selected: false, name: "Coal"},
  {label: "Oil Line", url: "million tonnes,predictContinents/oil_co2", selected: false, name: "Oil"},
  {label: "Flaring Line", url: "million tonnes,predictContinents/flaring_co2", selected: false, name: "Flaring"},
  {label: "Gas Line", url: "million tonnes,predictContinents/gas_co2", selected: false, name: "Gas"},
  {label: "Cement Line", url: "million tonnes,predictContinents/cement_co2", selected: false, name: "Cement"}
]

const selectedUrl = ref(buttons[0].url);
const selectedBarUrl = ref(buttons[0].url);
const selectedCompUrl = ref(barchartButtons[0].url);
const selectedContinentUrl = ref(linechartContinentButtons[0].url);
const countries = ref([]);
const selectedCountryFilter = ref('');
const fetchError = ref(null);
const showDropdown = ref(false);
let preventHide = false;
const detailed = ref(false);

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
  countries.value = await fetchData('http://127.0.0.1:5000/countries'); // Assign fetched data
});

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

function updateContinentData(url) {
  selectedContinentUrl.value = url;
  linechartContinentButtons.forEach(button => button.selected = (button.url === url));
}

function sliderChange() {
  [comparisonStartYear.value, comparisonEndYear.value] = sliderValue.value;
}

function selectFirstOption() {
  if (filteredCountries.value.length > 0) {
    addCountryToFilter(filteredCountries.value[0]);
  }
  showDropdown.value = true;
}

function toggleDetailed() {
  detailed.value = !detailed.value;
}

function scrollToGlobe() {
  const globeElement = document.getElementById('globe-container');
  globeElement.scrollIntoView({behavior: 'smooth', block: 'center'});
}
</script>

<template>
  <ToolBar/>
  <div class="main-container">
    <div class="logoContainer">
      <img src="../assets/logo.png" alt="Globe World Stats Logo" class="logo">
      <h1>Let's dive into the story of our greenhouse gas
        emissions</h1>
    </div>

    <div class="textcontainer" :style="{ width: TextWidth, maxWidth: TextMaxWidth }">
      <p>
        The world is slowly coming to the realization that <span
          style="font-weight: 900; color: #cce79d; font-family: Inter,sans-serif">GLOBAL WARMING</span> is the biggest
        issue we are facing as a global
        community. Mass production has led to great growth for society as a whole, but it has led us to <span
          style="font-weight: 900; color: #e16350; font-family: Inter,sans-serif">IGNORE</span> the
        consequences of our actions. From rising sea levels to extreme weather events, it’s getting increasingly obvious
        that something needs to <span
          style="font-weight: 900; color: #67c563; font-family: Inter,sans-serif">CHANGE</span>. The team behind Globe
        World Stats strongly believes that knowledge of our
        climate history as well as where they are headed, is key to fully supporting the measures necessary to <span
          style="font-weight: 900; color: #f6d0a0; font-family: Inter,sans-serif">REVERT</span>
        our changes. We hope you find value in the experience you are about to start, enjoy. </p>
    </div>

    <div class="sectionHeader">
      First, Let's Look at the Past
    </div>


    <div class="map-container">
      <div class="mapHeader">
        <h2>Our Climate History, Summarized</h2>
      </div>
      <MotionChartComponent url="Total Co2 emissions,cumulative_co2"/>
      <div class="innerTextContainer">
        <h3>The Pollution Evolution</h3>
        <p>Let's start our journey by looking through the evolution of climate emissions. The past provides insight into
          the situation we find ourselves in today.
          See which empires dominated early on, inspect outliers and see the rise of our current powerhouses.Enjoy the
          "movie" and explore each country to see where they lie on the climate scale.</p>
        <br/>
        <p>Spot something interesting?</p>
      </div>
    </div>

    <div class="afterTextContainer">
      <h5> A couple of countries are clear outliers, let's have a look a them.</h5>
    </div>
    <InformationalBox></InformationalBox>

    <div class="sectionHeader">
      Now, Let's Dive Into the Present
    </div>

    <div class="map-container">
      <div class="mapHeader">
        <h2>Co2 Emissions Per Continent as Percentage</h2>
      </div>
      <pin-map :url="selectedUrl"/>

      <div class="innerTextContainer">
        <h3>Historic Superpowers Dominate Emissions</h3>
        <p>The history of our emissions follow the empires of old.
          <span style="font-weight: 900; color: #FFA737; font-family: Inter,sans-serif">EUROPE</span>,
          <span style="font-weight: 900; color: #BA7BA1; font-family: Inter,sans-serif">NORTH AMERICA</span> and
          <span style="font-weight: 900; color: #5BC0EB; font-family: Inter,sans-serif">ASIA</span> lead the way for
          total CO<sub>2</sub>
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
        <h2>Explore the Greenhouse Gas Emission Data By Continent</h2>
      </div>
      <ContinentMap @continent-clicked="handleContinentClick"/>
      <div class="innerTextContainer">
        <p>
          Let's dive into the data of the continents.
          Click on the <span style="font-weight: 900; color: #c2eb5b; font-family: Inter,sans-serif">CONTINENT</span>
          you are the most interested in learning about to
          view the countries with the highest greenhouse gas emissions within it.
        </p>
      </div>
    </div>
    <br id="scroll-point">
    <div class="bar-container">
      <div class="mapHeader">
        <h2>{{ selectedBarUrl.split(",")[0] }} in {{ selectedContinent }}</h2>
      </div>
      <ContinentChartComponent :continent="selectedContinent" :url="selectedBarUrl"/>
      <div class="innerTextContainer">
        <h3>10 Biggest Polluters</h3>
        <p>This chart highlights the combined Co<sub>2</sub> emissions from <span
            style="font-weight: 900; color: #FFA737; font-family: Inter,sans-serif">{{ selectedContinent }}</span> over
          the last 200 years. Try changing the category to see the different nations contribution.</p>
        <div class="button-group">
          <div v-for="(button, index) in barchartButtons" :key="index" class="button-container">
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedBarUrl"
                   @change="updateBarUrl(button.url)">
            <label :for="button.label">{{ button.name }}</label>
          </div>
        </div>
        <div class="measurement">
          Measured in <span
            style="font-weight: 900; color: #f5d4a8; font-family: Inter,sans-serif">million tonnes</span>
        </div>
      </div>
    </div>
    <div class="bar-container">
      <div class="mapHeader">
        <h2>Compare Co2 Emission From Different Countries</h2>
      </div>
      <CountryComparisonChart :countries="comparisonCountries.join(',')" :comparisonData="selectedCompUrl.split(',')[1]"
                              :start-year="comparisonStartYear" :end-year="comparisonEndYear"/>
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
            <div class="item-error" v-if="input && !filteredCountries.length">
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
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedCompUrl"
                   @change="updateCompData(button.url)">
            <label :for="button.label">{{ button.name }}</label>
          </div>
        </div>
        <div class="measurement">
          Measured in <span
            style="font-weight: 900; color: #f5d4a8; font-family: Inter,sans-serif">million tonnes</span>
        </div>
      </div>
    </div>
    <div class="sectionHeader">
      Our Future
    </div>
    <div class="bar-container">
      <div class="mapHeader">
        <h2>Co2 Emissions Predictions the Next 5 Years</h2>
      </div>
      <AmChartComponent :url="selectedContinentUrl" :key="selectedContinentUrl" :isContinent="true"/>
      <div class="innerTextContainer">
        <p>
          These are our <span
            style="font-weight: 900; color: #f5a8a8; font-family: Inter,sans-serif">PREDICTIONS</span> for the next 5
          years. The data is based on the current trend of emissions. As you
          can see, <span style="font-weight: 900; color: #5BC0EB; font-family: Inter,sans-serif">ASIA</span> is expected
          to continue its growth in emissions, while <span
            style="font-weight: 900; color: #FFA737; font-family: Inter,sans-serif">EUROPE</span>, and <span
            style="font-weight: 900; color: #BA7BA1; font-family: Inter,sans-serif">NORTH AMERICA</span> are
          expected to
          slightly decrease their emissions. <span
            style="font-weight: 900; color: #5BC0EB; font-family: Inter,sans-serif">ASIA</span> is entering it's
          <span
              style="font-weight: 900; color: #e57365; font-family: Inter,sans-serif">MASS PRODUCTION</span> phase similar to what the western
          countries experienced earlier. The issue, as you will see below is that their emissions might not be as <span
            style="font-weight: 900; color: #6eeb5b; font-family: Inter,sans-serif">CLEAN</span>
          as western nations.
        </p>
        <div class="button-group">
          <div v-for="(button, index) in linechartContinentButtons" :key="index" class="button-container">
            <input type="radio" :id="button.label" :value="button.url" v-model="selectedContinentUrl"
                   @change="updateContinentData(button.url)">
            <label :for="button.label">{{ button.name }}</label>
          </div>
        </div>
      </div>
    </div>
    <div class="bar-container">
      <div class="multipleContainer">
        <StackedLineGraph :url="'percentage,electricity_percentage/China,false'" :detailed="detailed"/>
        <StackedLineGraph url="percentage,electricity_percentage/United States,false" :detailed="detailed"/>
        <StackedLineGraph url="percentage,electricity_percentage/Saudi Arabia,false" :detailed="detailed"/>
      </div>
      <div class="innerTextContainer">
        <h3>Electricity Production</h3>
        <p>Electricity production is a key factor in the world's greenhouse gas emissions. The top 3 countries in
          electricity production are <span
              style="font-weight: 900; color: #FFA737; font-family: Inter,sans-serif">CHINA</span>,
          <span style="font-weight: 900; color: #BA7BA1; font-family: Inter,sans-serif">UNITED STATES</span> and
          <span style="font-weight: 900; color: #5BC0EB; font-family: Inter,sans-serif">SAUDI ARABIA</span>. The chart
          above
          shows the percentage of
          electricity production in each country. The data is retrieved from Our World In Data.
        </p>
        <div class="toggle-container">
          <label class="toggle-label">
            Detailed View
            <input type="checkbox" v-model="detailed">
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>
    </div>
    <div class="textcontainer" :style="{ width: TextWidth, maxWidth: TextMaxWidth }">
      <p>
        Western countries are <span
          style="font-weight: 900; color: #f5c6a8; font-family: Inter,sans-serif">MOVING AWAY</span> from the
        traditional fossil fuels at a pace that needs to be matched by the
        rest of the world.
        However, these countries need to provide the necessary <span
          style="font-weight: 900; color: #a8ecf5; font-family: Inter,sans-serif">SUPPORT</span> to the developing world
        to ensure that the
        transition happens as quickly as possible. Moving large amounts of production overseas only prolongs the
        problem. We require a <span
          style="font-weight: 900; color: #f5f1a8; font-family: Inter,sans-serif">FUNDAMENTAL TRANSITION</span> into a
        climate positive production chain, as we are just as strong
        as our weakest link. Move production back to more sustainable methods, Lift the developing world up to the
        standards we aspire to reach and <span
          style="font-weight: 900; color: #f5a8f1; font-family: Inter,sans-serif">TOGETHER</span> we can make a
        difference.
      </p>
      <br/><br/>
      <p>
        Before sending you off to explore the data yourself, we want to <span
          style="font-weight: 900; color: #f5a8bd; font-family: Inter,sans-serif">THANK YOU</span> for taking the time
        to go on this <span
          style="font-weight: 900; color: #a8def5; font-family: Inter,sans-serif">JOURNEY.</span> We hope you found
        value in this presentation and that you aspire to <span
          style="font-weight: 900; color: #a8f5ae; font-family: Inter,sans-serif">BECOME AN EXAMPLE</span> for the world
        you want to live in.
      </p>
    </div>
    <div class="lastHeader">
      <h4>What can we do?</h4>
      <WorldClimateGoals/>
    </div>

    <div class="sectionHeader">
      Enjoy exploring our data!
    </div>

    <div class="map-container" id="globe-container">
      <Globe/>
    </div>
    <!-- Fixed Icon Button -->
    <button class="scroll-button" @click="scrollToGlobe">
      <font-awesome-icon icon="fa-solid fa-globe" style="color: #FFFFFF; height: 22px"/>
    </button>
  </div>
</template>

<style scoped>

.country-information-con {
  display: flex;
  justify-content: center;
  background-color: #1E555F;
  position: relative;
  gap: 20px;
  padding-top: 50px;
  padding-left: 25px;
  padding-right: 100px;
}

.country-information-con::before {
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


.lastHeader {
  margin: auto;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.measurement {
  text-align: end;
  position: relative;
  bottom: 0;
  right: 0;
  font-size: 0.9rem;
}

h4 {
  margin: 50px auto;
  font-size: 4rem;
  font-weight: 900;
  color: #1e555f;
}

h5 {
  font-size: 3.5rem;
  font-weight: 900;
  color: #1e555f;
  max-width: 60vw;
  margin: auto;

}

.scroll-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #1E555F;
  border: 2px solid #FFFFFF;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-container {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.toggle-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  gap: 10px
}

.toggle-label input {
  display: none;
}

.toggle-slider {
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 20px;
  position: relative;
  transition: background-color 0.2s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  background-color: white;
  border-radius: 50%;
  top: 1px;
  left: 1px;
  transition: transform 0.2s;
}

.toggle-label input:checked + .toggle-slider {
  background-color: #FFA737;
}

.toggle-label input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.main-container {
  display: flex;
  flex-direction: column;
  margin: 70px auto;
  text-align: left;
  height: 100%;
  width: 100%;
  gap: 50px;
}

.logoContainer {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  max-width: 1000px;
  width: 65%;
  margin: auto;
  gap: 20px;
}

.logo {
  position: absolute;
  right: 0;
  top: 25%;
  width: 200px;
  height: 200px;

}

h1 {
  text-align: left;
  font-size: 4.5rem;
  font-weight: 900;
  background: linear-gradient(to bottom, rgb(74, 118, 136), rgb(21, 79, 87));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
  width: 80%;
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
  font-size: 22px;
}

.map-container {
  display: flex;
  justify-content: center;
  background-color: #1E555F;
  position: relative; /* Add this line */
  gap: 20px;
  padding-right: 50px;
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

.textcontainer p {
  font-size: 24px;
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

.multipleContainer {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  justify-content: center;
  max-width: 70%;
  width: 100%;
  height: 700px;
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
  align-items: center;
  background-color: #1E555F;
  position: relative; /* Add this line */
  gap: 20px;
  padding-top: 50px;
  padding-left: 25px;
  padding-right: 50px;
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
  position: relative;
  width: 100%;
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

.sectionHeader {
  margin: 50vh 0;
  text-align: center;
  font-size: 4rem;
  font-weight: 900;
  color: #1e555f;
}

#globe-container {
  padding: 0;
}

@media screen and (max-width: 1400px) {
  .multipleContainer {
    margin-top: 20px;
    max-width: 100%;
    height: 500px;
  }

  .map-container {
    flex-direction: column-reverse;
    padding: 0 50px;
    gap: 0;
  }

  .innerTextContainer {
    max-width: 100%;
    width: 95%;
    margin: 80px auto 0 auto;
    gap: 20px;
  }

  .mapHeader {
    display: none;
  }

  .bar-container {
    flex-direction: column-reverse;
    padding: 0 50px;
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

  .logoContainer {
    flex-direction: column-reverse;
    align-items: center;
    min-width: 0;
    gap: 0px
  }

  .logo {
    margin: 40px 0;
    position: relative;
    width: 150px;
    height: 150px;
  }

  h1[data-v-eb6a0664] {
    width: 100% !important;
  }
}
</style>