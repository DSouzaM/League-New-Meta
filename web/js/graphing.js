var dataTypes = ['CHAMPIONS','ITEMS'];
var queueTypes = ['NORMAL_5X5', 'RANKED_SOLO'];
var regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']

// object to keep track of what data should be shown on the graph
var selection = {'data':'','queue':[], 'region':[] };

$(function() {
// function to handle checkbox actions
$('input[type=checkbox]').change(function() {
	var name = this.name;
	var value = this.value;

		//check action
		if ($(this).attr('checked')){
			if (value == 'ALL') {
				//selects all checkboxes with the given name, checks them, and adds them to the according selection array
				$('input[type=checkbox][name=' + name + ']').each(function() {
					$(this).attr('checked',true);
					if (this.value != 'ALL' && selection[this.name].indexOf(this.value) < 0) {
						selection[this.name].push(this.value);
					}
				});
			} else {
				//pushes value to according selection array
				selection[name].push(value);
			}
		}

		//uncheck action
		else {
			if (value == 'ALL') {
				//selects all checkboxes with the given name, unchecks them, and removes them from the according selection array
				$('input[type=checkbox][name=' + name + ']').each(function() {
					$(this).attr('checked',false);
					if (selection[this.name].indexOf(this.value) >= 0) {
						selection[this.name].splice(selection[this.name].indexOf(this.value),1);
					}
				});
			} else {
				//removes value from according selection array
				selection[name].splice(selection[name].indexOf(value),1);
				$('input[type=checkbox][name=' + name + '][value=ALL]').attr('checked',false);
			}
		}

		//TODO add graph button and later add functionality for other data types
		selection['data'] = 'CHAMPIONS';
		getDataSet(selection);
	});


	/*
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
		champs = champs.sort(sortDescend);
		
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
}); */
});

//function used by Array.sort to sort arrays of data objects in descending order
function sortDescend(a,b) {
	if (a.data[0] > b.data[0]) {
		return -1;
	} else if (a.data[0] == b.data[0]) {
		return 0;
	} else {
		return 1;
	}
}



function getDataSet(selection) {

	//input sanitation
	var dataType = selection['data'].toUpperCase()
	var queueList = [];
	$.each(selection['queue'], function(index, queue){
		queueList.push(queue.toUpperCase());
	})
	var regionList = [];
	$.each(selection['region'], function(index, region) {
		regionList.push(region.toUpperCase());
	})

	//input validation
	if (dataType=='' || dataTypes.indexOf(dataType)<0 || queueList.length==0 ||  !queueList.every(function(queue){
		return (queueTypes.indexOf(queue)>=0);
	}) || regionList.length==0 || !regionList.every(function(region) {
		return (regions.indexOf(region)>=0);
	})) {
		console.log('Invalid data set request:\ndataType: ' + dataType + '\nqueueList: ' + queueList + '\nregionList: ' + regionList);
	}
	else {

	//compiles array of required JSON files
	var jsons = [];
	for (var i = 0; i < queueList.length; i++) {
		for (var j = 0; j < regionList.length; j++) {
			jsons.push(dataType+'_'+queueList[i]+'_'+regionList[j]+'.json');
		}
	}
	console.log(jsons);
}
}
