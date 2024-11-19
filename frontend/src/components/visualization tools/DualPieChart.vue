<template>
  <div id="chartdiv" ref="chartdiv">
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5percent from "@amcharts/amcharts5/percent";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {prettyNames} from "@/components/dictionaries/prettyNames.js";

const api = "http://127.0.0.1:5000/";

export default {
  name: "PieChartComponent",
  props: {
    url: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      measurement: this.url.split(',')[0]
    };
  },
  mounted() {
    let root = am5.Root.new(this.$refs.chartdiv);

    root.setThemes([am5themes_Animated.new(root)]);

    root.container.set("layout", root.verticalLayout);

    this.fetchData(this.url).then(data => {
      console.log(data);
      const transformData = (series) => {
        return Object.keys(series)
            .filter(key => !['co2', 'co2_including_luc', 'country', 'year', 'land_use_change_co2'].includes(key))
            .map(key => ({
              category: key,
              value: series[key]
            }));
      };

      const series1Data = transformData(data.series1);
      const series2Data = transformData(data.series2);

      let chartContainer = root.container.children.push(am5.Container.new(root, {
        layout: root.horizontalLayout,
        width: am5.p100,
        height: am5.p100
      }));

      let chart = chartContainer.children.push(
          am5percent.PieChart.new(root, {
            endAngle: 270,
            innerRadius: am5.percent(60)
          })
      );

      let series = chart.series.push(
          am5percent.PieSeries.new(root, {
            valueField: "value",
            categoryField: "category",
            endAngle: 270,
            alignLabels: false
          })
      );

      series.children.push(am5.Label.new(root, {
        centerX: am5.percent(50),
        centerY: am5.percent(50),
        text: data.series1.year,
        populateText: true,
        fontSize: "1.5em"
      }));

      series.slices.template.setAll({
        cornerRadius: 8
      });

      series.states.create("hidden", {
        endAngle: -90
      });

      series.labels.template.setAll({
        text: "",
      });


      let chart2 = chartContainer.children.push(
          am5percent.PieChart.new(root, {
            endAngle: 270,
            innerRadius: am5.percent(60)
          })
      );

      let series2 = chart2.series.push(
          am5percent.PieSeries.new(root, {
            valueField: "value",
            categoryField: "category",
            endAngle: 270,
            alignLabels: false,
            tooltip: am5.Tooltip.new(root, {
              pointerOrientation: "horizontal",
              labelText: `{category}: {valuePercentTotal.formatNumber("#.0")}%`,
            })
          })
      );

      series2.children.push(am5.Label.new(root, {
        centerX: am5.percent(50),
        centerY: am5.percent(50),
        text: data.series2.year,
        populateText: true,
        fontSize: "1.5em"
      }));

      series2.slices.template.setAll({
        cornerRadius: 8
      });

      series2.states.create("hidden", {
        endAngle: -90
      });

      series2.labels.template.setAll({
        text: "",
      });

      function getSlice(dataItem, series) {
        var otherSlice;
        am5.array.each(series.dataItems, function(di) {
          if (di.get("category") === dataItem.get("category")) {
            otherSlice = di.get("slice");
          }
        });

        return otherSlice;
      }

      series.slices.template.on("active", function(active, target) {
        let slice = target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series2);

        if (otherSlice) {
          otherSlice.set("active", active);
        }
      });

      series.slices.template.events.on("pointerover", function(ev) {
        let slice = ev.target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series2);

        if (otherSlice) {
          otherSlice.hover();
        }
      });

      series.slices.template.events.on("pointerout", function(ev) {
        let slice = ev.target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series2);

        if (otherSlice) {
          otherSlice.unhover();
        }
      });

      series2.slices.template.events.on("pointerover", function(ev) {
        let slice = ev.target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series);

        if (otherSlice) {
          otherSlice.hover();
        }
      });

      series2.slices.template.events.on("pointerout", function(ev) {
        let slice = ev.target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series);

        if (otherSlice) {
          otherSlice.unhover();
        }
      });

      series2.slices.template.on("active", function(active, target) {
        let slice = target;
        let dataItem = slice.dataItem;
        let otherSlice = getSlice(dataItem, series);

        if (otherSlice) {
          otherSlice.set("active", active);
        }
      });

      series.data.setAll(series1Data);
      series2.data.setAll(series2Data);
    });
  },
  methods: {
    async fetchData(url, start_year = 2000, end_year = 2021) {
      const response = await fetch(`${api}co2/${url}/${start_year}/${end_year}`);
      if (response.ok) {
        const data = await response.json();
        return {
          series1: data[0],
          series2: data[data.length - 1]
        };
      } else {
        console.error("Failed to fetch data");
        return {
          series1: [],
          series2: []
        };
      }
    }
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
};
</script>

<style scoped>
#chartdiv {
  width: 40%;
  height: 500px;
  margin-top: 650px;
  margin-left: 70px;
}

.measurement-label {
  position: absolute;
  bottom: 10%;
  right: 180px;
  color: #000000;
  padding: 5px;
  border-radius: 3px;
  font-family: Arial, sans-serif;
  font-size: 12px;
}

.bold {
  font-weight: bold;
}
</style>