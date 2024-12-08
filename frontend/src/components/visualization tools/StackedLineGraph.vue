<template>
  <div class="chardivContainerStackedLine" :ref="chartRef">
    <h2>{{ title }}</h2>
    <div :id="chartId" class="chartdivStackedLine"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

const api = "http://127.0.0.1:5000/";

export default {
  name: "StackedLineGraphComponent",
  props: {
    url: {
      type: String,
      required: true
    },
    detailed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      measurement: this.url.split(',')[0],
      interactable: this.url.split(',')[2] === 'true',
      title: this.url.split(',')[1].split('/')[1],
      chartId: `chartdivStackedLine-${Math.random().toString(36).substr(2, 9)}`,
      chartRef: ref(null),
    };
  },
  mounted() {
    this.initializeLineGraph();
  },
  watch: {
    detailed: 'initializeLineGraph'
  },
  methods: {
  async initializeLineGraph() {
    if (this.root) {
      this.root.dispose();
      this.root = null;
    }

    let prefix = this.measurement === "percentage" ? "%" : "twh";
    let interactable = this.interactable;
    console.log(interactable);
    let data = await this.fetchData(this.url.split(',')[1]);
    if (!this.detailed){
      data.forEach(item => {
        item.year = item.year.toString();
        item.bad_energy = item.bioenergy_generation__twh_chart_electricity_prod_source_stacked +
            item.coal_generation__twh_chart_electricity_prod_source_stacked +
            item.gas_generation__twh_chart_electricity_prod_source_stacked +
            item.oil_generation__twh_chart_electricity_prod_source_stacked;
        item.clean_energy = item.hydro_generation__twh_chart_electricity_prod_source_stacked +
            item.nuclear_generation__twh_chart_electricity_prod_source_stacked +
            item.solar_generation__twh_chart_electricity_prod_source_stacked +
            item.wind_generation__twh_chart_electricity_prod_source_stacked;
      });
    }
    am5.ready(async () => {
      // Create root element
      this.root = am5.Root.new(this.chartId);

      // Set themes
      this.root.setThemes([
        am5themes_Animated.new(this.root)
      ]);

      // Create chart
      let chart = this.root.container.children.push(am5xy.XYChart.new(this.root, {
        panX: interactable,
        panY: interactable,
        wheelX: interactable ? "panX" : "none",
        wheelY: interactable ? "zoomX" : "none",
        pinchZoomX: interactable,
        maxZoomLevelX: interactable ? 10 : 1,
      }));

      chart.set("colors", am5.ColorSet.new(this.root, {
        step: 2,
        colors: [
          am5.color(0x73556E),
          am5.color(0x9FA1A6),
          am5.color(0xF2AA6B),
          am5.color(0xF28F6B),
          am5.color(0xA95A52),
          am5.color(0xE35B5D),
          am5.color(0xFFA446)
        ]
      }));

      // Add cursor
      var cursor = chart.set("cursor", am5xy.XYCursor.new(this.root, {
        behavior: "none"
      }));
      cursor.lineY.set("visible", false);

      // Create axes
      var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(this.root, {
        categoryField: "year",
        startLocation: 0.5,
        endLocation: 0.5,
        renderer: am5xy.AxisRendererX.new(this.root, {
          minorGridEnabled: true,
          minGridDistance: 70,
          labels: {
            fill: am5.color(0xFFFFFF)
          },
        }),
        tooltip: am5.Tooltip.new(this.root, {})
      }));

      xAxis.get("renderer").labels.template.setAll({
        fill: am5.color(0xFFFFFF)
      });

      xAxis.data.setAll(data);

      var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(this.root, {
        renderer: am5xy.AxisRendererY.new(this.root, {}),
        labels: {
          fill: am5.color(0xFFFFFF)
        },
        min: 0,
        max: prefix === "twh" ? 30000 : 100
      }));

      yAxis.get("renderer").labels.template.setAll({
        fill: am5.color(0xFFFFFF)
      });

      // Add series
      const createSeries = (name, field) => {
        var series = chart.series.push(am5xy.SmoothedXLineSeries.new(this.root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          categoryXField: "year",
          stacked: true,
          stroke: am5.color(0xffffff),
          tooltip: am5.Tooltip.new(this.root, {
            pointerOrientation: "horizontal",
            labelText: "[bold]{name}[/]\n{categoryX}: {valueY.formatNumber('#,###.00')}" + prefix
          })
        }));

        series.strokes.template.setAll({
          strokeWidth: 4,
          strokeOpacity: 1,
          shadowBlur: 2,
          shadowOffsetX: 2,
          shadowOffsetY: 2,
          shadowColor: am5.color(0x000000),
          shadowOpacity: 0.1
        });

        series.fills.template.setAll({
          fillOpacity: 1,
          visible: true,
          fillPattern: am5.GrainPattern.new(this.root, {
            maxOpacity: 0.15,
            density: 0.5,
            colors: [am5.color(0x000000), am5.color(0x000000), am5.color(0xffffff)]
          })
        });

        series.data.setAll(data);
        series.appear(1000);
      }

      if (this.detailed) {
        createSeries("Biofuel", "bioenergy_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Coal", "coal_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Gas", "gas_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Hydro", "hydro_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Nuclear", "nuclear_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Oil", "oil_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Solar", "solar_generation__twh_chart_electricity_prod_source_stacked");
        createSeries("Wind", "wind_generation__twh_chart_electricity_prod_source_stacked");
      } else {
        createSeries("Dirty Energy", "bad_energy");
        createSeries("Clean Energy", "clean_energy");
      }

      // Make stuff animate on load
      chart.appear(1000, 100);
    });
  },
  async fetchData(url) {
    const response = await fetch(`${api}${url}`);
    return await response.json();
  }
}
};
</script>

<style scoped>
.chartdivStackedLine {
  width: 100%;
  height: 100%;
}

.chardivContainerStackedLine {
  position: relative;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 0 0 20px 0;
}

h2 {
  color: white;
  font-size: 1.5rem;
}
</style>