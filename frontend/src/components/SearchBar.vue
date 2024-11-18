<template>
    <div class="search-bar">
      <div class="search-input-wrapper">
        <font-awesome-icon :icon="['fas', 'magnifying-glass']" class="search-icon"/>
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for a Country or a Category..."
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
    </div>
    <div class="selected-items">
      <SelectedItem
          v-for="item in selectedItems"
          :key="item"
          :item="item"
          :onRemove="removeItem"
      />
    </div>
</template>

<script setup>
import {ref, computed} from 'vue';
import SelectedItem from './SelectedItem.vue';
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const searchQuery = ref('');
const isDisabled = ref(false);

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

const suggestions = ref([
  'Country', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo, Democratic Republic of the', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe', 'Year', 'ISO Code', 'Population', 'GDP', 'Cement CO2', 'Cement CO2 per Capita', 'Total CO2', 'CO2 Growth (Absolute)', 'CO2 Growth (%)', 'CO2 incl. Land-Use Change', 'CO2 Growth incl. Land-Use Change (Absolute)', 'CO2 Growth incl. Land-Use Change (%)', 'CO2 incl. Land-Use Change per Capita', 'CO2 incl. Land-Use Change per GDP', 'CO2 incl. Land-Use Change per Unit Energy', 'CO2 per Capita', 'CO2 per GDP', 'CO2 per Unit Energy', 'Coal CO2', 'Coal CO2 per Capita', 'Consumption CO2', 'Consumption CO2 per Capita', 'Consumption CO2 per GDP', 'Cumulative Cement CO2', 'Cumulative CO2', 'Cumulative CO2 incl. Land-Use Change', 'Cumulative Coal CO2', 'Cumulative Flaring CO2', 'Cumulative Gas CO2', 'Cumulative Land-Use Change CO2', 'Cumulative Oil CO2', 'Cumulative Other CO2', 'Energy per Capita', 'Energy per GDP', 'Flaring CO2', 'Flaring CO2 per Capita', 'Gas CO2', 'Gas CO2 per Capita', 'GHG (Excluding LULCF) per Capita', 'GHG per Capita', 'Land-Use Change CO2', 'Land-Use Change CO2 per Capita', 'Methane', 'Methane per Capita', 'Nitrous Oxide', 'Nitrous Oxide per Capita', 'Oil CO2', 'Oil CO2 per Capita', 'Other CO2 per Capita', 'Other Industry CO2', 'Primary Energy Consumption', 'Share of Global Cement CO2', 'Share of Global CO2', 'Share of Global CO2 incl. Land-Use Change', 'Share of Global Coal CO2', 'Share of Global Cumulative Cement CO2', 'Share of Global Cumulative CO2', 'Share of Global Cumulative CO2 incl. Land-Use Change', 'Share of Global Cumulative Coal CO2', 'Share of Global Cumulative Flaring CO2', 'Share of Global Cumulative Gas CO2', 'Share of Global Cumulative Land-Use Change CO2', 'Share of Global Cumulative Oil CO2', 'Share of Global Cumulative Other CO2', 'Share of Global Flaring CO2', 'Share of Global Gas CO2', 'Share of Global Land-Use Change CO2', 'Share of Global Oil CO2', 'Share of Global Other CO2', 'Share of Temperature Change from GHG', 'Temperature Change from CH₄', 'Temperature Change from CO2', 'Temperature Change from GHG', 'Temperature Change from N2O', 'Total GHG', 'Total GHG (Excluding LULCF)', 'Trade CO2', 'Trade CO2 Share'
]);
</script>

<style scoped>
.search-bar {
  position: relative;
  display: flex;
  flex-direction: row;
  width: 20vw;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid black;
  border-radius: 15px;
  background: white;
  width: 20vw;
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
  top: 100%;
  left: 0;
  width: 20vw;
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 150px;
  overflow-y: auto;
  background: white;
  border-radius: 0 0 15px 15px; /* Match border radius */
  z-index: 1;
}

.suggestions li {
  cursor: pointer;
  color: black;
}

.suggestions li {
  padding: 8px;
  cursor: pointer;
}

.suggestions li:hover {
  background-color: #03DAC6;
  color: white;
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
  margin-left: 5px;
  display: flex;
  flex-wrap: nowrap;
  gap: 5px;
}
</style>