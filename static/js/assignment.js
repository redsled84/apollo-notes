/*

  Copyright 2020 Lucas Bernard Black

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

*/

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

function scatterAssignment(json_data, classes) {
    var ctx = document.getElementById("scatterAssignment");
    ctx.height = window.innerHeight * .3;

    // Define the data
    var datasets = [];
    var months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "Jun": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    // inefficient but works for now
    for (var j = 0; j < classes.length; j++) {
        var tempset = {
            label: classes[j][0],
            data: [],
            borderColor: colors[j],
            baclgroundColor: colors[j]
        }
        for (var i = 0; i < json_data.length; i++) {
            if (classes[j][4] == json_data[i][0]) {
                tempset.data.push({
                    x: months[json_data[i][1].substring(0,3)] * 30 + Number(json_data[i][1].substring(4, 6)),
                    y: json_data[i][2] * 100
                });
            }
        }
        datasets.push(tempset);
    }

    var options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    callback: function(label, index, labels) {
                        return label.toString() + "%";
                    }
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Grade of assignment'
                },
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Approximate day of the year'
                }
            }]
        },
        tooltips: {
          callbacks: {
            label: function(item, data) {
              return '(' + item.label.toString() + ', ' + item.value.toString() + '%)';
            }
          }
        }
    };

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: datasets
        },
        options: options
    });
};