<template>
  <div id="chartdiv"></div>
  <CountryInfoBox ref="countryInfoBox" /> <!-- Reference to CountryInfoBox -->
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_worldLow from "@amcharts/amcharts5-geodata/worldLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import { ref, onMounted } from 'vue';
import CountryInfoBox from './CountryInfoBox.vue'; // Import the CountryInfoBox component

let chart;

export function selectCountryByLongLat(longitude, latitude) {
  if (chart) {
    if(longitude > 180 || longitude < -180 || latitude > 90 || latitude < -90) {
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
      function selectCountryInfo(name) {
        if (countryInfoBox.value) {

          countryInfoBox.value.updateCountryInfo(name, "10 million", "500,000", "Dummy Capital");
        }
      }

      am5.ready(() => {
        // Create root element
        var root = am5.Root.new("chartdiv");

        // Set themes
        root.setThemes([am5themes_Animated.new(root)]);

        // Create the map chart
chart = root.container.children.push(
  am5map.MapChart.new(root, {
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
            am5map.MapPolygonSeries.new(root, {
              geoJSON: am5geodata_worldLow,
            })
        );

        polygonSeries.mapPolygons.template.setAll({
          tooltipText: "{name}",
          toggleKey: "active",
          interactive: true,
        });

        polygonSeries.mapPolygons.template.states.create("hover", {
          fill: root.interfaceColors.get("primaryButtonHover"),
        });

        polygonSeries.mapPolygons.template.states.create("active", {
          fill: root.interfaceColors.get("primaryButtonHover"),
        });

        // Create series for background fill
        var backgroundSeries = chart.series.push(
            am5map.MapPolygonSeries.new(root, {})
        );
        backgroundSeries.mapPolygons.template.setAll({
          fill: root.interfaceColors.get("alternativeBackground"),
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

        function selectCountry(id,name) {
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
          selectCountryInfo(name);
        }

        // Make stuff animate on load
        chart.appear(1000, 100);
      });
    });

    return { countryInfoBox };
  },
};
</script>

<style>
#chartdiv {
  width: 100vw;
  height: calc(100vh - 70px);
  max-width: 100%;
  max-height: 100%;
  position: absolute;
  top: 70px;
  left: 0;
}
</style>
