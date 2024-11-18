<template>
  <div id="chartdiv" ref="chartdiv"></div>
</template>

<script>
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy.js";
import {Theme as am5themes_Responsive} from "@amcharts/amcharts5";

const prettyNames = {
  "co2": "CO\u2082",
  "co2_including_luc": "CO\u2082 w/Land Use Change",
  "coal_co2": "Coal",
  "consumption_co2": "Consumption",
  "cement_co2": "Cement",
  "flaring_co2": "Flaring",
  "gas_co2": "Gas",
  "land_use_change_co2": "Land Use Change",
  "oil_co2": "Oil",
  "other_industry_co2": "Other Industry",
  "temperature_change_from_co2": "Temperature Change from CO\u2082",
  "trade_co2": "Trade",
  "co2_including_luc_per_gdp": "CO\u2082 w/Land Use Change per GDP",
  "co2_per_gdp": "CO\u2082 per GDP",
  "consumption_co2_per_gdp": "Consumption CO\u2082 per GDP",
  "energy_per_gdp": "Energy per GDP"
};

const api = "http://127.0.0.1:5000/";

export default {
  name: "BarChartComponent",
  props: {
    url: {
      type: String,
      required: true
    }
  },
  mounted() {
    let root = am5.Root.new(this.$refs.chartdiv);

    const myTheme = am5.Theme.new(root);
    myTheme.rule("AxisLabel", ["minor"]).setAll({dy: 1});

    root.setThemes([am5themes_Animated.new(root), myTheme, am5themes_Responsive.new(root)]);

    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: false,
      panY: false,
      wheelX: "panX",
      wheelY: "zoomX",
      paddingLeft: 0
    }));

    const cursor = chart.set("cursor", am5xy.XYCursor.new(root, {behavior: "zoomX"}));
    cursor.lineY.set("visible", false);

    this.fetchData(this.url).then(data => {
      data.forEach(item => {
        item.date = new Date(parseInt(item.year), 0, 1).getTime();
      });


      const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0,
        baseInterval: {timeUnit: "year", count: 1},
        renderer: am5xy.AxisRendererX.new(root, {minorGridEnabled: true, minorLabelsEnabled: true}),
        tooltip: am5.Tooltip.new(root, {})
      }));

      const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      const fields = Object.keys(data[0]).filter(key => key !== "year");

      fields.forEach(field => {
        const series = chart.series.push(am5xy.ColumnSeries.new(root, {
          name: prettyNames[field],
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: "co2_growth_prct",
          valueXField: "date",
          tooltip: am5.Tooltip.new(root, {labelText: `{${field}}  %`})
        }));

        series.columns.template.setAll({strokeOpacity: 0});
        series.data.setAll(data);
      });

      chart.set("scrollbarX", am5.Scrollbar.new(root, {orientation: "horizontal"}));
      chart.appear(1000, 100);
    });
  },
  methods: {
    async fetchData(url) {
      const response = await fetch(`${api}${url}`);
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
  width: 70%;
  height: 500px;
  max-width: 70%;
}
</style>