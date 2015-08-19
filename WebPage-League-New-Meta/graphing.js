$(function() {
	var startTime = new Date().getTime();
	var chart = $('#container').highcharts();
	var pre = $.getJSON('v5.11_NORMAL_5V5_NA.json');
	var post = $.getJSON('v5.14_NORMAL_5V5_NA.json');
	var champs = [];
	$.when(pre, post).done(function(pre,post) {
		pre = pre[0];
		post = post[0];

		for (var i = 0; i<50; i++) {
			champs.push({name:pre[i].fields.name, data:[(post[i].fields.picks-pre[i].fields.picks)]});
		}
		console.log(champs);
		//chart.series[0].setData(champs.map(function(champ) {
		//	return {name:champ.name,data:champ.dPick};
		//}));
	console.log('done in ' + (new Date().getTime()-startTime) + ' ms');

	$('#container').highcharts({
		chart: {
			type: 'column'
		},
		title: {
			text: 'Pick Rates'
		},
		xAxis: {
			categories: ['Pick Rate']
		},
		yAxis: {
			title: {
				text: 'Fruit eaten'
			}
		},
		series: champs
	});

});

});


