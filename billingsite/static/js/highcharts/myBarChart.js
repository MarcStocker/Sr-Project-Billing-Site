Highcharts.chart('graphDiv', {
    data: {
      table: 'OverviewTable',
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
      allowDecimals: true,
      labels: {
        style:{fontSize: '18px'},
        formatter: function() {
          return '$' + this.value;
        }
      },
      title: { text: '' }
    },
    plotOptions: {
      column: {
        borderWidth: 0,
        dataLabels: {
          format: '-${point.y:.2f}',
          style : {fontSize: '30px'},
          enabled: true
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
