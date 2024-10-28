<template>
  <div class="search-bar">
    <div class="search-input-wrapper">
      <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon" />
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Search..."
      />
    </div>
    <ul v-if="filteredSuggestions.length" class="suggestions">
      <li
          v-for="suggestion in filteredSuggestions"
          :key="suggestion"
          @click="selectSuggestion(suggestion)"
      >
        {{ suggestion }}
      </li>
    </ul>
    <div class="selected-items">
      <SelectedItem
          v-for="item in selectedItems"
          :key="item"
          :item="item"
          :onRemove="removeItem"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import SelectedItem from './SelectedItem.vue';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const searchQuery = ref('');
const isDisabled = ref(false);
const suggestions = ref([
  // ... your suggestions array
]);

const selectedItems = ref([]);

const filteredSuggestions = computed(() => {
  if (!searchQuery.value) return [];
  return suggestions.value.filter(item =>
      item.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const selectSuggestion = (suggestion) => {
  if (!selectedItems.value.includes(suggestion)) {
    selectedItems.value.push(suggestion);
  }
  searchQuery.value = '';
};

const removeItem = (item) => {
  selectedItems.value = selectedItems.value.filter(i => i !== item);
};
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 300px;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid black;
  border-radius: 15px;
  background: white;
}

.search-icon {
  margin-right: 8px;
  color: #888;
}

input {
  width: 100%;
  border: none;
  outline: none;
}

.suggestions {
  position: absolute;
  width: 100%;
  background: white;
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 150px;
  overflow-y: auto;
}

.suggestions li {
  padding: 8px;
  cursor: pointer;
}

.suggestions li:hover {
  background: #f0f0f0;
}

.suggestions::-webkit-scrollbar {
  width: 8px;
}

.suggestions::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.suggestions::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.selected-items {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
}
</style>