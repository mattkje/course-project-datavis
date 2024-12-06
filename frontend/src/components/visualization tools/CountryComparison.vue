<template>
  <div id="chartdivContainer_countrComparison">
    <div ref="chartContainer" id="comparisonchartdiv"></div>
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
      chartData: [],  // Holds the chart data fetched from the API
      root: null,     // Holds the amCharts root object (reference to the chart)
      chart: null,    // Reference to the chart instance
      series: [],     // Reference to the chart series
    };
  },
  mounted() {
    const chartContainer = this.$refs.chartContainer;
    if (chartContainer) {
      this.createChart(chartContainer);  // Create the chart when the component mounts
    }
  },
  props: {
    countries: {
      type: String,
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
    // Watch for changes in countries and comparisonData to trigger chart update
    countries: 'updateChartData',
    comparisonData: 'updateChartData',
    startYear: 'updateChartData',  // Watch for changes in year range
    endYear: 'updateChartData',    // Watch for changes in year range
  },

  methods: {
    // Fetch data from the backend
    async fetchData(url) {
      try {
        const response = await fetch('http://127.0.0.1:5000/' + url);
        return await response.json();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    // Filter data by the selected year range and countries
    filterChartData(data, startYear, endYear) {
      return data
          .filter(item => item.year >= startYear && item.year <= endYear)
          .map(item => {
            const filteredItem = { year: item.year }; // Always include year

            // Include data for selected countries dynamically
            this.countries.split(",").forEach(country => {
              if (item[country]) {  // Ensure the country exists in the item
                filteredItem[country] = item[country];
              }
            });
            return filteredItem;
          });
    },

    // Create the chart (initial setup)
    async createChart() {
      if (this.countries === "") return;

      // Remove the old chart if it exists
      if (this.root) {
        await this.removeChart();  // Ensure the previous chart is disposed
      }

      // Create a new root element for amCharts
      let root_country_comparison = am5.Root.new("comparisonchartdiv"); // Attach the chart to the container ref
      this.root = root_country_comparison; // Store reference to root

      root_country_comparison.setThemes([am5themes_Animated.new(root_country_comparison)]);

      // Create the XYChart itself
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

      this.chart = chart; // Store reference to the chart

      // Set color theme
      root_country_comparison.interfaceColors.set("text", am5.color(0xffffff));

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

      xRenderer.grid.template.setAll({
        location: 1,  // This adjusts where the grid lines appear
        strokeOpacity: 0.3,  // Adjust opacity if needed
        stroke: am5.color(0x888888),  // Set a color for the grid lines
      });

      // Also, set axis labels to a visible style
      xRenderer.labels.template.setAll({
        fill: am5.color(0xffffff),  // Label color
        fontSize: 12,  // Adjust font size if needed
      });

      this.xAxis = xAxis;

      this.yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(root_country_comparison, {
            renderer: am5xy.AxisRendererY.new(root_country_comparison, { strokeOpacity: 0.1 }),
          })
      );

      // Fetch and process chart data
      this.chartData = await this.fetchData(`comparison/${this.countries}/${this.comparisonData}`);
      this.chartData = this.filterChartData(this.chartData, this.startYear, this.endYear);

      // Format the data to avoid errors (e.g., remove commas from years)
      this.chartData.forEach(item => {
        item.year = item.year.toString().replace(",", "").trim();  // Remove commas and spaces
      });

      this.xAxis.data.setAll(this.chartData);
      this.countries.split(",").forEach(country => {
        this.makeSeries(country, country);
      });

      // Animate chart appearance
      await chart.appear(1000, 100);
    },

    // Method to remove old chart (dispose it)
    async removeChart() {
      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }
      if (this.root) {
        this.root.dispose();
        this.root = null;
      }
    },

    // Update chart data dynamically (called by prop watchers)
    async updateChartData() {
      // Create the data URL using countries and comparisonData
      const url = `comparison/${this.countries}/${this.comparisonData}`;

      // Fetch the data
      this.chartData = await this.fetchData(url);
      this.chartData = this.filterChartData(this.chartData, this.startYear, this.endYear);

      // Format the year data (e.g., removing commas)
      this.chartData.forEach(item => {
        item.year = item.year.toString().replace(",", "");
      });

      // Update xAxis with filtered data
      if (this.xAxis) {
        this.xAxis.data.setAll(this.chartData);
      }

      // Remove all existing series before adding new ones
      if (this.chart) {
        this.chart.series.clear(); // This removes the old series
      }

      // Create or update series for each country dynamically
      this.countries.split(",").forEach(country => {
        this.makeSeries(country, country);
      });

      // Animate chart appearance if necessary
      if (this.chart) {
        await this.chart.appear(1000, 100);
      }
    },

    // Function to create or update series dynamically
    makeSeries(name, fieldName) {
      let series = this.chart.series.push(
          am5xy.ColumnSeries.new(this.root, {
            name: name,
            xAxis: this.xAxis,
            yAxis: this.yAxis,
            valueYField: fieldName,  // Field corresponding to country values
            categoryXField: "year",  // Category for x-axis (years)
          })
      );

      // Set column series template
      series.columns.template.setAll({
        tooltipText: "{name}, {categoryX}: {valueY}",
        width: am5.percent(90),
        tooltipY: 0,
        strokeOpacity: 0,
      });

      // Set the series data
      series.data.setAll(this.chartData);

      // Add labels to columns
      series.bullets.push(() => {
        return am5.Bullet.new(this.root, {
          locationY: 0,
          sprite: am5.Label.new(this.root, {
            text: "{valueY}",
            fill: this.root.interfaceColors.get("alternativeText"),
            centerY: 0,
            centerX: am5.p50,
            populateText: true,
          }),
        });
      });

      // Ensure legend is created
      if (!this.chart.legend) {
        this.chart.legend = am5.Legend.new(this.root, {
          centerX: am5.p50,
          x: am5.p50,
        });
      }

      // Add the series to the legend
      this.chart.legend.data.push(series);
    },
  },

  beforeUnmount() {
    // Dispose of the chart when component unmounts to avoid memory leaks
    if (this.root) {
      this.root.dispose();
    }
  },
};
</script>

<style scoped>
#comparisonchartdiv {
  width: 100%;
  height: 500px;
}

#chartdivContainer_countrComparison {
  position: relative;
  padding-top: 150px;
  width: 100%;
  height: 600px;
  margin: 0;
}
</style>
