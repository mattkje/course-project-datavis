<script setup>

import Globe from "@/components/Globe.vue";
import ToolBar from "@/components/ToolBar.vue";
import CountryInfoBox from "@/components/CountryInfoBox.vue";
import SearchBar from "@/components/SearchBar.vue";
import StartScreen from "@/components/StartScreen.vue";
import ContinentMap from "@/components/ContinentMap.vue";
import MainStoryPage from "@/components/MainStoryPage.vue";
</script>

<template>
  <MainStoryPage />
</template>

<style scoped>
html, body, #app {
  height: 100%;
  width: 100%;
  margin: 0;
  background-color: #f0f0f0; /* Example: change background color */
  font-family: Arial, sans-serif; /* Example: change font family */
}
</style>
