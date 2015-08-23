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


var startTime = new Date().getTime();
var request = $.getJSON('json/NORMAL_5X5_NA.json');
var champs = [];

request.done(function(data) {
	champs = data;
	$('#container').highcharts({
		'chart': {
			'type': 'columnrange',
			'zoomType': 'x'
		},
		'title': {
			'text': 'Change in Pick Rates after Patch 5.14'
		},

		'xAxis': {
			'categories': getCategories(champs),
			'min': 0
		},

		'yAxis': {
			'title': {
				'text': 'Win Rate'
			}
		},
		'legend': {
			'enabled':false
		},
		
		'series': [{
			'data': getWinSeries(champs)
		}],
		'tooltip': {
			'formatter': function() {
				// if color is red, 5.11 > 5.14 and there's a decrease
				if (this.point.color == 'red') { 
					return '<em>' + this.point.category + '</em><br>5.11 winrate: ' + roundOff(this.point.high) + '%<br>5.14 winrate: ' + roundOff(this.point.low) + '%<br>Change in winrate: ' + roundOff(this.point.low-this.point.high)+'%';
				}
				// if color is not red, 5.11 < 5.14 and there's an increase
				return '<em>'+this.point.category + '</em><br>5.11 winrate: ' + roundOff(this.point.low) + '%<br>5.14 winrate: ' + roundOff(this.point.high) + '%<br>Change in winrate: +' + roundOff(this.point.high-this.point.low)+'%';
			}
		}
	});
	console.log('Initialization done in ' + (new Date().getTime()-startTime) + ' ms.');
}); 

$('#btn').click(function() {
	//sample sort with time taken
	var start = new Date().getTime();
	champs = champs.sort(sortByProperty('wins'));
	var chart = $('#container').highcharts();
	chart.xAxis[0].setCategories(getCategories(champs));
	chart.series[0].setData(getWinSeries(champs));
	chart.series[0].update(chart.series[0].options);
	console.log('Update done in ' + (new Date().getTime()-start) + ' ms.');
});
});

// returns a callback function for Arrays.sort which will sort by one of the object's properties
function sortByProperty(property) {
	return function(a,b) {
		if (a[property] < b[property]) {
			return -1;
		} else if (a[property] > b[property]) {
			return 1;
		}
		return 0;
	}
}

function getCategories(champs) {
	var categories = [];
	for (var i = 0; i < champs.length; i++) {
		categories.push(champs[i].name);
	}
	return categories;
}

function roundOff(num) {
	return parseFloat((Math.round(num*100)/100).toFixed(2));
}

function getWinSeries(champs) {
	var series = [];
	for (var i = 0; i < champs.length; i++) {
		var pre = roundOff(champs[i]['5.11']['wins']/champs[i]['5.11']['picks']*100);
		var post = roundOff(champs[i]['5.14']['wins']/champs[i]['5.14']['picks']*100);
		if (pre < post) {
			series.push({
				'low':pre, 'high':post, 'color':'green'
			});
		} else if (pre > post) {
			series.push({
				'low':post, 'high':pre, 'color':'red'
			});
		} else {
			series.push({
				'low':pre, 'high':post, 'color':'grey'
			})
		}
	}
	return series
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
/*
TODO
- set minimum size/padding so that all element names are visible along the bottom (may need to be zoomed in initially)
- set maximum zoom size
- set tooltip to appear for the value of whichever x the cursor is over (rather than require users to hover the bar in the y-axis as well)
- make sortable by increasing change in rate, overall rate before, overall rate after (might require a JSON refactor since sortByProperty() requires direct 'children' of each JSON object. it would potentially save processing overhead to have rates pre-calculated in JSON)
- make modular for other rates (pick, ban)
- make modular for other data sets (region and queue type)
*/