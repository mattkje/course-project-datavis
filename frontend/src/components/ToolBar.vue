<script setup>
import { ref } from 'vue';

</script>

<template>
  <div class="toolbar">
    <div class="title-box">
      <img src="../assets/logo.svg" alt="Logo" class="logo"  />
      <h1 class="title">Globe World Stats</h1>
    </div>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  background-color: var(--color-background-soft);
  justify-content: left;
  padding: 1rem;
  color: #ffffff; /* White text color */
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
  font-weight: 900;
  font-size: 1.5rem;
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.7s ease-in-out;
}

.title-box:hover .title {
  opacity: 1;
  transform: translateX(0);
}
</style>