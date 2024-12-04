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
    async fetchData(url) {
      try {
        const response = await fetch("http://127.0.0.1:5000/" + url)
        return await response.json();
      } catch (error) {
        console.error('There was an error!', error);
      }
    },
    async createChart() {
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

      let country_data = await this.fetchData("continent_data/AF/co2");
      country_data.sort((a, b) => Object.values(b)[0] - Object.values(a)[0]);

      let top_countries = country_data.slice(0, 10).map(item => item.country).join(',');

      let translated_names = await this.fetchData(`translate/${top_countries}`);

      let data = country_data.slice(0, 10).map((item, index) => ({
        country: item.country,
        visits: Object.values(item)[0],
        icon: `public/countryflags/${translated_names[index].countryCode}.svg`,
        columnSettings: { fill: colors.next() }
      }));

      var xRenderer = am5xy.AxisRendererX.new(root_continent_chart, {
        minGridDistance: 30,
        minorGridEnabled: true
      })

      var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root_continent_chart, {
        categoryField: "country",
        renderer: xRenderer,
        bullet: function (root, axis, dataItem) {
          return am5xy.AxisBullet.new(root_continent_chart, {
            location: 0.5,
            sprite: am5.Picture.new(root_continent_chart, {
              width: 32,
              height: 24,
              centerY: am5.p50,
              centerX: am5.p50,
              src: dataItem.dataContext.icon
            })
          });
        }
      }));

      // Create axes
      xRenderer.grid.template.setAll({
        location: 1
      })

      xRenderer.labels.template.setAll({
        paddingTop: 20,
        maxWidth: 100,
        wrap: true,
        textAlign: "center"
      });

      xAxis.data.setAll(data);

      var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root_continent_chart, {
        renderer: am5xy.AxisRendererY.new(root_continent_chart, {
          strokeOpacity: 0.1
        })
      }));

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