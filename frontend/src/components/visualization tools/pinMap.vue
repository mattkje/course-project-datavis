<template>
  <div id="chartdivContainer_pinMap">
    <div id="chartdiv_pinMap">
      <div class="measurement-label"><span class="bold">{{ measurement }}</span></div>
    </div>
  </div>
</template>

<script>
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
  watch: {
    async url() {
      this.updateData(await this.fetchData(this.url));
      this.measurement = this.url.split(',')[0];
    }
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
    initializeMap: async function () {
      if (!document.getElementById("chartdiv_pinMap")._am5root) {

        const DataMap = await this.fetchData(this.url)

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

          var colorSet = am5.ColorSet.new(this.root_pinMap, {
            colors: [
              am5.color(0xBA7BA1), // North America
              am5.color(0xFFA737), // Europe
              am5.color(0x5BC0EB), // Asia
              am5.color(0x9BC53D), // Africa
              am5.color(0xA133FF), // South America
              am5.color(0x7BE0AD)  // Oceania
            ]
          });

          pointSeries.bullets.push((root, series, dataItem) => {
            var value = dataItem.dataContext.value;

            var container = am5.Container.new(root, {});
            var color = colorSet.next();
            var radius = 20 + value / 70 * 30;
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


          this.pointSeries = pointSeries;
          this.updateData(DataMap);

        });
      }
    },
    async fetchData(url) {
      const continentsList = ["Europe", "Asia", "Africa", "North America", "South America", "Oceania"];
      let co2Type = url.split(',')[1];
      if (co2Type == null) {
        co2Type = cumulative_co2;
      }
      let combinedData = {};

      for (let i = 0; i < continentsList.length; i++) {
        const response = await fetch(`${api}cumulative/${continentsList[i]}`);
        if (response.ok) {
          const data = await response.json();
          if (data.length > 0) {
            const lastEntry = data[data.length - 1];
            combinedData[continentsList[i]] = lastEntry[co2Type];
          }
        } else {
          console.error(`Failed to fetch data for ${continentsList[i]}`);
        }
      }

      // Calculate total cumulative CO2
      const totalCO2 = Object.values(combinedData).reduce((sum, value) => sum + value, 0);

      // Calculate percentage for each continent
      let percentageData = {};
      for (const [continent, value] of Object.entries(combinedData)) {
        percentageData[continent] = (value / totalCO2 * 100).toFixed(1);
      }

      return percentageData;
    },
    updateData(DataMap)
    {
      var data = [{
        "title": "North America",
        "latitude": 39.563353,
        "longitude": -99.316406,
        "width": 100,
        "height": 100,
        "value": DataMap["North America"]
      }, {
        "title": "Europe",
        "latitude": 38.896104,
        "longitude": 15.160156,
        "width": 50,
        "height": 100,
        "value": DataMap["Europe"]
      }, {
        "title": "Asia",
        "latitude": 35.212106,
        "longitude": 95.183594,
        "width": 80,
        "height": 80,
        "value": DataMap["Asia"]
      }, {
        "title": "Africa",
        "latitude": 11.081385,
        "longitude": 21.621094,
        "width": 50,
        "height": 50,
        "value": DataMap["Africa"]
      },
        {
          "title": "South America",
          "latitude": -14.179186,
          "longitude": -59.589844,
          "width": 50,
          "height": 50,
          "value": DataMap["South America"]
        },
        {
          "title": "Oceania",
          "latitude": -25.799891,
          "longitude": 134.472656,
          "width": 50,
          "height": 50,
          "value": DataMap["Oceania"]
        }];

      this.pointSeries.data.setAll(data.map(d => ({
        geometry: {type: "Point", coordinates: [d.longitude, d.latitude]},
        title: d.title,
        value: d.value
      })));
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

.measurement-label {
  position: absolute;
  bottom: 5%;
  right: 180px;
  color: #ffffff;
  padding: 5px;
  border-radius: 3px;
  font-family: Arial, sans-serif;
  font-size: 12px;
}

@media screen and (max-width: 1400px) {
  #chartdivContainer_pinMap {
    padding: 70px 0 40px 0;
  }
}
</style>