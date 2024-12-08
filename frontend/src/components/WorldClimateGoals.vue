<template>
  <div class="climate-goals">
    <div v-for="(goal, index) in goals" :key="index" class="goal">
      <div class="goal-number">{{ index + 1 }}</div>
      <div class="goal-content">
        <div class="goal-text">
          <p class="title">{{ goal.text }}</p>
          <p class="description">{{ goal.description }}</p>
          <div class="goal-sources">
            <p>{{ goal.resourcesText }}</p>
            <ul>
              <li v-for="(source, sIndex) in goal.sources" :key="sIndex">
                <a :href="source.url" target="_blank">{{ source.name }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const goals = ref([
  {
    text: 'Invest in Nuclear Energy',
    description: 'Nuclear energy is a clean, safe and efficient electricity.',
    resourcesText: 'Learn more about Nuclear Energy:',
    sources: [
      { name: 'Advantages and Challenges of Nuclear Energy', url: 'https://www.energy.gov/ne/articles/advantages-and-challenges-nuclear-energy' },
      { name: '5 Reasons to Embrace Nuclear Energy', url: 'https://www.weforum.org/stories/2024/01/nuclear-energy-transistion-climate-change/' }
    ]
  },
  {
    text: 'Integrate Vegan Meals Into Your Diet.',
    description: 'Industrial farming is a major contributor to climate change.',
    resourcesText: 'Want to go vegan? Check out these resources:',
    sources: [
      { name: 'Why Go Vegan? - Vegan Society', url: 'https://www.vegansociety.com/go-vegan/why-go-vegan' },
      { name: 'Amazing Vegan Meals', url: 'https://www.foodandwine.com/special-diets/vegan/vegan-recipes' }
    ]
  },
  {
    text: 'Protect our Nature',
    description: 'Lush forests, healthy oceans, and thriving wildlife are essential.',
    resourcesText: 'The Organizations that are working to protect our planet:',
    sources: [
      { name: 'Nature.org - Protecting Ocean, Land & Fresh Water', url: 'https://www.nature.org/en-us/' },
      { name: 'Wild.org - Protecting the Worlds Animals', url: 'https://wild.org' }
    ]
  },
  {
    text: 'Reduce Unnecessary Consumption',
    description: 'Yes, we also play a role in climate change.',
    resourcesText: 'Get tips on how to become a conscious consumer:',
    sources: [
      { name: '8 Ways to Reduce Waste', url: 'https://www.nature.org/en-us/about-us/where-we-work/united-states/delaware/stories-in-delaware/delaware-eight-ways-to-reduce-waste/' },
      { name: 'Alternatives to Household Consumables', url: 'https://greenecofriend.co.uk/sustainable-eco-friendly-alternatives/' }
    ]
  }
]);
</script>

<style scoped>
.climate-goals {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: auto;
  justify-content: center;
}

.goal {
  display: flex;
  align-items: start;
  gap: 40px;
}

.goal-number {
  font-size: 4rem;
  font-weight: bold;
  align-items: center;
  display: flex;
  height: 4rem;
  color: #1E555F;
  justify-content: center;
}

.goal-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.goal-text {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #1E555F;
}

.description {
  font-size: 1.2em;
  color: #FFA737;
}

.goal-sources {
  font-size: 0.9em;
  color: gray;
}

.goal-sources a {
  color: gray;
  text-decoration: none;
  cursor: pointer;
  background-color: transparent;
}

.goal-sources a:hover {
  text-decoration: underline;
  color: #1E555F;
}
</style>