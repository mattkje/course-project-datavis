<template>
  <div id="chartdivContainer">
    <div id="chartdiv1"></div>
  </div>
</template>

<script setup>
import {onMounted} from 'vue';
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_continentsLow from "@amcharts/amcharts5-geodata/continentsLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

const emit = defineEmits(['continent-clicked']);

onMounted(() => {
  am5.ready(function () {
    // Create root and chart
    var root1 = am5.Root.new("chartdiv1");

    // Set themes
    root1.setThemes([
      am5themes_Animated.new(root1)
    ]);

    const chart = root1.container.children.push(
        am5map.MapChart.new(root1, {
          panX: "rotateX",
          projection: am5map.geoNaturalEarth1()
        })
    );

    // Create polygon series
    var polygonSeries = chart.series.push(
        am5map.MapPolygonSeries.new(root1, {
          geoJSON: am5geodata_continentsLow,
          exclude: ["antarctica"]
        })
    );

    polygonSeries.mapPolygons.template.setAll({
      tooltipText: "{name}",
      interactive: true,
      templateField: "settings"
    });

    polygonSeries.mapPolygons.template.states.create("hover", {
      fill: am5.color(0x677935)
    });

    polygonSeries.mapPolygons.template.events.on("click", function(ev) {
      const data = ev.target.dataItem.dataContext;
      emit('continent-clicked', data.name);
    });

    var colors = am5.ColorSet.new(root1, {
      colors: [
        am5.color(0xFFA737), // Europe
        am5.color(0x5BC0EB), // Asia
        am5.color(0x9BC53D), // Africa
        am5.color(0xBA7BA1), // North America
        am5.color(0xA133FF), // South America
        am5.color(0x7BE0AD)  // Oceania
      ]
    });

    polygonSeries.data.setAll([{
      id: "europe",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }, {
      id: "asia",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }, {
      id: "africa",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }, {
      id: "northAmerica",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }, {
      id: "southAmerica",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }, {
      id: "oceania",
      settings: {
        fill: colors.next(),
        fillPattern: am5.LinePattern.new(root1, {
          color: am5.color(0xffffff),
          rotation: 45,
          strokeWidth: 1
        })
      }
    }]);
  }); // end am5.ready()
});
</script>

<style scoped>
#chartdiv1 {
  width: 100%;
  height: 500px;
}

#chartdivContainer {
  position: relative;
  justify-content: center;
  width: 100%;
  height: 620px;
  padding: 60px 0 60px 0;
}

</style>