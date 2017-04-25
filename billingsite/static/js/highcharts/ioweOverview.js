Highcharts.chart('userpaymentOverview', {
    data: {
        table: 'ioweTable'
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
            text: 'Total Owed'
        }
    },
    plotOptions: {
      column: {
            // borderWidth = 0,
            dataLabels: {
                enabled: true,
                format: '${point.y:.2f}',
            },
            enableMouseTracking: false
        }
    },
    legend: {
      enabled: false
   },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                '$' + this.point.y + ' ' + this.point.name.toLowerCase();
        }
    }
});
