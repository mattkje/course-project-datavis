<script setup lang="ts">
import { ref } from 'vue'
import { HoverCardArrow, HoverCardContent, HoverCardPortal, HoverCardRoot, HoverCardTrigger } from 'radix-vue'

const hoverState = ref(false)
</script>

<template>
  <HoverCardRoot v-model:open="hoverState">
    <HoverCardTrigger
        class="ImageTrigger"
        target="_blank"
        rel="noreferrer noopener"
    >
      <font-awesome-icon icon="fa-solid fa-circle-info" style="color: #1E555F;" size="xl"/>
    </HoverCardTrigger>
    <HoverCardPortal>
      <HoverCardContent
          class="HoverCardContent"
          :side-offset="5"
      >
        <div :style="{ display: 'flex', flexDirection: 'column', gap: 7 }">
          <img
              class="Image large"
              src="../assets/logo.png"
              alt="Radix UI"
          >
          <div :style="{ display: 'flex', flexDirection: 'column', gap: 15 }">
            <div>
              <div class="Text bold">
                Globe World Stats
              </div>
              <div class="Text faded">
                By Gruppe 5
              </div>
            </div>
            <hr>
            <div class="Text">
              Made as a part of the course project in the course IE500417 at NTNU.
            </div>
            <hr>
            <div class="Text">
              This project visualizes global statistics using an interactive 3D globe. It includes data on population, area, and capital cities for various countries.
            </div>
            <hr>
            <div class="Text">
              Credits: Matti, Adrian, Håkon.
            </div>
          </div>
        </div>

        <HoverCardArrow
            class="HoverCardArrow"
            :width="8"
        />
      </HoverCardContent>
    </HoverCardPortal>
  </HoverCardRoot>
</template>

<style>
@import '@radix-ui/colors/mauve.css';

/* reset */
a {
  all: unset;
}

.HoverCardContent {
  border-radius: 6px;
  padding: 20px;
  width: 300px;
  background-color: white;
  box-shadow: hsl(206 22% 7% / 35%) 0px 10px 38px -10px, hsl(206 22% 7% / 20%) 0px 10px 20px -15px;
  animation-duration: 400ms;
  animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform, opacity;
}
.HoverCardContent[data-side='top'] {
  animation-name: slideDownAndFade;
}
.HoverCardContent[data-side='right'] {
  animation-name: slideLeftAndFade;
}
.HoverCardContent[data-side='bottom'] {
  animation-name: slideUpAndFade;
}
.HoverCardContent[data-side='left'] {
  animation-name: slideRightAndFade;
}

.HoverCardArrow {
  fill: white;
}

.ImageTrigger {
  cursor: pointer;
  border-radius: 100%;
  display: inline-block;
}
.ImageTrigger:focus {
  box-shadow: 0 0 0 2px white;
}

.Image {
  display: block;
  border-radius: 100%;
}
.Image.normal {
  width: 45px;
  height: 45px;
}
.Image.large {
  width: 60px;
  height: 60px;
}

.Text {
  margin: 0;
  color: #4d4d4d;
  font-size: 15px;
  line-height: 1.5;
}

hr {
  margin: 15px 0;
  border: 0;
  border-top: 1px solid #e6e6e6;
}

.Text.faded {
  color: var(--mauve-10);
}
.Text.bold {
  font-weight: 500;
}

@keyframes slideUpAndFade {
  0% {
    opacity: 0;
    transform: translateY(2px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideRightAndFade {
  0% {
    opacity: 0;
    transform: translateX(-2px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideDownAndFade {
  0% {
    opacity: 0;
    transform: translateY(-2px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideLeftAndFade {
  0% {
    opacity: 0;
    transform: translateX(2px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>