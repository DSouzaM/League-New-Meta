var dataTypes = ['CHAMPIONS','ITEMS'];
var queueTypes = ['NORMAL_5X5', 'RANKED_SOLO'];
var regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']

$(function() {
	var startTime = new Date().getTime();
	var request = $.getJSON('json/NORMAL_5X5_NA.json');
	var chart;
	var champs = [];
	request.done(function(data) {
		
		for (var i = 0; i<data.length; i++) {
			champs.push({name:data[i].name, data:[data[i].picks]});
		}
		console.log(champs);
		chart = $('#container').highcharts();
		/*champs = champs.sort(sortDescend);*/
		
		console.log('done in ' + (new Date().getTime()-startTime) + ' ms');

		$('#container').highcharts({
			chart: {
				type: 'column',
				zoomType: 'x'
			},
			title: {
				text: 'Change in Pick Rates after Patch 5.14'
			},
			xAxis: {
				categories: ['Champion'],
				min: 0
			},
			yAxis: {
				title: {
					text: 'Percentage change'
				},
			},

			plotOptions: {
				series: {
					pointPadding: 0.00,
					groupPadding: 0.1
				}
			},
			series: champs,
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

function getDataSet(dataType, queueList, regionList) {
	if (dataTypes.indexOf(dataType.toUpperCase())<0 || !queueList.every(function(queue){
		return (queueTypes.indexOf(queue.toUpperCase())>=0);
	}) || !regionList.every(function(region) {
		return (regions.indexOf(region.toUpperCase())>=0);
	})) {
		console.log("Invalid data set request:\ndataType: " + dataType + "\nqueueList: " + queueList + "\nregionList: " + regionList);
	}
	else {
		console.log("Valid data set request.");
	}

	//var jsons = [];

}
