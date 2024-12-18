<template>
  <div id="chartdiv" ref="chartdiv">
<!--<div class="measurement-label" v-if="!isContinent">Measured in <span class="bold">{{ measurement }}</span></div>-->
  </div>
</template>

<script>
import { prettyNames } from "@/components/dictionaries/prettyNames.js";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy.js";
import {color} from "@amcharts/amcharts5";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
const api = "http://127.0.0.1:5000/";

export default {
  name: "AmChartComponent",
  props: {
    url: {
      type: String,
      required: true
    },
  isContinent: {
    type: Boolean,
    required: false,
    default: false,
  }
  },
  data() {
    return {
      measurement : this.url.split(',')[0],
    };
  },
  mounted() {
    let root = am5.Root.new(this.$refs.chartdiv);

    const myTheme = am5.Theme.new(root);

    // Custom theme rules to change text color
    myTheme.rule("AxisLabel").setAll({ fill: am5.color(0x000000) });
    myTheme.rule("Tooltip").setAll({ labelText: { fill: am5.color(0xFFFFFF) } });
    myTheme.rule("LegendLabel").setAll({ labelText: { fill: am5.color(0x000000) } });
    myTheme.rule("LegendValueLabel").setAll({ labelText: { fill: am5.color(0x000000) } });

    root.setThemes([am5themes_Animated.new(root), myTheme]);

    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      maxTooltipDistance: 0,
      pinchZoomX: true
    }));

    this.fetchData(this.url).then(data => {
      data.forEach(item => {
        item.year = new Date(item.year, 0, 1).getTime();
      });

      const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0.2,
        baseInterval: {timeUnit: "year", count: 1},
        renderer: am5xy.AxisRendererX.new(root, {minorGridEnabled: true}),
        tooltip: am5.Tooltip.new(root, {})
      }));

      const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      xAxis.get("renderer").labels.template.setAll({fill: am5.color(0xFFFFFF)}); // Red color for x-axis labels
      yAxis.get("renderer").labels.template.setAll({fill: am5.color(0xFFFFFF)}); // Blue color for y-axis labels

      const fields = Object.keys(data[0]).filter(key => key !== "year" && key !== "country");
      const measurement = this.url.split(',')[0];
      fields.forEach(field => {
        // Split the data into two parts
        const dataBefore2022 = data.filter(item => new Date(item.year).getFullYear() <= 2022);
        const dataAfter2022 = data.filter(item => new Date(item.year).getFullYear() >= 2022);

        // Create the first series (before 2022)
        const seriesBefore2022 = chart.series.push(am5xy.LineSeries.new(root, {
          name: `${prettyNames[field]}`,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          valueXField: "year",
          legendValueText: `{${field}}`,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            labelText: `${prettyNames[field]}: {${field}} ${measurement}`,
          })
        }));

        seriesBefore2022.data.setAll(dataBefore2022);
        seriesBefore2022.strokes.template.setAll({
          strokeWidth: 3,
        });

        // Create the second series (after 2022)
        const seriesAfter2022 = chart.series.push(am5xy.LineSeries.new(root, {
          name: `${prettyNames[field]} (After 2022)`,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          valueXField: "year",
          legendValueText: `{${field}}`,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            labelText: `${prettyNames[field]} (After 2022): {${field}} ${measurement}`,
          })
        }));

        seriesAfter2022.data.setAll(dataAfter2022);
        seriesAfter2022.strokes.template.setAll({
          strokeWidth: 3,
          strokeDasharray: [5, 5], // Example dashed line style
        });
      });

      const cursor = chart.set("cursor", am5xy.XYCursor.new(root, {behavior: "none"}));
      cursor.lineY.set("visible", false);

      const legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
        width: 300,
        paddingLeft: 15,
        height: am5.percent(100),
      }));

      legend.itemContainers.template.events.on("pointerover", function (e) {
        const itemContainer = e.target;
        const series = itemContainer.dataItem.dataContext;
        chart.series.each(function (chartSeries) {
          if (chartSeries !== series) {
            chartSeries.strokes.template.setAll({
              strokeOpacity: 0.15,
              stroke: am5.color(0x000000),
            });
          } else {
            chartSeries.strokes.template.setAll({strokeWidth: 3});
          }
        });
      });

      legend.itemContainers.template.events.on("pointerout", function (e) {
        const itemContainer = e.target;
        const series = itemContainer.dataItem.dataContext;
        chart.series.each(function (chartSeries) {
          chartSeries.strokes.template.setAll({
            strokeOpacity: 1,
            strokeWidth: 3,
            stroke: chartSeries.get("fill"),
          });
        });
      });

      legend.labels.template.setAll({fill: am5.color(0xFFFFFF)});
      legend.valueLabels.template.setAll({fill: am5.color(0xFFFFFF)});


      legend.valueLabels.template.setAll({
        width: am5.p200,
        textAlign: "right"
      });

      legend.itemContainers.template.set("width", am5.p100);
      legend.valueLabels.template.setAll({
        width: am5.p100,
        textAlign: "right"
      });

      legend.itemContainers.template.setAll({
        paddingTop: 2,
        paddingBottom: 2
      });

      legend.data.setAll(chart.series.values);
      chart.appear(1000, 100);
    });
  },
  methods: {
    async fetchData(url) {
      const temp = url.split(',')[1];
      const response = await fetch(`${api}${temp}`);
      if (response.ok) {
        return await response.json();
      } else {
        console.error("Failed to fetch data");
        return [];
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
  margin-top: 1rem;
  width: 100%;
  height: 500px;
  max-width: 100%;
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