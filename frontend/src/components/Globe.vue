<template>
  <div id="chartdivContainer_globe">
    <div id="chartdiv_globe"></div>
    <CountryInfoBox ref="countryInfoBox"/>
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_worldLow from "@amcharts/amcharts5-geodata/worldLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {ref, onMounted} from 'vue';
import CountryInfoBox from './CountryInfoBox.vue'; // Import the CountryInfoBox component

let chart;

export function selectCountryByLongLat(longitude, latitude) {
  if (chart) {
    if (longitude > 180 || longitude < -180 || latitude > 90 || latitude < -90) {
      longitude = -101.25;
      latitude = 38.52;
    }
    chart.animate({
      key: "rotationX",
      to: -longitude,
      duration: 1500,
      easing: am5.ease.inOut(am5.ease.cubic),
    });
    chart.animate({
      key: "rotationY",
      to: -latitude,
      duration: 1500,
      easing: am5.ease.inOut(am5.ease.cubic),
    });
  } else {
    console.error("Chart is not initialized");
  }
}

export default {
  name: "Globe",
  components: {
    CountryInfoBox
  },
  setup() {
    const countryInfoBox = ref(null); // Create a ref for the CountryInfoBox component

    onMounted(() => {
      function selectCountryInfo(name, id) {
        if (countryInfoBox.value) {
          document.getElementById("chartdiv_globe").style.width = "75%";
          fetch('http://127.0.0.1:5000/country_data/' + name)
              .then(response => response.json())
              .then(data => {
                const countryData = data[0];
                countryInfoBox.value.updateCountryInfo(name, countryData["Population"], countryData["Land Area(Km2)"],
                    countryData["Capital/Major City"], id);
              })
              .catch(error => {
                console.error('There was an error!', error);
                countryInfoBox.value.updateCountryInfo(name, "N/A", "N/A", "N/A", id);
              });
        }
      }

      am5.ready(() => {
        // Create root element
        var rootGlobe = am5.Root.new("chartdiv_globe");

        // Set themes
        rootGlobe.setThemes([am5themes_Animated.new(rootGlobe)]);

        // Create the map chart
        chart = rootGlobe.container.children.push(
            am5map.MapChart.new(rootGlobe, {
              panX: "rotateX",
              panY: "rotateY",
              projection: am5map.geoOrthographic(),
              centerX: am5.percent(-12.5),
              centerY: am5.percent(-12.5),
              paddingBottom: 20,
              paddingTop: 20,
              paddingLeft: 20,
              paddingRight: 20,
              scale: 0.8
            })
        );

        // Create main polygon series for countries
        var polygonSeries = chart.series.push(
            am5map.MapPolygonSeries.new(rootGlobe, {
              geoJSON: am5geodata_worldLow,
            })
        );

        polygonSeries.mapPolygons.template.setAll({
          tooltipText: "{name}",
          toggleKey: "active",
          interactive: true,
        });

        polygonSeries.mapPolygons.template.states.create("hover", {
          fill: rootGlobe.interfaceColors.get("primaryButtonHover"),
        });

        polygonSeries.mapPolygons.template.states.create("active", {
          fill: rootGlobe.interfaceColors.get("primaryButtonHover"),
        });

        // Create series for background fill
        var backgroundSeries = chart.series.push(
            am5map.MapPolygonSeries.new(rootGlobe, {})
        );
        backgroundSeries.mapPolygons.template.setAll({
          fill: rootGlobe.interfaceColors.get("alternativeBackground"),
          fillOpacity: 0.1,
          strokeOpacity: 0,
        });
        backgroundSeries.data.push({
          geometry: am5map.getGeoRectangle(90, 180, -90, -180),
        });


        // Set up events
        var previousPolygon;

        polygonSeries.mapPolygons.template.on("active", function (active, target) {
          if (previousPolygon && previousPolygon != target) {
            previousPolygon.set("active", false);
          }
          if (target.get("active")) {
            selectCountry(target.dataItem.get("id"), target.dataItem.dataContext.name);
          }
          previousPolygon = target;
        });

        polygonSeries.mapPolygons.template.setAll({
          fill: am5.color(0x0ffffff),
          stroke: am5.color(0x0999999),
          strokeWidth: 1,
        });
        polygonSeries.mapPolygons.template.states.create("hover", {
          fill: am5.color(0x09AD9E)
        });
        polygonSeries.mapPolygons.template.states.create("focused", {
          fill: am5.color(0x09AD9E)
        });
        polygonSeries.mapPolygons.template.states.create("active", {
          fill: am5.color(0x03dac6)
        });

        function selectCountry(id, name) {
          var dataItem = polygonSeries.getDataItemById(id);
          var target = dataItem.get("mapPolygon");
          if (target) {
            var centroid = target.geoCentroid();
            if (centroid) {
              chart.animate({
                key: "rotationX",
                to: -centroid.longitude,
                duration: 1500,
                easing: am5.ease.inOut(am5.ease.cubic),
              });
              chart.animate({
                key: "rotationY",
                to: -centroid.latitude,
                duration: 1500,
                easing: am5.ease.inOut(am5.ease.cubic),
              });
            }
          }
          selectCountryInfo(name, id);
        }

        // Make stuff animate on load
        chart.appear(1000, 100);
      });
    });

    return {countryInfoBox};
  },
};
</script>

<style>
#chartdiv_globe {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  left: 0;
  transition: width 0.5s ease-in-out;
}

#chartdivContainer_globe {
  position: relative;
  justify-content: center;
  align-items: start;
  width: 100%;
  height: 90vh;
  padding: 60px 0 60px 0;
}
</style>
