<template>
  <div id="chartdivContainer_countrComparison">
    <div id="comparisonchartdiv"></div>
  </div>
</template>

<script>
// Import amCharts libraries
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "CountryComparisonChart",
  data() {
    return {
      chartData: [],
      root: null,
      chart: null,
      series: [],
    };
  },
  mounted() {
    this.createChart(); // Initialize chart on component mount
  },
  props: {
    countries: {
      type: Array,
      required: true,
    },
    startYear: {
      type: Number,
      required: true,
    },
    endYear: {
      type: Number,
      required: true,
    },
    comparisonData: {
      type: String,
      required: true,
    }
  },
  watch: {
    countries: 'createChart',
    startYear: 'updateChartData',  // Watch startYear
    endYear: 'updateChartData',    // Watch endYear
    async comparisonData(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.chartData = await this.fetchData(`comparison/${this.countries.join(',')}/${newVal}`);
        this.chartData.forEach(item => {
          item.year = item.year.toString().replace(",", "");
        });
        this.updateChartData();
      }
    }
  },
  methods: {
    async fetchData(url) {
      try {
        const response = await fetch('http://127.0.0.1:5000/' + url);
        return await response.json();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    filterChartData(data, startYear, endYear) {
      return data.filter(item => item.year >= startYear && item.year <= endYear);
    },
    async createChart() {
      if (this.root) {
        this.root.dispose(); // Dispose of the existing chart if it exists
        this.root = null;
      }

      if (!this.$el) return;

      // Create root element
      let root_country_comparison = am5.Root.new("comparisonchartdiv");
      this.root = root_country_comparison;

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

      this.chart = chart; // Assign the chart to this.chart

      root_country_comparison.interfaceColors.set("text", am5.color(0xffffff));

      // Add legend
      let legend = chart.children.push(
          am5.Legend.new(root_country_comparison, {
            centerX: am5.p50,
            x: am5.p50,
          })
      );

      this.chartData = await this.fetchData(`comparison/${this.countries.join(',')}/${this.comparisonData}`);

      // Initially filter data based on the start and end year
      this.chartData = this.filterChartData(this.chartData, this.startYear, this.endYear);

      this.chartData.forEach(item => {
        item.year = item.year.toString().replace(",", "");
      });

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
      xAxis.data.setAll(this.chartData);

      let yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(root_country_comparison, {
            renderer: am5xy.AxisRendererY.new(root_country_comparison, { strokeOpacity: 0.1 }),
          })
      );

      // Create series for each region
      const makeSeries = (name, fieldName) => {
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
          tooltipText: "{name}, {categoryX}: {valueY}",
          width: am5.percent(90),
          tooltipY: 0,
          strokeOpacity: 0,
        });

        series.data.setAll(this.chartData);

        // Add labels to columns
        series.bullets.push(() => {
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

      // Create series for each country
      this.countries.forEach(country => {
        makeSeries(country, country);
      });

      // Animate on load
      await chart.appear(1000, 100);
    },

    updateChartData() {
      if (!this.chart || !this.chartData) return; // Prevent errors if the chart or data are not ready

      // Filter data based on updated year range
      const filteredData = this.filterChartData(this.chartData, this.startYear, this.endYear);

      // Update the xAxis with new data
      let xAxis = this.chart.xAxes.getIndex(0);  // Get the xAxis from the chart
      if (xAxis) {
        xAxis.data.setAll(filteredData);
      }

      // Update the series data for each country
      this.countries.forEach((country, index) => {
        let series = this.chart.series.getIndex(index);  // Get the corresponding series for the country
        if (series) {
          series.data.setAll(filteredData); // Update the data for the series
        }
      });

      // Optionally, you can animate the chart again if needed
      this.chart.appear(1000, 100);
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
#comparisonchartdiv {
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
