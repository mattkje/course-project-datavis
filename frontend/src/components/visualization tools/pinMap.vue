<template>
  <div id="chartdivContainer_pinMap">
    <div id="chartdiv_pinMap">
      <div class="measurement-label">Measured in <span class="bold">{{ measurement }}</span></div>
    </div>
  </div>
</template>

<script>
import {onMounted} from 'vue';
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_continentsLow from "@amcharts/amcharts5-geodata/continentsLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

const api = "http://127.0.0.1:5000/";

export default {
  name: "PinMapComponent",
  props: {
    url: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      measurement: this.url.split(',')[0],
    };
  },
  mounted() {
    this.initializeMap();
  },
  methods: {
    async initializeMap() {
      if (!document.getElementById("chartdiv_pinMap")._am5root) {

        this.fetchData(this.url).then(data => {
          console.log(data);
        });

        am5.ready(() => {
          this.root_pinMap = am5.Root.new("chartdiv_pinMap");
          document.getElementById("chartdiv_pinMap")._am5root = this.root_pinMap;

          this.root_pinMap.setThemes([
            am5themes_Animated.new(this.root_pinMap)
          ]);

          var map = this.root_pinMap.container.children.push(
              am5map.MapChart.new(this.root_pinMap, {
                panX: "none",
                panY: "none",
                projection: am5map.geoNaturalEarth1(),
                maxZoomLevel: 1,
              })
          );

          var polygonSeries = map.series.push(
              am5map.MapPolygonSeries.new(this.root_pinMap, {
                geoJSON: am5geodata_continentsLow,
                exclude: ["antarctica"],
                fill: am5.color(0xFFFFFF),
              })
          );

          let pointSeries = map.series.push(
              am5map.MapPointSeries.new(this.root_pinMap, {})
          );

          var colorSet = am5.ColorSet.new(this.root_pinMap, {step: 2});

          pointSeries.bullets.push((root, series, dataItem) => {
            var value = dataItem.dataContext.value;

            var container = am5.Container.new(root, {});
            var color = colorSet.next();
            var radius = 15 + value / 30 * 15;
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
                  {opacity: 1},
                  {opacity: 1},
                  {opacity: 0}
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
            "title": "North America",
            "latitude": 39.563353,
            "longitude": -99.316406,
            "width": 100,
            "height": 100,
            "value": 12
          }, {
            "title": "Europe",
            "latitude": 38.896104,
            "longitude": 15.160156,
            "width": 50,
            "height": 100,
            "value": 50
          }, {
            "title": "Asia",
            "latitude": 35.212106,
            "longitude": 95.183594,
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
          },
            {
              "title": "South America",
              "latitude": -14.179186,
              "longitude": -59.589844,
              "width": 50,
              "height": 50,
              "value": 25
            },
            {
              "title": "Oceania",
              "latitude": -25.799891,
              "longitude": 134.472656,
              "width": 50,
              "height": 50,
              "value": 20
            }
          ];

          for (var i = 0; i < data.length; i++) {
            var d = data[i];
            pointSeries.data.push({
              geometry: {type: "Point", coordinates: [d.longitude, d.latitude]},
              title: d.title,
              value: d.value
            });
          }
        });
      }
    },
    async fetchData(url) {
      const continentsList = ["EU", "AS", "AF", "NA", "SA", "OC"];
      const temp = url.split(',')[1];
      let combinedData = [];

      for (let i = 0; i < continentsList.length; i++) {
        const response = await fetch(`${api}continent_data/${continentsList[i]}/${temp}`);
        if (response.ok) {
          const data = await response.json();
          combinedData = combinedData.concat(data);
        } else {
          console.error(`Failed to fetch data for ${continentsList[i]}`);
        }
      }

      return combinedData;
    }
  },
  beforeDestroy() {
    if (this.root_pinMap) {
      this.root_pinMap.dispose();
    }
  }
};
</script>

<style scoped>
#chartdiv_pinMap {
  width: 100%;
  height: 500px;
}

#chartdivContainer_pinMap {
  position: relative;
  justify-content: center;
  width: 100%;
  height: 700px;
  padding: 140px 0 60px 0;
}
</style>