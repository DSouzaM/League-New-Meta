$(function() {
	var startTime = new Date().getTime();
	var chart = $('#container').highcharts();
	var pre = $.getJSON('v5.11_NORMAL_5V5_NA.json');
	var post = $.getJSON('v5.14_NORMAL_5V5_NA.json');
	var champs = [];
	$.when(pre, post).done(function(pre,post) {
		pre = pre[0];
		post = post[0];

		for (var i = 0; i<pre.length; i++) {
			if (pre[i].fields.picks != 0 && post[i].fields.picks != 0)
				champs.push({name:pre[i].fields.name, data:[((post[i].fields.picks/pre[i].fields.picks)-1)*100]});
		}
		console.log(champs);
		champs = champs.sort(sortDescend);
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

function sortDescend(a,b) {
	if (a.data[0] > b.data[0]) {
		return -1;
	} else if (a.data[0] == b.data[0]) {
		return 0;
	} else {
		return 1;
	}
}
