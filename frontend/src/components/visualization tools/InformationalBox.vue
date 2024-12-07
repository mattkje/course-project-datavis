<script setup lang="ts">
import {ref} from 'vue';

const selectedTab = ref(1);

const tabs = [
  {
    id: 1,
    name: 'Britain - The First Superpower',
    content: 'In the early 1800s, Britain led the world in climate pollution due to its role in the Industrial Revolution. Its abundant coal reserves powered steam engines and factories, driving rapid industrialization and urbanization. This led to dense factory concentrations, emitting vast amounts of carbon dioxide and other pollutants. With no environmental regulations, industries operated freely, causing severe air pollution and deforestation. Britain\'s dominance in global trade also spread industrial pollution worldwide, making it a key contributor to early anthropogenic climate change.',
    largeImageURL: 'https://upload.wikimedia.org/wikipedia/commons/5/5e/Hand-loom_weaving.jpg',
    smallImageURL1: 'https://upload.wikimedia.org/wikipedia/commons/f/f3/Winchester_High_Street_Mudie_1853.jpg',
    smallImageURL2: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Dore_London.jpg/220px-Dore_London.jpg',
  },
  {
    id: 2,
    name: 'Middle East - Oil Rush',
    content: 'The discovery of oil in the Middle East in the early 20th century transformed the region into a global economic powerhouse. Countries like Saudi Arabia, Iran, and Iraq quickly became major players in the global energy market, as their vast oil reserves were tapped to meet the world’s growing demand for fuel. This resource brought immense wealth, reshaping the region’s economies and elevating the political influence of oil-rich nations. Western powers and multinational corporations heavily invested in Middle Eastern oil, further accelerating its extraction and export. The oil boom not only enriched the region but also cemented its central role in global energy and politics.',
    largeImageURL: 'https://cdn.punchng.com/wp-content/uploads/2023/06/14111510/01-gas-1.jpg',
    smallImageURL1: 'https://www.arabnews.com/sites/default/files/styles/n_670_395/public/2017/03/07/867641-1586784408.jpg?itok=BUm_0SVy',
    smallImageURL2: 'https://upload.wikimedia.org/wikipedia/commons/c/c4/Dammam_No._7_on_March_4%2C_1938.jpg',
  },
  {
    id: 3,
    name: 'USA - Co2 Domination',
    content: 'The United States became an emissions superpower through decades of industrialization, urban growth, and heavy reliance on fossil fuels. Starting in the late 19th century, industries like steel, manufacturing, and automotive production, powered by coal, oil, and gas, drove massive carbon emissions. The post-World War II economic boom and suburbanization further increased energy use, with car culture playing a major role. As one of the world’s largest economies, the U.S. has long been a top emitter, with high per capita energy consumption and a focus on economic growth. Despite progress in renewables, its industrial base and transportation systems remain major sources of emissions.',
    largeImageURL: 'https://imageio.forbes.com/blogs-images/jamesconca/files/2015/04/PaloVerde-nuclear.jpg?format=jpg&height=600&width=1200&fit=bounds',
    smallImageURL1: 'https://i.insider.com/629faf1b7498590019651323?width=700',
    smallImageURL2: 'https://sitescdn.wearevennture.co.uk/public/nes-fircroft/mediahub/austrian-national-library-exgfrvfjk4m-unsplash-910332978e534cfe9c3028b2dc1087ac.jpg',
  },
  {
    id: 4, name: 'China - The Worlds Factory', content: '\n' +
        'China became the world’s factory as global businesses capitalized on its low labor costs, abundant workforce, and favorable manufacturing policies. Starting in the late 20th century, foreign companies outsourced production to China, taking advantage of its rapidly developing infrastructure and government incentives. This shift allowed multinational corporations to reduce costs while accessing China’s massive export capabilities. Over time, China built a vast industrial base, producing everything from electronics to textiles at unprecedented scales. The global demand for cheap goods fueled this growth. However, this economic model also led to significant environmental and social challenges, including high carbon emissions and labor issues.',
    largeImageURL: 'https://image.cnbcfm.com/api/v1/image/104859991-Foxconn_factory_.jpg?v=1710508838&w=1920&h=1080',
    smallImageURL1: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9hxpUGBGsk1JgH1kvCvWbEp5DTDr1xbt28g&s',
    smallImageURL2: 'https://chinatownatlas.org/wp-content/uploads/2014/06/Garment-Factory-1024x794.jpg',
  },
];

const selectTab = (tabId: number) => {
  selectedTab.value = tabId;
};

defineExpose({selectTab});
</script>

<template>
  <div class="informational-box">
    <div class="tabs">
      <div
          v-for="tab in tabs"
          :key="tab.id"
          :class="['tab', { active: tab.id === selectedTab, ['tab-' + tab.id]: true }]"
          @click="selectTab(tab.id)"
      >
        {{ tab.name }}
      </div>
    </div>
    <div class="content">
      <div class="text-box">
        <h3>{{ tabs.find(tab => tab.id === selectedTab)?.name ?? 'Unknown Tab' }}</h3>
        <p> {{ tabs.find(tab => tab.id === selectedTab)?.content ?? 'Unknown Tab' }}</p>
      </div>
      <div class="image-gallery">
        <div
            v-if="tabs.filter(tab => tab.id === selectedTab)[0]?.largeImageURL"
            class="main-image"
            :style="{ backgroundImage: 'url(' + tabs.find(tab => tab.id === selectedTab).largeImageURL + ')' }">
        </div>
        <div
            v-if="tabs.filter(tab => tab.id === selectedTab)[0]?.smallImageURL1"
            class="sub-image"
            :style="{ backgroundImage: 'url(' + tabs.filter(tab => tab.id === selectedTab)[0].smallImageURL1 + ')' }">
        </div>
        <div
            v-if="tabs.filter(tab => tab.id === selectedTab)[0]?.smallImageURL2"
            class="sub-image"
            :style="{ backgroundImage: 'url(' + tabs.find(tab => tab.id === selectedTab).smallImageURL2 + ')' }">
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

p {
  font-weight: 100;
  font-family: "Corbel Light", serif;
  font-size: 20px;
}

h3 {
  justify-self: left;
  font-size: 1.6rem;
  font-weight: 900;
  color: #FFA737;
  margin: 0;
}

.informational-box {
  display: flex;
  flex-direction: column;
  background-color: #1E555F;
  min-height: 700px;
  width: 65%;
  position: relative;
  margin: auto;
  border-radius: 20px;
}

.informational-box::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border-style: none dotted dotted dotted;
  border-width: 0 2px 2px 2px;
  border-color: #FFA737;
  pointer-events: none;
  border-radius: 18px;
}

.tabs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.tab {
  width: 100%;
  height: 100%;
  padding: 10px 20px;
  background-color: #1E555F;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: bold;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border-bottom: 2px dotted #FFA737;
}

.tab-1 {
  border-top-left-radius: 20px;
}

.tab-4 {
  border-top-right-radius: 20px;
}

.tab.active {
  background-color: #346972;
}

.tab:hover {
  background-color: #346972;
}

.content {
  display: flex;
  gap: 20px;
  padding: 30px;
  height: 100%;
}

.text-box {
  flex: 2;
  background-color: #1E555F;
  color: white;
  border-radius: 20px;
  padding: 20px 40px;
  position: relative;
  font-size: 1.4rem;
  font-weight: 400;
  border: 2px dotted #FFA737;
  min-height: 100%;

}

.image-gallery {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 10px;
  flex: 3;
}

.main-image {
  grid-column: 1 / 3;
  grid-row: 1 / 2;
  background-color: #4e90a4;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  background-size: cover;
  background-position: center;
}

.sub-image {
  background-color: #4e90a4;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  background-size: cover;
  background-position: center;
}

@media (max-width: 1400px) {
  .informational-box {
    width: 90%;
  }

  .content {
    flex-direction: column;
    gap: 20px;
    height: 100%;
  }

  .image-gallery {
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr;
    min-height: 380px;
  }

  .main-image {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
  }

  .sub-image {
    grid-column: 2 / 3;
    grid-row: 1 / 2;
  }

  .sub-image:nth-child(3) {
    grid-column: 3 / 4;
    grid-row: 1 / 2;
  }
}
</style>