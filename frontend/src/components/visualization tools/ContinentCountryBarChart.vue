<template>
  <div id="chartdivContainer">
    <div id="continentchartdiv"></div>
  </div>
</template>

<script>
// Import necessary amCharts libraries
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "ContinentChartComponent",
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      // Create root element
      let root_continent_chart = am5.Root.new("continentchartdiv");

      // Set themes
      root_continent_chart.setThemes([am5themes_Animated.new(root_continent_chart)]);

      // Create chart
      let chart = root_continent_chart.container.children.push(
          am5xy.XYChart.new(root_continent_chart, {
            panX: false,
            panY: false,
            wheelX: "panX",
            wheelY: "zoomX",
            paddingLeft: 0,
            layout: root_continent_chart.verticalLayout
          })
      );

      root_continent_chart.interfaceColors.set("text", am5.color(0xffffff));
      // Data
      let colors = chart.get("colors");
      let data = [
        { country: "US", visits: 725, icon: "https://www.amcharts.com/wp-content/uploads/flags/united-states.svg", columnSettings: { fill: colors.next() } },
        { country: "UK", visits: 625, icon: "https://www.amcharts.com/wp-content/uploads/flags/united-kingdom.svg", columnSettings: { fill: colors.next() } },
        { country: "China", visits: 602, icon: "https://www.amcharts.com/wp-content/uploads/flags/china.svg", columnSettings: { fill: colors.next() } },
        { country: "Japan", visits: 569, icon: "https://www.amcharts.com/wp-content/uploads/flags/japan.svg", columnSettings: { fill: colors.next() } },
        { country: "Germany", visits: 506, icon: "https://www.amcharts.com/wp-content/uploads/flags/germany.svg", columnSettings: { fill: colors.next() } },
        { country: "France", visits: 495, icon: "https://www.amcharts.com/wp-content/uploads/flags/france.svg", columnSettings: { fill: colors.next() } },
        { country: "India", visits: 488, icon: "https://www.amcharts.com/wp-content/uploads/flags/india.svg", columnSettings: { fill: colors.next() } },
        { country: "Spain", visits: 443, icon: "https://www.amcharts.com/wp-content/uploads/flags/spain.svg", columnSettings: { fill: colors.next() } },
        { country: "Italy", visits: 430, icon: "https://www.amcharts.com/wp-content/uploads/flags/italy.svg", columnSettings: { fill: colors.next() } },
        { country: "Netherlands", visits: 291, icon: "https://www.amcharts.com/wp-content/uploads/flags/netherlands.svg", columnSettings: { fill: colors.next() } },
        { country: "Russia", visits: 286, icon: "https://www.amcharts.com/wp-content/uploads/flags/russia.svg", columnSettings: { fill: colors.next() } },
        { country: "South Korea", visits: 242, icon: "https://www.amcharts.com/wp-content/uploads/flags/south-korea.svg", columnSettings: { fill: colors.next() } },
        { country: "Canada", visits: 234, icon: "https://www.amcharts.com/wp-content/uploads/flags/canada.svg", columnSettings: { fill: colors.next() } }
      ];

      var xRenderer = am5xy.AxisRendererX.new(root_continent_chart, {
        minGridDistance: 30,
        minorGridEnabled: true
      })

      var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root_continent_chart, {
        categoryField: "country",
        renderer: xRenderer
      }));

      // Create axes
      xRenderer.grid.template.setAll({
        location: 1
      })

      xRenderer.labels.template.setAll({
        paddingTop: 20
      });

      xAxis.data.setAll(data);

      var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root_continent_chart, {
        renderer: am5xy.AxisRendererY.new(root_continent_chart, {
          strokeOpacity: 0.1
        })
      }));


// Add series
// https://www.amcharts.com/docs/v5/charts/xy-chart/series/
      var series = chart.series.push(am5xy.ColumnSeries.new(root_continent_chart, {
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "visits",
        categoryXField: "country"
      }));

      series.columns.template.setAll({
        tooltipText: "{categoryX}: {valueY}",
        tooltipY: 0,
        strokeOpacity: 0,
        templateField: "columnSettings"
      });

      series.data.setAll(data);

      series.bullets.push(function (root_continent_chart, series, dataItem) {
        return am5xy.Bullet.new(root_continent_chart, {
          sprite: am5.Picture.new(root_continent_chart, {
            width: 24,
            height: 24,
            centerX: am5.p50,
            centerY: am5.p100, // Position the icon at the bottom center of the column
            src: dataItem.dataContext.icon
          })
        });
      });

      // Animate on load
      series.appear();
      chart.appear(1000, 100);

      this.root = root_continent_chart; // Store root for cleanup
    }
  },
  beforeUnmount() {
    if (this.root) {
      this.root.dispose(); // Dispose the chart to prevent memory leaks
    }
  }
};
</script>

<style scoped>
#continentchartdiv {
  width: 100%;
  height: 500px;
}

#chartdivContainer {
  position: relative;
  width: 100%;
  height: 550px;
}
</style>