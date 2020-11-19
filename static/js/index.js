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

function chart(data) {
  console.log(data);

  var ctx = document.getElementById("todaySchedule");
  ctx.height = 80;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        "8:00 AM",
        "8:30 AM",
        "9:00 AM",
        "9:30 AM",
        "10:00 AM",
        "10:30 AM",
        "11:00 AM",
        "11:30 AM",
        "12:00 PM",
        "12:30 PM",
        "1:00 PM",
        "1:30 PM",
        "2:00 PM",
        "2:30 PM",
        "3:00 PM",
        "3:30 PM",
        "4:00 PM",
        "4:30 PM",
        "5:00 PM",
        "5:30 PM",
        "6:00 PM",
        "6:30 PM",
        "7:00 PM",
        "7:30 PM",
        "8:00 PM",
        "8:30 PM",
        "9:00 PM",
        "9:30 PM"
      ],
      datasets: [{ 
          data: [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          label: "CS 202",
          borderColor: "#3e95cd",
          fill: true,
          steppedLine: true
        }, { 
          data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          label: "PHYS 181",
          borderColor: "#8e5ea2",
          fill: true,
          steppedLine: true
        }
      ]
      },
      options: {
      title: {
        display: true,
        text: 'Daily class schedule (in hours)'
      },
      scales: {
          yAxes: [{
              ticks: {
                  min: 0,
                  max: 1,
                  stepSize: 1
              }
          }]
      }
    }
  });
}