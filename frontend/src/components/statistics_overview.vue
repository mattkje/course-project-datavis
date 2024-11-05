<template>
  <div id="chartdiv" ref="chartdiv"></div>
</template>

<script>
export default {
  name: "AmChartComponent",
  props: {
    countryName: {
      type: String,
      required: true
    }
  },
  mounted() {
    // Create root element for the chart
    let root = am5.Root.new(this.$refs.chartdiv);

    const myTheme = am5.Theme.new(root);

    // Custom theme rules
    myTheme.rule("AxisLabel", ["minor"]).setAll({ dy: 1 });
    myTheme.rule("Grid", ["x"]).setAll({ strokeOpacity: 0.05 });
    myTheme.rule("Grid", ["x", "minor"]).setAll({ strokeOpacity: 0.05 });

    // Set themes
    root.setThemes([am5themes_Animated.new(root), myTheme]);

    // Create chart
    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      maxTooltipDistance: 0,
      pinchZoomX: true
    }));

    // Fetch data based on countryName prop
    this.fetchData(this.countryName).then(data => {
      // Parse the year field as a date
      data.forEach(item => {
        item.year = new Date(item.year, 0, 1).getTime();
      });

      // Create axes
      const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0.2,
        baseInterval: { timeUnit: "year", count: 1 },
        renderer: am5xy.AxisRendererX.new(root, { minorGridEnabled: true }),
        tooltip: am5.Tooltip.new(root, {})
      }));

      const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      // Add series for each data field
      const fields = Object.keys(data[0]).filter(key => key !== "year");

      fields.forEach(field => {
        const series = chart.series.push(am5xy.LineSeries.new(root, {
          name: field,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          valueXField: "year",
          legendValueText: `{${field}}`,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            labelText: `{${field}}`
          })
        }));

        series.data.setAll(data);

        // Make stuff animate on load
        series.appear();
      });

      // Add cursor
      const cursor = chart.set("cursor", am5xy.XYCursor.new(root, { behavior: "none" }));
      cursor.lineY.set("visible", false);

      // Add scrollbars
      chart.set("scrollbarX", am5.Scrollbar.new(root, { orientation: "horizontal" }));
      chart.set("scrollbarY", am5.Scrollbar.new(root, { orientation: "vertical" }));

      // Add legend
      const legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
        width: 200,
        paddingLeft: 15,
        height: am5.percent(100)
      }));

      legend.itemContainers.template.events.on("pointerover", function(e) {
        const itemContainer = e.target;
        const series = itemContainer.dataItem.dataContext;
        chart.series.each(function(chartSeries) {
          if (chartSeries !== series) {
            chartSeries.strokes.template.setAll({
              strokeOpacity: 0.15,
              stroke: am5.color(0x000000)
            });
          } else {
            chartSeries.strokes.template.setAll({ strokeWidth: 3 });
          }
        });
      });

      legend.itemContainers.template.events.on("pointerout", function(e) {
        const itemContainer = e.target;
        const series = itemContainer.dataItem.dataContext;

        chart.series.each(function(chartSeries) {
          chartSeries.strokes.template.setAll({
            strokeOpacity: 1,
            strokeWidth: 1,
            stroke: chartSeries.get("fill")
          });
        });
      });

      legend.itemContainers.template.set("width", am5.p100);
      legend.valueLabels.template.setAll({
        width: am5.p100,
        textAlign: "right"
      });

      // Set legend data after all events
      legend.data.setAll(chart.series.values);

      // Animate the chart on load
      chart.appear(1000, 100);
    });
  },
  methods: {
    async fetchData(countryName) {
      const response = await fetch(`http://127.0.0.1:5000/co2/${countryName}`);
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
  width: 100%;
  height: 500px;
  max-width: 100%;
}
</style>