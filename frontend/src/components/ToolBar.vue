<script setup>
import { ref } from 'vue';
import { Label } from 'radix-vue';

import '@fortawesome/fontawesome-free/css/all.css';
</script>

<template>
  <div class="toolbar">
    <div class="title-box">
      <img src="../assets/logo.svg" alt="Logo" class="logo" />
      <h1 class="title">Globe World Stats</h1>
    </div>
    <i class="fas fa-info-circle about-icon"></i>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  background-color: var(--color-background-soft);
  justify-content: space-between;
  padding: 1rem;
  color: #000; /* White text color */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  z-index: 1000; /* Ensure it stays on top */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title-box {
  display: flex;
  align-items: center;
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 1rem;
  transition: all 0.7s ease-in-out;
}

.title-box:hover .logo {
  transform: rotate(360deg) scale(1.2);
}

.title {
  font-family: Inter, sans-serif;
  color: #2c2c2c;
  font-weight: 900;
  font-size: 1.5rem;
  transition: all 0.7s ease-in-out;
}

.search-box {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.LabelRoot {
  margin-right: 0.5rem;
  font-family: Inter, sans-serif;
  font-weight: 700;
  transform: translateX(100px);
  color: var(--color-text);
}

.Input {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  font-family: Inter, sans-serif;
  font-size: 1rem;
  color: var(--color-text);
  background-color: var(--color-background-mute);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.Input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(187, 134, 252, 0.5);
  outline: none;
}

</style>