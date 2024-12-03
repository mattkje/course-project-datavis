<template>
  <div id="chartdiv"></div>
</template>

<script setup>
import { onMounted } from 'vue';
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_continentsLow from "@amcharts/amcharts5-geodata/continentsLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

onMounted(() => {
  if (!document.getElementById("chartdiv")._am5root) {
    am5.ready(function() {
      var root = am5.Root.new("chartdiv");
      document.getElementById("chartdiv")._am5root = root;

      root.setThemes([
        am5themes_Animated.new(root)
      ]);

      var map = root.container.children.push(
        am5map.MapChart.new(root, {
          panX: "none",
          projection: am5map.geoNaturalEarth1()
        })
      );

      var polygonSeries = map.series.push(
        am5map.MapPolygonSeries.new(root, {
          geoJSON: am5geodata_continentsLow,
          exclude: ["antarctica"],
          fill: am5.color(0xbbbbbb)
        })
      );

      let pointSeries = map.series.push(
        am5map.MapPointSeries.new(root, {})
      );

      var colorSet = am5.ColorSet.new(root, { step: 2 });

      pointSeries.bullets.push(function(root, series, dataItem) {
        var value = dataItem.dataContext.value;

        var container = am5.Container.new(root, {});
        var color = colorSet.next();
        var radius = 15 + value / 20 * 20;
        var circle = container.children.push(am5.Circle.new(root, {
          radius: radius,
          fill: color,
          dy: -radius * 2
        }));

        var pole = container.children.push(am5.Line.new(root, {
          stroke: color,
          height: -40,
          strokeGradient: am5.LinearGradient.new(root, {
            stops: [
              { opacity: 1 },
              { opacity: 1 },
              { opacity: 0 }
            ]
          })
        }));

        let label = container.children.push(am5.Label.new(root, {
          text: value + "%",
          fill: am5.color(0xffffff),
          fontWeight: "400",
          centerX: am5.p50,
          centerY: am5.p50,
          dy: -radius * 2
        }));

        let titleLabel = container.children.push(am5.Label.new(root, {
          text: dataItem.dataContext.title,
          fill: color,
          fontWeight: "500",
          fontSize: "1em",
          centerY: am5.p50,
          dy: -radius * 2,
          dx: radius
        }));

        return am5.Bullet.new(root, {
          sprite: container
        });
      });

      var data = [{
        "title": "United States",
        "latitude": 39.563353,
        "longitude": -99.316406,
        "width": 100,
        "height": 100,
        "value": 12
      }, {
        "title": "European Union",
        "latitude": 50.896104,
        "longitude": 19.160156,
        "width": 50,
        "height": 50,
        "value": 15
      }, {
        "title": "Asia",
        "latitude": 47.212106,
        "longitude": 103.183594,
        "width": 80,
        "height": 80,
        "value": 8
      }, {
        "title": "Africa",
        "latitude": 11.081385,
        "longitude": 21.621094,
        "width": 50,
        "height": 50,
        "value": 5
      }];

      for (var i = 0; i < data.length; i++) {
        var d = data[i];
        pointSeries.data.push({
          geometry: { type: "Point", coordinates: [d.longitude, d.latitude] },
          title: d.title,
          value: d.value
        });
      }
    });
  }
});
</script>

<style scoped>
#chartdiv {
  width: 100%;
  height: 500px;
}
</style>