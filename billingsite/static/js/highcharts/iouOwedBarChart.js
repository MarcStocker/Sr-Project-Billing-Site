Highcharts.chart('iouOwed', {
   data: {
      table: 'iouOwedTable'
   },
   chart: {
      type: 'bar'
   },
   title: {
      text: 'I owe'
   },
   legend: {

   },
   xAxis: [{
      min: 0,
      reversed: true,
      title: {
         text: ''
      }
   }, {
      reversed: true,
      title: {
         text: ''
      },
      opposite: true
   }],
   tooltip: {
      shared: true
   },
   plotOptions: {
      bar: {
         grouping: false,
         shadow: false,
         borderWidth: 0
      }
   },
});
