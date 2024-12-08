<template>
  <div id="chartdivContainer_RingModule">
    <div id="chartdiv_RingModule"></div>
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5radar from "@amcharts/amcharts5/radar";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {prettyNames} from "@/components/dictionaries/prettyNames.js";

const api = "http://127.0.0.1:5000/";

export default {
  name: "RingModule",
  props: {
    url: {
      type: String,
      required: true
    },
  },
  mounted() {
    this.InitializeRingModule();
  },
  methods: {
    fetchData(url) {
      return fetch(api + url)
          .then(response => response.json())
          .then(data => {
            return data;
          });
    },
    async InitializeRingModule() {
      am5.ready(async () => {
        // Create root element
        var root = am5.Root.new("chartdiv_RingModule");

        // Set themes
        root.setThemes([am5themes_Animated.new(root)]);

        // Create chart
        var chart = root.container.children.push(
            am5radar.RadarChart.new(root, {
              panX: false,
              panY: false,
              wheelX: "panX",
              wheelY: "zoomX",
              innerRadius: am5.percent(20),
              startAngle: -90,
              endAngle: 180,
            })
        );


        let rawData = await this.fetchData(this.url);

        let data = Object.keys(rawData).map((key, index) => {
          return {
            category: prettyNames[key] || key,
            value: rawData[key],
            full: 100,
            columnSettings: {
              fill: chart.get("colors").getIndex(index),
            },
          };
        });

        // Add cursor
        var cursor = chart.set(
            "cursor",
            am5radar.RadarCursor.new(root, {
              behavior: "zoomX",
            })
        );
        cursor.lineY.set("visible", false);

        // Create axes and their renderers
        var xRenderer = am5radar.AxisRendererCircular.new(root, {});
        xRenderer.labels.template.setAll({
          radius: 10,
        });
        xRenderer.grid.template.setAll({
          forceHidden: true,
        });

        var xAxis = chart.xAxes.push(
            am5xy.ValueAxis.new(root, {
              renderer: xRenderer,
              min: 0,
              max: 60,
              numberFormat: "#'%'",
              tooltip: am5.Tooltip.new(root, {}),
            })
        );

        var yRenderer = am5radar.AxisRendererRadial.new(root, {
          minGridDistance: 20,
        });
        yRenderer.labels.template.setAll({
          centerX: am5.p100,
          fontWeight: "500",
          fontSize: 18,
          templateField: "columnSettings",
        });
        yRenderer.grid.template.setAll({
          forceHidden: true,
        });

        var yAxis = chart.yAxes.push(
            am5xy.CategoryAxis.new(root, {
              categoryField: "category",
              renderer: yRenderer,
            })
        );

        yAxis.data.setAll(data);

        // Create series
        var series1 = chart.series.push(
            am5radar.RadarColumnSeries.new(root, {
              xAxis: xAxis,
              yAxis: yAxis,
              clustered: false,
              valueXField: "full",
              categoryYField: "category",
              fill: root.interfaceColors.get("alternativeBackground"),
            })
        );
        series1.columns.template.setAll({
          width: am5.p100,
          fillOpacity: 0.08,
          strokeOpacity: 0,
          cornerRadius: 20,
        });
        series1.data.setAll(data);

        var series2 = chart.series.push(
            am5radar.RadarColumnSeries.new(root, {
              xAxis: xAxis,
              yAxis: yAxis,
              clustered: false,
              valueXField: "value",
              categoryYField: "category",
            })
        );
        series2.columns.template.setAll({
          width: am5.p100,
          strokeOpacity: 0,
          tooltipText: "{category}: {valueX}%",
          cornerRadius: 20,
          templateField: "columnSettings",
        });
        series2.data.setAll(data);

        // Animate chart and series in
        series1.appear(1000);
        series2.appear(1000);
        chart.appear(1000, 100);
      });
    }
  }
};
</script>

<style scoped>
#chartdiv_RingModule {
  width: 100%;
  height: 100%;
}

#chartdivContainer_RingModule {
  position: relative;
  justify-content: center;
  width: 100%;
  height: 850px;
  padding: 90px 0 60px 0;
}
</style>