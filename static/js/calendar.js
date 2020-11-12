colors = [
  "#ff5252",
  "#29b6f6",
  "#81c784",
  "#ffeb3b",
  "#40c4ff",
  "#673ab7",
  "#d32f2f",
  "#00e676",
  "#ff9800",
  "#cddc39",
];

function util_get_dataset(data) {
  var datasets = [];

  data.forEach(function (item, index) {
    var course = item;
    var days = [
      course[1].search('M'),
      course[1].search('Tu'),
      course[1].search('W'),
      course[1].search('Th'),
      course[1].search('F')
    ];

    var data = [];
    for (var i = 0; i < 5; i++) {
      end_pm = course[3].substring(6, 9) == 'PM' ? 12 : 0;
      start_pm = course[2].substring(6, 9) == 'PM' ? 12 : 0;
      if (days[i] > -1) {
        data.push(
          Math.abs(Math.round(
            (parseFloat(
              (parseInt(course[3].substring(0, 2)) + end_pm)
                + '.' + course[3].substring(3, 5)) - end_pm)
              - (parseFloat((parseInt(course[2].substring(0, 2)) + start_pm)
                + '.' + course[2].substring(3, 5)) - start_pm)*100)/100))
      } else {
        data.push(
          0
        )
      }
    }

    datasets.push({
      data: data,
      label: course[0],
      backgroundColor: colors[index],
      fill: true,
      steppedLine: true
    });
  });

  return datasets;
}

function timeReq(data) {
  var datasets = util_get_dataset(data);

  var ctx = document.getElementById("timeRequirements");
  ctx.height = 80;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      datasets: datasets
    },
    options: {            
      title: {
        display: true,
        text: 'Minimum class time requirements'
      },
      tooltips: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(item) { return datasets[item.datasetIndex].label.padEnd(10, ' ') + ' ' + item.yLabel.toString().padStart(4, ' ') + " hours"; }
        }
      },
      responsive: true,
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'hour'
          }
        },
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true,
          scaleLabel: {
            display: true,
            labelString: 'Total daily class time (in hours)'
          },
          ticks: {
            beginAtZero: true,
            suggestedMax: 8
          }
        }]
      }
    }
  });
}


function weeklySchedule(data) {
  console.log(data);

  var datasets = [];
  data.forEach(function (item, index) {
    var course = item;
    var days = [
      course[1].search('M'),
      course[1].search('Tu'),
      course[1].search('W'),
      course[1].search('Th'),
      course[1].search('F')
    ];

    var data = [];
    for (var i = 0; i < 5; i++) {
      start_pm = course[2].substring(6, 9) == 'PM' ? 12 : 0;
      if (days[i] > -1) {
        data.push(
          Math.abs(Math.round(
            (parseFloat(
              (parseInt(course[2].substring(0, 2)) + start_pm)
                + '.' + course[2].substring(3, 5)))*100)/100))
      } else {
        data.push(
          0
        )
      }
    }

    datasets.push({
      data: data,
      label: course[0],
      backgroundColor: 'rgba(.8, .8, .8, .075)',
      borderColor: colors[index],
      pointBackgroundColor: colors[index],
      fill: true,
      steppedLine: 'middle'
    });
  });

  var ctx = document.getElementById("weeklySchedule");
  ctx.height = 100;
  new Chart(ctx, {
    type: 'line',
    tooltips: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(item) {
            return item.yLabel + 'hours';
          }
        }
      },
    data: {

      labels: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      datasets: datasets
      },
      options: {
        title: {
          display: true,
          text: 'Weekly Class Schedule'
        },
        tooltips: {
          callbacks: {
            label: function(item) {
              var hour = Math.round(item.yLabel);
              var minute = Math.round(item.yLabel*100)%100;
              var am_pm = hour >= 12 ? ' PM' : ' AM';
              console.log(item);
              return datasets[item.datasetIndex].label.padEnd(10, ' ') + '  ' +
                hour.toString().padStart(2, '0') + ":" + minute.toString().padStart(2, '0') + am_pm;
            }
          }
        },
        responsive: true,
        scales: {
          yAxes: [{
              ticks: {
                  min: 0,
                  max: 23,
                  stepSize: 1,
                  callback: function(label, index, labels) {
                      var am_pm = label >= 12 ? ' PM' : ' AM';
                      return label.toString().padStart(2, '0') + ':00' + am_pm;
                  }
              },
              scaleLabel: {
                display: true,
                labelString: 'Timeline of a day'
              },
          }]
      }
    }
  });
}