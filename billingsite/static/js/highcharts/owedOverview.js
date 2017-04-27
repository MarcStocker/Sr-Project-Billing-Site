Highcharts.chart('IamOwedGraph', {
    data: {
        table: 'ImOwedTable'
    },
    chart: {
        type: 'column'
    },
    title: {
        text: ''
    },
    xAxis: {
      labels: {
        style: { fontSize: '26px' },
      }
    },
    yAxis: {
        labels: {
          style:{fontSize: '14px'},
          formatter: function() {
            return '$' + this.value;
          }
        },
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
                style : {fontSize: '30px'},
            },
            enableMouseTracking: true
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
