<script setup>
import { ref } from 'vue';

const rankings = ref([
  { country: 'Country A', number: 1, category: 'GDP' },
  { country: 'Country A', number: 2, category: 'Population' },
]);
</script>

<template>
  <div class="key-info-box">
    <p v-for="(ranking, index) in rankings" :key="index">
      {{ ranking.country }} is ranked <span class="highlight">#{{ ranking.number }}</span> in {{ ranking.category }}
    </p>
  </div>
</template>

<style scoped>
.key-info-box {
  padding: 20px;
  margin-top: 100px;
  height: 500px;
  width: 30%;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  font-family: Arial, sans-serif;
  color: #000000;
  align-items: start;
  display: flex;
  flex-direction: column;
}

p {
  font-family: "American Typewriter";
}

.highlight {
  color: #03D3C1;
}
</style>