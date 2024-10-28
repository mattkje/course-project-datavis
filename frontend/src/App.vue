<script setup>

import Globe from "@/components/Globe.vue";
<<<<<<< Updated upstream
import SearchBar from "@/components/SearchBar.vue";
</script>

<template>
  <main>
   <SearchBar />

  </main>
=======
import ToolBar from "@/components/ToolBar.vue";
import CountryInfoBox from "@/components/CountryInfoBox.vue";
</script>

<template>
<ToolBar />
    <Globe />
  <CountryInfoBox />
>>>>>>> Stashed changes
</template>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
}

</style>
