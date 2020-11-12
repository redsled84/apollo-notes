function chart(data) {
    console.log(data);

    var ctx = document.getElementById("weeklySchedule");
    ctx.height = 80;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [
                "Saturday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Sunday"
            ],
            datasets: [{ 
                    data: [0, 0, 0, 0, 0, 0, 0],
                    label: "CS 202",
                    borderColor: "#3e95cd",
                    fill: true,
                    steppedLine: true
                }, { 
                    data: [0, 0, 0, 0, 0, 0, 0],
                    label: "PHYS 181",
                    borderColor: "#8e5ea2",
                    fill: true,
                    steppedLine: true
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    stacked: true,
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    },
                }]
            }
        }
    });
}