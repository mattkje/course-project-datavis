<script setup>

import Globe from "@/components/Globe.vue";
import ToolBar from "@/components/ToolBar.vue";
import CountryInfoBox from "@/components/CountryInfoBox.vue";
</script>

<template>
<ToolBar />
    <Globe />
  <CountryInfoBox />
</template>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
}

</style>
