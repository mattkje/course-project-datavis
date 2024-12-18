<template>
  <div id="chartdiv" ref="chartdiv">
    <div class="measurement-label">Measured in <span class="bold">{{ measurement }}</span></div>
  </div>
</template>

<script>
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy.js";
import {Theme as am5themes_Responsive} from "@amcharts/amcharts5";
import { prettyNames } from "@/components/dictionaries/prettyNames.js";

const api = "http://127.0.0.1:5000/";

export default {
  name: "BarChartComponent",
  props: {
    url: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      measurement: this.url.split(',')[0]
    };
  },
  mounted() {
    let root = am5.Root.new(this.$refs.chartdiv);

    const myTheme = am5.Theme.new(root);
    myTheme.rule("AxisLabel", ["minor"]).setAll({ dy: 1 });

    root.setThemes([am5themes_Animated.new(root), myTheme, am5themes_Responsive.new(root)]);

    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: false,
      panY: false,
      wheelX: "panX",
      wheelY: "zoomX",
      paddingLeft: 0
    }));

    const cursor = chart.set("cursor", am5xy.XYCursor.new(root, { behavior: "zoomX" }));
    cursor.lineY.set("visible", false);

    this.fetchData(this.url).then(data => {
      data.forEach(item => {
        item.date = new Date(parseInt(item.year), 0, 1).getTime();
      });

      // Create X-axis
      const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0,
        baseInterval: { timeUnit: "year", count: 1 },
        renderer: am5xy.AxisRendererX.new(root, { minorGridEnabled: true, minorLabelsEnabled: true }),
        tooltip: am5.Tooltip.new(root, {}),
      }));

      xAxis.get("renderer").labels.template.setAll({
        fill: am5.color(0xFFFFFF)
      });

      // Create Y-axis
      const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      // Set y-axis label color to white
      yAxis.get("renderer").labels.template.setAll({
        fill: am5.color(0xFFFFFF)  // Set the y-axis label text color to white
      });

      const measure = this.url.split(',')[0];
      const temp = this.url.split(',')[1];
      const value = temp.split('/')[0];

      const series = chart.series.push(am5xy.ColumnSeries.new(root, {
        name: prettyNames[value],
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: value,
        valueXField: "date",
        tooltip: am5.Tooltip.new(root, {
          labelText: `${prettyNames[value]}: {${value}} ${measure}`,
        })
      }));

      // Style series
      series.columns.template.setAll({ strokeOpacity: 0 });
      series.data.setAll(data);

      // Add legend
      const legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
        width: 200,
        paddingLeft: 15,
        height: am5.percent(100)
      }));

      legend.labels.template.setAll({
        fill: am5.color(0xFFFFFF)
      });

      legend.itemContainers.template.set("width", am5.p100);
      legend.valueLabels.template.setAll({
        width: am5.p100,
        textAlign: "right",
        fill: am5.color(0xFFFFFF)
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
  margin-top: 6rem;
  width: 100%;
  height: 500px;
  max-width: 100%;
}

.measurement-label {
  position: absolute;
  bottom: 10%;
  right: 100px;
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