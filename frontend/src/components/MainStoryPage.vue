<script setup>
import ContinentMap from './visualization tools/ContinentMap.vue';
import ToolBar from "@/components/ToolBar.vue";
import {ref} from "vue";
import PinMap from "@/components/visualization tools/pinMap.vue";

const TextWidth = ref('65%');
const TextMaxWidth = ref('1000px');
const MapContainerWith = ref('100%');

</script>

<template>
  <ToolBar />
  <div class="main-container">
  <h1 :style="{ width: TextWidth, maxWidth: TextMaxWidth }">Let's dive into the story of our greenhouse gas emissions</h1>
    <div class="textcontainer" :style="{ width: TextWidth, maxWidth: TextMaxWidth }">
      <p>
        The world is facing the ever-important challenge of climate change. How can we solve it? This question has become increasingly urgent as we witness the devastating impacts of global warming, from rising sea levels to extreme weather events. Addressing climate change requires a multifaceted approach, including reducing greenhouse gas emissions, transitioning to renewable energy sources, and implementing sustainable practices in agriculture and industry. Governments, businesses, and individuals all have a role to play in this global effort. By investing in clean technologies, promoting energy efficiency, and supporting policies that protect the environment, we can work together to mitigate the effects of climate change and build a more sustainable future for generations to come.      </p>
    </div>

    <div class="map-container">
      <div class="mapHeader">
        <h2>Explore the greenhouse gas emissions data by country</h2>
      </div>
      <pin-map />
      <div class="innerTextContainer">
      </div>
    </div>

    <div class="map-container">
      <div class="innerTextContainer">
        <p>Explore the greenhouse gas emissions data by continent</p>
      </div>
      <ContinentMap />
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
  font-size: 1.5rem;
  font-weight: 900;
  color: white;
  margin: 0;
}

p {
  text-align: left;
  color: white
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
  border: 2px dotted #FFA737; /* Use the background color of .textcontainer */
  max-width: 30%; /* Maximum width of 30% */
  width: 100%; /* Shrink width-wise only if the container is smaller */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
}

.mapHeader {
  position: absolute;
  color: white;
  top: 10px;
  left: 10px;
  padding: 10px;
  z-index: 1;
}
</style>