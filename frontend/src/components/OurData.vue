<script setup>
</script>

<template>
  <div class="ourdata-box">
    <h1>Our Data</h1>
    <div class="content">
      <p>This project was made as part of an assignment at <span
          style="font-weight: 900; color: #9da9e7; font-family: Inter,sans-serif">NTNU ÅLESUND</span> for the <span
          style="font-weight: 900; color: #e79dc2; font-family: Inter,sans-serif">IE500417 COURSE.</span> The dataset
        provided by the course is linked below together with all other datasets used for this project. We hope to have
        selected <span
            style="font-weight: 900; color: #bee79d; font-family: Inter,sans-serif">RELIABLE SOURCES</span> to give the user the honest truth. </p>
    </div>
    <div class="sources">
      <div id="left">
        <h2>Datasets</h2>
        <p>Original: <a href="https://drive.google.com/file/d/1XKkWOjjp4SZv0NPFvbE6_Ye5dbq0SYTg/view?usp=sharing">View</a></p>
        <p>Electricity Production: <a href="https://drive.google.com/file/d/1U8nHaXshJV3-NK7fbNS_4QinmC3gq4ly/view?usp=sharing">View</a></p>
        <p>World Information: <a href="https://drive.google.com/file/d/1gX2hrhmcQlPU9et-zbfj2jyGLQtRsCPU/view?usp=sharing">View</a></p>
      </div>
      <div id="right">
        <h2>Sources</h2>
        <p>Dataset was given with task</p>
        <p>Our World in Data: <a href="https://ourworldindata.org/electricity-mix">Go to</a></p>
        <p>Kaggle: <a href="https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023">Go to</a> </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ourdata-box {
  background-color: #1E555F;
  color: white;
  border-radius: 20px;
  padding: 40px;
  position: relative;
  font-size: 1.4rem;
  font-weight: 400;
  margin: auto;
}

.ourdata-box::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 2px dotted #FFA737;
  border-radius: 16px;
  pointer-events: none;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #FFA737;
}

.sources {
  padding: 0 20%;
  margin: 30px 0;
  display: flex;
  justify-content: space-between;
}

.content > p {
  font-family: "Corbel Light", sans-serif;
  font-size: 1.4rem;
  margin: 5px 0;
}


h2 {
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: #ffffff;
}

p {
  margin: 5px 0;
  color: #ffffff;
  font-family: "Corbel Light", sans-serif;
  font-size: 1.5rem;
}

a {
  color: #FFA737;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
  background-color: transparent;
  cursor: pointer;
}
</style>