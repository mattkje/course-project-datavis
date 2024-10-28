<template>

    <div class="info-box">
      <h2>{{ countryName }}</h2>
      <hr>
      <p>Population: {{ population }}</p>
      <p>Area: {{ area }} km²</p>
      <p>Capital: {{ capital }}</p>
  </div>

</template>

<script setup>
import { ref } from 'vue';
import SearchBar from "@/components/SearchBar.vue";

const countryName = ref('Norway');
const population = ref('5,630,341');
const area = ref('385,207');
const capital = ref('Oslo');
</script>

<style scoped>


.info-box {
  position: absolute;
  right: 0;
  top: 70px;
  width: 25vw;
  height: calc(100% - 70px - 3rem);
  padding: 20px;
  margin: 1.5rem;
  background: rgba(30, 30, 30, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  color: #f2f2f2;
  font-family: Inter, sans-serif;
  font-weight: 900;
  font-size: 2rem;
}

p {
  font-family: Inter, sans-serif;
  font-weight: bold;
  margin: 5px 0;
  color: #f2f2f2;
}
</style>