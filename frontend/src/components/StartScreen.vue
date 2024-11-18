<script setup>
import { ref } from 'vue';
import { useGeolocation } from '@vueuse/core';
import { selectCountryByLongLat } from './Globe.vue';

const isVisible = ref(true);
const { coords, locatedAt, error, resume, pause } = useGeolocation();

const hideStartScreen = async () => {
  isVisible.value = false;
  try {
    if (coords.value) {
      const { latitude, longitude } = coords.value;
      console.log('Geolocation:', latitude, longitude);
      selectCountryByLongLat(longitude, latitude);
    } else {
      console.error('Geolocation not available');
    }
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <div v-if="isVisible" class="start-screen">
    <div class="content">
      <h1>Welcome to Globe World Stats</h1>
      <h2>Embark on a visual journey of our greenhouse history</h2>
      <button @click="hideStartScreen">Explore the World</button>
    </div>
  </div>
</template>

<style>
h1 {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(to bottom, rgb(12, 12, 12), rgb(21, 79, 87));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0px;
}

h2 {
  font-size: 1.5rem;
  font-weight: 500;
  margin-top: 0px;
  color: #5b5b5b;
}

.start-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.48), rgba(255, 255, 255, 0.87));
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.content {
  text-align: center;
  color: white;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1.2rem;
  color: white;
  background-color: #03DAC6;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #028a8a;
}
</style>