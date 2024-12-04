<template>
  <div id="chartdivContainer_MotionChart">
    <div id="chartdiv_MotionChart"></div>
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5map from "@amcharts/amcharts5/map";
import am4geodata_continentsLow from "@amcharts/amcharts4-geodata/continentsLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {toRaw} from "vue";

const api = "http://127.0.0.1:5000/";
let selectedDataItem = null;
let selectedContinent = null;

export default {
  name: "MotionChartComponent",
  props: {
    url: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      rawYearData: {},
      yearData: {},
      firstYear: 1800,
      lastYear: 2022,
      currentYear: 1800,
      countries: {},
      colors: {
        EU: am5.color(0x1f77b4), // Blue
        NA: am5.color(0xff7f0e), // Orange
        SA: am5.color(0x2ca02c), // Green
        AS: am5.color(0xd62728), // Red
        AF: am5.color(0x9467bd), // Purple
        OC: am5.color(0x8c564b), // Brown
        AN: am5.color(0xe377c2)  // Pink
      },
      bubbleSeries: null,
      yearLabel: null,
      polygonSeries: null,
    };
  },
  mounted() {
    this.fetchCountryNameData().then(countryNameData => {
      this.countries = countryNameData.reduce((acc, country) => {
        const countryCode = country;
        acc[countryCode] = {
          name: country,
        };
        return acc;
      }, {});
    });
    this.fetchCountryValueData().then(countryValueData => {
      this.rawYearData = toRaw(countryValueData);
      this.initializeChart();
    });
  },
 methods: {
  async fetchCountryNameData() {
    const response = await fetch(`${api}countries`);
    if (response.ok) {
      return await response.json();
    } else {
      console.error("Failed to fetch data");
      return {};
    }
  },
  async fetchCountryValueData() {
    const response = await fetch(`${api}gdp_co2`);
    if (response.ok) {
      return await response.json();
    } else {
      console.error("Failed to fetch data");
      return {};
    }
  },
  generateYearData() {
    for (let year = this.firstYear; year <= this.lastYear; year++) {
      let data = [];
      this.yearData[year] = data;

      let i = 0;
      am5.object.each(this.countries, (id, country) => {
        let dObj = {
          id: id,
          name: country.name,
          continent: this.rawYearData[year][i], // Assuming you have a method to get the continent
          settings: { fill: this.colors[this.rawYearData[year][i].continent] },
          x: this.rawYearData[year][i].x,
          y: this.rawYearData[year][i].y,
          value: this.rawYearData[year][i].y,
        };
        data.push(dObj);
        country.data = [dObj];
        i++;
      });
    }
  },
  updateSeriesData(year) {
    if (this.currentYear !== year) {
      this.currentYear = year;
      let data = this.yearData[year];

      if (data && data.length > 0) {
        let i = 0;
        am5.array.each(data, (item) => {
          this.bubbleSeries.data.setIndex(i, item);
          i++;
        });
      } else {
        console.error("No data available for the year:", year);
      }

      this.yearLabel.set("text", year.toString());
    }
  },
  async initializeChart() {
    let root = am5.Root.new("chartdiv_MotionChart");

    root.setThemes([am5themes_Animated.new(root)]);

    this.generateYearData();

    let mainContainer = root.container.children.push(am5.Container.new(root, {
      width: am5.p100,
      height: am5.p100,
      layout: root.verticalLayout
    }));

    let chart = mainContainer.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelY: "zoomXY",
      pinchZoomX: true,
      pinchZoomY: true
    }));

    let xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
      min: 0,
      max: 6200,
      renderer: am5xy.AxisRendererX.new(root, { minGridDistance: 50 }),
      tooltip: am5.Tooltip.new(root, {})
    }));

    xAxis.children.push(am5.Label.new(root, { text: "Co2 Emissions", x: am5.p50, centerX: am5.p50 }));

    let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
      min: 0,
      max: 100,
      renderer: am5xy.AxisRendererY.new(root, {}),
      tooltip: am5.Tooltip.new(root, {})
    }));

    yAxis.children.moveValue(am5.Label.new(root, {
      text: "GDP",
      rotation: -90,
      y: am5.p50,
      centerX: am5.p50
    }), 0);

    this.bubbleSeries = chart.series.push(am5xy.LineSeries.new(root, {
      calculateAggregates: true,
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "y",
      valueXField: "x",
      valueField: "value"
    }));

    this.bubbleSeries.strokes.template.set("visible", false);

    let circleTemplate = am5.Template.new({ tooltipY: 0 });
    circleTemplate.states.create("transparent", { opacity: 0.15 });

    circleTemplate.events.on("pointerover", this.handleOver);
    circleTemplate.events.on("pointerout", this.handleOut);
    circleTemplate.events.on("click", this.handleClick);

    this.bubbleSeries.bullets.push(() => {
      let bulletCircle = am5.Circle.new(root, {
        radius: 5,
        templateField: "settings",
        fillOpacity: 0.9,
        tooltipText: "[fontSize:18px; bold]{name}[/]\nCo2 emissions: {valueY} tonnes per person\nCo2 emissions: {valueX} million tonnes",
      }, circleTemplate);
      return am5.Bullet.new(root, {
        sprite: bulletCircle
      });
    });

    this.bubbleSeries.set("heatRules", [{
      target: circleTemplate,
      min: 3,
      max: 6,
      dataField: "value",
      key: "radius", maxValue: 10
    }]);

    let lineSeries = chart.series.push(am5xy.LineSeries.new(root, {
      valueXField: "x",
      valueYField: "y",
      xAxis: xAxis,
      yAxis: yAxis,
      stroke: am5.color(0x00000)
    }));

    lineSeries.strokes.template.set("strokeOpacity", 0.3);

    lineSeries.bullets.push(() => {
      let bulletCircle = am5.Circle.new(root, {
        radius: 2,
        fill: lineSeries.stroke
      });
      return am5.Bullet.new(root, {
        sprite: bulletCircle
      });
    });

    chart.set("cursor", am5xy.XYCursor.new(root, {
      xAxis: xAxis,
      yAxis: yAxis,
      snapToSeries: [this.bubbleSeries]
    }));

    chart.set("scrollbarX", am5.Scrollbar.new(root, {
      orientation: "horizontal",
      exportable: false
    }));

    chart.set("scrollbarY", am5.Scrollbar.new(root, {
      orientation: "vertical",
      exportable: false
    }));

     this.yearLabel = chart.plotContainer.children.push(am5.Label.new(root, {
      text: this.currentYear.toString(),
      fontSize: "10em",
      fill: am5.color(0x000000),
      opacity: 0.15,
      x: am5.p50,
      y: am5.p50,
      fontFamily: "Courier New",
      textAlign: "right",
      centerY: am5.p50,
      centerX: am5.p50
    }));

    let yearSliderContainer = mainContainer.children.push(am5.Container.new(root, {
      width: am5.percent(100),
      layout: root.horizontalLayout,
      paddingLeft: 70,
      paddingRight: 40,
      exportable: false
    }));

    let playButton = yearSliderContainer.children.push(am5.Button.new(root, {
      themeTags: ["play"],
      centerY: am5.p50,
      marginRight: 20,
      icon: am5.Graphics.new(root, {
        themeTags: ["icon"]
      })
    }));

    playButton.events.on("click", () => {
      if (playButton.get("active")) {
        slider.set("start", slider.get("start") + 0.0001);
      } else {
        slider.animate({
          key: "start",
          to: 1,
          duration: 30000 * (1 - slider.get("start"))
        });
      }
    });

    let slider = yearSliderContainer.children.push(am5.Slider.new(root, {
      orientation: "horizontal",
      start: 0,
      centerY: am5.p50
    }));

    slider.on("start", (start) => {
      if (start === 1) {
        playButton.set("active", false);
      }
    });

    slider.events.on("rangechanged", () => {
      this.updateSeriesData(
        this.firstYear + Math.round(slider.get("start", 0) * (this.lastYear - this.firstYear))
      );
    });

    let navMap = chart.plotContainer.children.push(am5map.MapChart.new(root, {
      projection: am5map.geoNaturalEarth1(),
      rotationX: -11,
      width: 250,
      height: 150,
      x: am5.percent(100),
      y: am5.percent(100),
      centerY: am5.percent(100),
      centerX: am5.percent(100),
      panY: "none",
      panX: "none"
    }));

     this.polygonSeries = navMap.series.push(am5map.MapPolygonSeries.new(root, {
      geoJSON: am4geodata_continentsLow,
      exclude: ["antarctica"]
    }));

    let polygonTemplate = this.polygonSeries.mapPolygons.template;

    polygonTemplate.setAll({
      templateField: "settings",
      tooltipText: "{name}",
      interactive: true
    });

    polygonTemplate.states.create("disabled", {
      fill: root.interfaceColors.get("disabled")
    });

    polygonTemplate.events.on("pointerover", this.handleContinentOver);
    polygonTemplate.events.on("click", this.handleContinentClick);
    polygonTemplate.events.on("pointerout", this.handleOut);

    this.polygonSeries.data.setAll([
      { id: "europe", code: "EU", settings: { fill: this.colors.EU } },
      { id: "northAmerica", code: "NA", settings: { fill: this.colors.NA } },
      { id: "southAmerica", code: "SA", settings: { fill: this.colors.SA } },
      { id: "asia", code: "AS", settings: { fill: this.colors.AS } },
      { id: "africa", code: "AF", settings: { fill: this.colors.AF } },
      { id: "oceania", code: "OC", settings: { fill: this.colors.OC } }
    ]);

    await this.updateSeriesData(this.currentYear);
    const rawData = toRaw(this.yearData[this.currentYear]);
    console.log(rawData);
    this.bubbleSeries.data.setAll(rawData);
    this.bubbleSeries.appear(1000);
    chart.appear(1000, 100);
  },
  handleOver(e) {
    let target = e.target;
    am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
      if (dataItem.bullets) {
        let bullet = dataItem.bullets[0];
        if (bullet) {
          let sprite = bullet.get("sprite");
          if (sprite && sprite != target) {
            sprite.states.applyAnimate("transparent");
          }
        }
      }
    });
  },
  handleOut(e) {
    am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
      if (dataItem.bullets) {
        let bullet = dataItem.bullets[0];
        if (bullet) {
          let sprite = bullet.get("sprite");
          if (sprite) {
            sprite.states.applyAnimate("default");
          }
        }
      }
    });
  },
  handleClick(e) {
    if (selectedDataItem == e.target.dataItem) {
      am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
        let bullet = dataItem.bullets[0];
        let sprite = bullet.get("sprite");
        sprite.set("fillOpacity", 1);
      });
      lineSeries.data.clear();
    } else {
      selectedDataItem = e.target.dataItem;

      lineSeries.data.setAll(this.countries[selectedDataItem.dataContext.id].data);
      lineSeries.show();

      am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
        let bullet = dataItem.bullets[0];
        let sprite = bullet.get("sprite");
        if (dataItem != selectedDataItem) {
          sprite.set("fillOpacity", 0.15);
        } else {
          sprite.set("fillOpacity", 1);
        }
      });
    }
  },
  handleContinentOver(e) {
    let target = e.target;
    am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
      if (dataItem.bullets) {
        let bullet = dataItem.bullets[0];
        if (bullet) {
          let sprite = bullet.get("sprite");
          if (sprite) {
            if (target.dataItem.dataContext.code == sprite.dataItem.dataContext.continent) {
              sprite.states.applyAnimate("default");
            } else {
              sprite.states.applyAnimate("transparent");
            }
          }
        }
      }
    });
  },
  handleContinentClick(e) {
    let target = e.target;
    if (target.dataItem == selectedContinent) {
      selectedContinent = undefined;

      am5.array.each(this.polygonSeries.dataItems, (dataItem) => {
        let mapPolygon = dataItem.get("mapPolygon");
        mapPolygon.states.applyAnimate("default");
      });

      am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
        let bullet = dataItem.bullets[0];
        if (bullet) {
          let sprite = bullet.get("sprite");
          if (sprite) {
            sprite.set("forceHidden", false);
          }
        }
      });
    } else {
      selectedContinent = target.dataItem;

      am5.array.each(this.polygonSeries.dataItems, (dataItem) => {
        let mapPolygon = dataItem.get("mapPolygon");
        if (dataItem != selectedContinent) {
          mapPolygon.states.applyAnimate("disabled");
        } else {
          mapPolygon.states.applyAnimate("default");
        }
      });

      am5.array.each(this.bubbleSeries.dataItems, (dataItem) => {
        if (dataItem.bullets) {
          let bullet = dataItem.bullets[0];
          let sprite = bullet.get("sprite");
          if (target.dataItem.dataContext.code == sprite.dataItem.dataContext.continent) {
            sprite.set("forceHidden", false);
          } else {
            sprite.set("forceHidden", true);
          }
        }
      });
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
#chartdiv_MotionChart {
  width: 100%;
  height: 700px;
  max-width: 100%;
}

#chartdivContainer_MotionChart {
  position: relative;
  justify-content: center;
  width: 100%;
  height: 900px;
  padding: 140px 0 60px 0;
}
</style>