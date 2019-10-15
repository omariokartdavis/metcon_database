$(document).ready(function() {
	var ctx = document.getElementById('bodyweight_chart_id').getContext('2d');
	var chart = new Chart(ctx, {
		type: 'line',		
		
		data: {
			labels: bodyweight_date,
			datasets: [{
				label: 'Bodyweight',
				backgroundColor: 'rgb(102, 178, 178)',
				borderColor: 'rgb(102, 178, 178)',
				data: bodyweight_weight,
				fill: false, // controls if the area under the line is filled in
				lineTension: 0, //this changes the curvature of the line. default no value is 0.4
			}]
		},

		options: {
			hover: {
				mode: 'nearest',
				intersect: true,
				animationDuration: 0,
			},
			animation: {
				duration: 0
			},
			responsiveAnimationDuration: 0
		}
	});
	//console.log(bodyweight_weight);
	//console.log(bodyweight_date);
});