const showDonutChart = ({
    ressource,
    color,
    data,
    tooltip,
    ressourceSpark,
    ressourceSparkData
}) => {
    let donutConfig = $().c3ChartDefaults().getDefaultDonutConfig('A');
    donutConfig.bindto = ressource;
    donutConfig.color = color;
    donutConfig.data = data;
    donutConfig.tooltip = tooltip;

    // Generate the donut chart
    c3.generate(donutConfig);

    let donutChartTitle = d3.select(ressource).select(
        'text.c3-chart-arcs-title');
    donutChartTitle.text("");
    donutChartTitle.insert('tspan').text("1100").classed('donut-title-big-pf',
        true).attr('y', 0).attr('x', 0);
    donutChartTitle.insert('tspan').text("Gbps Used").classed(
        'donut-title-small-pf', true).attr('y', 20).attr('x', 0);

    let sparklineConfig = $().c3ChartDefaults().getDefaultSparklineConfig();
    sparklineConfig.bindto = ressourceSpark;
    sparklineConfig.data = ressourceSparkData;
    c3.generate(sparklineConfig);
};

const networkChartConfig = {
    ressource: "#chart-pf-donut-8",
    color: {
        pattern: ["#EC7A08", "#D1D1D1"]
    },
    data: {
        type: "donut",
        columns: [
            ["Used", 85],
            ["Available", 15]
        ],
        groups: [
            ["used", "available"]
        ],
        order: null
    },
    tooltip: {
        contents: function (d) {
            return '<span class="donut-tooltip-pf" style="white-space: nowrap;">' +
                Math.round(d[0].ratio * 100) + '%' + ' Gbps ' + d[0]
                    .name +
                '</span>';
        }
    },
    ressourceSpark: "#chart-pf-sparkline-8",
    ressourceSparkData: {
        columns: [
            ['%', 60, 55, 70, 44, 31, 67, 54, 46, 58, 75, 62, 68, 69,
                88, 74, 88, 85
            ],
        ],
        type: 'area'
    }
};


const memoryCharConfig = {
    ressource: '#chart-pf-donut-7',
    color: {
        pattern: ["#3f9c35", "#D1D1D1"]
    },
    data: {
        type: "donut",
        columns: [
            ["Used", 41],
            ["Available", 59]
        ],
        groups: [
            ["used", "available"]
        ],
        order: null
    },
    tooltip: {
        contents: function (d) {
            return '<span class="donut-tooltip-pf" style="white-space: nowrap;">' +
                Math.round(d[0].ratio * 100) + '%' + ' GB ' + d[0]
                    .name +
                '</span>';
        }
    },
    ressourceSpark: '#chart-pf-sparkline-7',
    ressourceSparkData: {
        columns: [
            ['%', 35, 36, 20, 30, 31, 22, 44, 36, 40, 41, 55, 52, 48,
                48, 50, 40, 41
            ],
        ],
        type: 'area'
    }
}

const cpuChartConfig = {
    ressource: '#chart-pf-donut-6',
    color: {
        pattern: ["#cc0000", "#D1D1D1"]
    },
    data: {
        type: "donut",
        columns: [
            ["Used", 95],
            ["Available", 5]
        ],
        groups: [
            ["used", "available"]
        ],
        order: null
    },
    tooltip: {
        contents: function (d) {
            return '<span class="donut-tooltip-pf" style="white-space: nowrap;">' +
                Math.round(d[0].ratio * 100) + '%' + ' MHz ' + d[0]
                    .name +
                '</span>';
        }
    },
    ressourceSpark: '#chart-pf-sparkline-6',
    ressourceSparkData: {
        columns: [
            ['%', 10, 50, 28, 20, 31, 27, 60, 36, 52, 55, 62, 68, 69,
                88, 74, 88, 95
            ],
        ],
        type: 'area'
    }
};

const diskChartConfig = {
    ressource: '#disk',
    color: {
        pattern: ["#cc0000", "#D1D1D1"]
    },
    data: {
        type: "donut",
        columns: [
            ["Used", 95],
            ["Available", 5]
        ],
        groups: [
            ["used", "available"]
        ],
        order: null
    },
    tooltip: {
        contents: function (d) {
            return '<span class="donut-tooltip-pf" style="white-space: nowrap;">' +
                Math.round(d[0].ratio * 100) + '%' + ' MHz ' + d[0]
                    .name +
                '</span>';
        }
    },
    ressourceSpark: '#disk-spark',
    ressourceSparkData: {
        columns: [
            ['%', 10, 50, 28, 20, 31, 27, 60, 36, 52, 55, 62, 68, 69,
                88, 74, 88, 95
            ],
        ],
        type: 'area'
    }
};

console.log("Here we are!");

// Display Network Donut chart
showDonutChart(diskChartConfig);
showDonutChart(cpuChartConfig);
showDonutChart(memoryCharConfig);
showDonutChart(networkChartConfig);