Highcharts.chart('graphDiv', {
    data: {
        table: 'OverviewTable'
    },
    chart: {
        type: 'column'
    },
    title: {
        text: ''
    },
    yAxis: {
        allowDecimals: true,
        title: {
            text: '$ Dollars $'
        }
    },
    plotOptions: {
      column: {
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: false
        }
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                '$' + this.point.y + ' ' + this.point.name.toLowerCase();
        }
    }
});
