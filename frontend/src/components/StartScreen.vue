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

<style scoped>
h1 {
  font-size: 4rem;
  margin-bottom: 0px;
}

.start-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(3, 218, 198, 0.2);
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