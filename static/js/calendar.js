colors = [
    "#e91e63",
    "#2196f3",
    "#cddc39",
    "#673ab7",
    "#4caf50",
    "#ffeb3b",
    "#40c4ff",
    "#d32f2f",
    "#00e676",
    "#ff9800"
];

function chart(data) {
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
                    label: function(item) { return item.yLabel + " hours"; }
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