<script setup>
import '@fortawesome/fontawesome-free/css/all.css';
import About from "@/components/About.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const scrollToBottom = () => {
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
};

</script>

<template>
  <div class="toolbar">
    <div class="title-box">
      <img src="../assets/logo.png" alt="Logo" class="logo" />
      <h1 class="title">EcoConsequence</h1>
    </div>
    <div class="rightside">
      <h2 @click="scrollToBottom">Our Data</h2>
      <About />
    </div>
  </div>
  <button class="back-to-top" @click="scrollToTop">
    <font-awesome-icon :icon="['fas', 'arrow-up']" />
  </button>
</template>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  background-color: var(--color-background-soft);
  justify-content: space-between;
  padding: 1rem;
  color: #000;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title-box {
  display: flex;
  align-items: center;
  cursor: pointer;
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

.rightside {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

h2 {
  font-family: Inter, sans-serif;
  font-weight: 900;
  font-size: 1.2rem;
  color: #1E555F;
  cursor: pointer;
}
.back-to-top {
  position: fixed;
  bottom: 80px;
  right: 20px;
  background-color: #1E555F;
  color: white;
  border: none;
  border-radius: 50%;
  border: 2px solid #FFFFFF;
  padding: 15px;
  cursor: pointer;
  font-size: 1.5rem;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  width: 50px;
  height: 50px;
}

.back-to-top:hover {
  background-color: #144a4f;
}
</style>