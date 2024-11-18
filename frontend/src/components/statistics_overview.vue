<template>
  <div id="chartdiv" ref="chartdiv"></div>
</template>

<script>
const prettyNames = {
  "co2": "CO2",
  "co2_including_luc": "CO2 Including LUCF",
  "coal_co2": "Coal CO2",
  "consumption_co2": "Consumption CO2",
  "flaring_co2": "Flaring CO2",
  "gas_co2": "Gas CO2",
  "land_use_change_co2": "Land Use Change CO2",
  "oil_co2": "Oil CO2",
  "other_industry_co2": "Other Industry CO2",
  "temperature_change_from_co2": "Temperature Change from CO2",
  "trade_co2": "Trade CO2"
};

// TODO: Add a unit translation for each type
// TODO: Add all the prettyNames
// TODO: Makes this take in inputs instead of a set datatype


export default {
  name: "AmChartComponent",
  props: {
    countryName: {
      type: String,
      required: true
    }
  },
  mounted() {
    let root = am5.Root.new(this.$refs.chartdiv);

    const myTheme = am5.Theme.new(root);

    // Custom theme rules to change text color
    myTheme.rule("AxisLabel").setAll({ fill: am5.color(0xFFFFFF) });
    myTheme.rule("Tooltip").setAll({ labelText: { fill: am5.color(0xFFFFFF) } });
    myTheme.rule("LegendLabel").setAll({ labelText: { fill: am5.color(0xFFFFFF) } });
    myTheme.rule("LegendValueLabel").setAll({ labelText: { fill: am5.color(0xFFFFFF) } });

    root.setThemes([am5themes_Animated.new(root), myTheme]);

    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      maxTooltipDistance: 0,
      pinchZoomX: true
    }));

    this.fetchData(this.countryName).then(data => {
      data.forEach(item => {
        item.year = new Date(item.year, 0, 1).getTime();
      });

      const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0.2,
        baseInterval: { timeUnit: "year", count: 1 },
        renderer: am5xy.AxisRendererX.new(root, { minorGridEnabled: true }),
        tooltip: am5.Tooltip.new(root, {})
      }));

      const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
      }));

      const fields = Object.keys(data[0]).filter(key => key !== "year");

      fields.forEach(field => {
        const series = chart.series.push(am5xy.LineSeries.new(root, {
          name: prettyNames[field],
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          valueXField: "year",
          legendValueText: `{${field}} million tons`,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            labelText: `{${field}} million tons`,
          })
        }));

          series.data.setAll(data);


        // This is how we can hide all series except for the one we want to show
        // TODO: MAKE THIS INTO A FUNCTION BASED THING
        if (field !== "co2") {
            series.hide();
          } else {
          series.appear();
          }
      });

      const cursor = chart.set("cursor", am5xy.XYCursor.new(root, { behavior: "none" }));
      cursor.lineY.set("visible", false);

      chart.set("scrollbarX", am5.Scrollbar.new(root, { orientation: "horizontal" }));
      chart.set("scrollbarY", am5.Scrollbar.new(root, { orientation: "vertical" }));

      const legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
        width: 400,
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

      legend.labels.template.setAll({
        fill: am5.color("#ffffff")
      });
      legend.valueLabels.template.setAll({
        fill: am5.color("#ffffff"),
        width: am5.p200,
        textAlign: "right"
      });

      legend.itemContainers.template.set("width", am5.p100);
      legend.valueLabels.template.setAll({
        width: am5.p100,
        textAlign: "right"
      });

      legend.data.setAll(chart.series.values);
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
  width: 70%;
  height: 500px;
  max-width: 70%;
}
</style>