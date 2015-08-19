$(function() {
	var startTime = new Date().getTime();
	var request = $.getJSON('json/NORMAL_5X5_NA.json');
	var chart;
	var champ_names = [];
	var champ_picks = [];
	var champ_wins = [];
	
	request.done(function(data) {

		for (var i = 0; i<data.length; i++) {
			champ_names.push(data[i].name);
			champ_picks.push(data[i].picks);
			champ_wins.push(data[i].wins);
		}
		chart = $('#container').highcharts();
		/*champs = champs.sort(sortDescend);*/
		
		console.log('done in ' + (new Date().getTime()-startTime) + ' ms');

		$('#container').highcharts({
			chart: {
				type: 'column'
			},
			credits: {
			    enabled: false
			},
			title: {
				text: 'Change in Pick Rates after Patch 5.14'
			},
			xAxis: {
				categories: champ_names
			},
			yAxis: {
				title: {
					text: 'Percentage change'
				},
			},
			plotOptions: {
		    		series: {
		    		    pointPadding: 0.00,
		    		    groupPadding: 0.2
		  		}
			},
			series: [{
			    name: 'Picks',
			    data: champ_picks
			}, {
			    name: 'Wins',
			    data: champ_wins
			}],
			tooltip: {
			    valueSuffix: '%'
			}
		});

	});
});

function sortDescend(a,b) {
	if (a.data[0] > b.data[0]) {
		return -1;
	} else if (a.data[0] == b.data[0]) {
		return 0;
	} else {
		return 1;
	}
}
