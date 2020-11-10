/*
	TODO: Collect data from SQLite3 db and feed through this chart
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