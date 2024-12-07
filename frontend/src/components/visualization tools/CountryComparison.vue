<template>
  <div id="chartdivContainer_countrComparison">
    <div ref="comparisonchart" id="comparisonchartdiv">
      <p v-if="noCountries" id="errorText">No Countries chosen</p>
    </div>
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
      noCountries: false,
    };
  },
  mounted() {
    this.createChart(); // Initialize chart on component mount
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
    countries: 'createChart',      // Watch countries
    startYear: 'createChart',  // Watch startYear
    endYear: 'createChart',    // Watch endYear
    comparisonData: 'createChart' // Watch comparisonData
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
        // Create root element
        if (this.root) {
          this.root.dispose();
          this.root = null;
        }
        
        this.root = am5.Root.new(this.$refs.comparisonchart);

        // Set themes
        this.root.setThemes([am5themes_Animated.new(this.root)]);

        // Create chart
        let chart = this.root.container.children.push(
            am5xy.XYChart.new(this.root, {
              panX: false,
              panY: false,
              paddingLeft: 0,
              wheelX: "panX",
              wheelY: "zoomX",
              layout: this.root.verticalLayout,
            })
        );

        this.root.interfaceColors.set("text", am5.color(0xffffff));

        // Add legend
        let legend = chart.children.push(
            am5.Legend.new(this.root, {
              centerX: am5.p50,
              x: am5.p50,
            })
        );


        if (this.countries === "") {
          this.noCountries = true;
          return;
        } else {
          this.noCountries = false;
        }
        let chartData = await this.fetchData(`comparison/${this.countries}/${this.comparisonData}`);

        // Initially filter data based on the start and end year
        chartData = this.filterChartData(chartData, this.startYear, this.endYear);

        chartData.forEach(item => {
          item.year = item.year.toString().replace(",", "");
        });

        // Create axes
        let xRenderer = am5xy.AxisRendererX.new(this.root, {
          cellStartLocation: 0.1,
          cellEndLocation: 0.9,
          minorGridEnabled: true,
        });

        let xAxis = chart.xAxes.push(
            am5xy.CategoryAxis.new(this.root, {
              categoryField: "year",
              renderer: xRenderer,
              tooltip: am5.Tooltip.new(this.root, {}),
            })
        );

        xRenderer.grid.template.setAll({location: 1});
        xAxis.data.setAll(chartData);

        let yAxis = chart.yAxes.push(
            am5xy.ValueAxis.new(this.root, {
              renderer: am5xy.AxisRendererY.new(this.root, {strokeOpacity: 0.1}),
            })
        );

        // Create series for each region
        const makeSeries = (name, fieldName) => {
          let series = chart.series.push(
              am5xy.ColumnSeries.new(this.root, {
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

          series.data.setAll(chartData);

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

          legend.data.push(series);
        }

        // Create series for each country
        this.countries.split(",").forEach(country => {
          makeSeries(country, country);
        });

        this.updateChartData()

        // Animate on load
        await chart.appear(1000, 100);
      },

      updateChartData() {
        if (!this.chart || !this.chartData) return; // Prevent errors if chart or data are not ready

        // Filter data based on the updated year range
        const filteredData = this.filterChartData(this.chartData, this.startYear, this.endYear);

        // Update the xAxis with new data
        let xAxis = this.chart.xAxes.getIndex(0); // Get the xAxis from the chart
        if (xAxis) {
          xAxis.data.setAll(filteredData);
        }

        // Get the current list of countries
        const currentCountries = this.countries.split(",");

        // Remove series for countries no longer in the list
        const existingSeries = this.chart.series;
        const seriesToRemove = [];
        existingSeries.each(series => {
          if (!currentCountries.includes(series.get("name"))) {
            seriesToRemove.push(series);
          }
        });

        // Dispose of removed series
        seriesToRemove.forEach(series => {
          this.chart.series.removeValue(series).dispose();
        });

        // Add or update series for the current countries
        currentCountries.forEach(country => {
          let series = existingSeries.find(s => s.get("name") === country);

          if (!series) {
            // Create a new series for the country
            series = this.chart.series.push(
                am5xy.ColumnSeries.new(this.root, {
                  name: country,
                  xAxis: xAxis,
                  yAxis: this.chart.yAxes.getIndex(0),
                  valueYField: country,
                  categoryXField: "year",
                })
            );

            series.columns.template.setAll({
              tooltipText: "{name}, {categoryX}: {valueY}",
              width: am5.percent(90),
              tooltipY: 0,
              strokeOpacity: 0,
            });

            series.data.setAll(filteredData);
          } else {
            // Update the series data
            series.data.setAll(filteredData);
          }
        });

        // Optionally, animate the chart again if needed
        this.chart.appear(1000, 100);
      }
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.dispose(); // Dispose the chart to prevent memory leaks
      }
    }
};
</script>

<style scoped>
#errorText {
  color: white;
  font-size: 48px;
  text-align: center;
}

#comparisonchartdiv {
  width: 100%;
  height: 500px;
}

#chartdivContainer_countrComparison {
  position: relative;
  padding-top: 100px;
  width: 100%;
  height: 600px;
  margin: 0 0 40px 0;
}
</style>