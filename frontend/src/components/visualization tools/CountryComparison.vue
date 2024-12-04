<template>
  <div id="chartdivContainer_countrComparison">
  <div id="chartdiv"></div>
  </div>
</template>

<script>
// Import amCharts libraries
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "CountryComparisonChart",
  mounted() {
    this.createChart(); // Initialize chart on component mount
  },
  methods: {
    createChart() {
      // Create root element
      let root_country_comparison = am5.Root.new("chartdiv");

      // Set themes
      root_country_comparison.setThemes([am5themes_Animated.new(root_country_comparison)]);

      // Create chart
      let chart = root_country_comparison.container.children.push(
          am5xy.XYChart.new(root_country_comparison, {
            panX: false,
            panY: false,
            paddingLeft: 0,
            wheelX: "panX",
            wheelY: "zoomX",
            layout: root_country_comparison.verticalLayout,
          })
      );

      root_country_comparison.interfaceColors.set("text", am5.color(0xffffff));

      // Add legend
      let legend = chart.children.push(
          am5.Legend.new(root_country_comparison, {
            centerX: am5.p50,
            x: am5.p50,
          })
      );

      // Sample data
      let data = [
        {
          year: "2021",
          europe: 2.5,
          namerica: 2.5,
          asia: 2.1,
          lamerica: 1,
          meast: 0.8,
          africa: 0.4,
        },
        {
          year: "2022",
          europe: 2.6,
          namerica: 2.7,
          asia: 2.2,
          lamerica: 0.5,
          meast: 0.4,
          africa: 0.3,
        },
        {
          year: "2023",
          europe: 2.8,
          namerica: 2.9,
          asia: 2.4,
          lamerica: 0.3,
          meast: 0.9,
          africa: 0.5,
        },
      ];

      // Create axes
      let xRenderer = am5xy.AxisRendererX.new(root_country_comparison, {
        cellStartLocation: 0.1,
        cellEndLocation: 0.9,
        minorGridEnabled: true,
      });

      let xAxis = chart.xAxes.push(
          am5xy.CategoryAxis.new(root_country_comparison, {
            categoryField: "year",
            renderer: xRenderer,
            tooltip: am5.Tooltip.new(root_country_comparison, {}),
          })
      );

      xRenderer.grid.template.setAll({ location: 1 });
      xAxis.data.setAll(data);

      let yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(root_country_comparison, {
            renderer: am5xy.AxisRendererY.new(root_country_comparison, { strokeOpacity: 0.1 }),
          })
      );

      // Function to create series
      function makeSeries(name, fieldName) {
        let series = chart.series.push(
            am5xy.ColumnSeries.new(root_country_comparison, {
              name: name,
              xAxis: xAxis,
              yAxis: yAxis,
              valueYField: fieldName,
              categoryXField: "year",
            })
        );

        series.columns.template.setAll({
          tooltipText: "{name}, {categoryX}:{valueY}",
          width: am5.percent(90),
          tooltipY: 0,
          strokeOpacity: 0,
        });

        series.data.setAll(data);

        // Add labels to columns
        series.bullets.push(function () {
          return am5.Bullet.new(root_country_comparison, {
            locationY: 0,
            sprite: am5.Label.new(root_country_comparison, {
              text: "{valueY}",
              fill: root_country_comparison.interfaceColors.get("alternativeText"),
              centerY: 0,
              centerX: am5.p50,
              populateText: true,
            }),
          });
        });

        legend.data.push(series);
      }

      // Create series for each region
      makeSeries("Europe", "europe");
      makeSeries("North America", "namerica");
      makeSeries("Asia", "asia");
      makeSeries("Latin America", "lamerica");
      makeSeries("Middle East", "meast");
      makeSeries("Africa", "africa");

      // Animate on load
      chart.appear(1000, 100);
    },
  },
};
</script>

<style scoped>
#chartdiv {
  width: 100%;
  height: 500px;
}

#chartdivContainer_countrComparison {
  position: relative;
  width: 100%;
  height: 600px;
  margin: 0 0 40px 0;
}
</style>
