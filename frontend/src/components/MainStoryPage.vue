<script setup>
import ContinentMap from './visualization tools/ContinentMap.vue';
import ToolBar from "@/components/ToolBar.vue";
import {ref} from "vue";
import PinMap from "@/components/visualization tools/pinMap.vue";
import ChartComponent from "@/components/visualization tools/ContinentCountryBarChart.vue";
import ContinentChartComponent from "@/components/visualization tools/ContinentCountryBarChart.vue";
import CountryComparisonChart from "@/components/visualization tools/CountryComparison.vue";
import MotionChartComponent from "@/components/visualization tools/MotionChart.vue";

const TextWidth = ref('65%');
const TextMaxWidth = ref('1000px');
const selectedContinent = ref('Europe');

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

const selectedUrl = ref(buttons[0].url);
const selectedBarUrl = ref(buttons[0].url);

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
      <CountryComparisonChart/>
      <div class="innerTextContainer">
        <p>Explore the greenhouse gas emissions data by country</p>
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