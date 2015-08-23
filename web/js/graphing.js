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
var dataSet = [];

request.done(function(data) {
	dataSet = data;
	$('#container').highcharts({
		'chart': {
			'type': 'columnrange',
			'zoomType': 'x'
		},
		'title': {
			'text': 'Change in Pick Rates after Patch 5.14'
		},

		'xAxis': {
			'categories': getArrayOf(dataSet,'name'),
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
			'data': setDataSet(dataSet,'prepost','wr')//getSeries(dataSet,'')
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
	dataSet.sort(sortByProperty('d_wr'));	
	var chart = $('#container').highcharts();
	chart.xAxis[0].setCategories(getArrayOf(dataSet,'name'));
	chart.series[0].update(chart.series[0].options);
	console.log('Update done in ' + (new Date().getTime()-start) + ' ms.');
});
$('#block').css({'width':'200px','height':'200px','background-color':'red'});
$('#slider').on('input',function() {
	$('#block').css('background-color',getColor($(this).val(),0,100));	
});
});

// UNTESTED 
//infoType = 'prepost', 'change'
//info = 'wr','pr','br'
//sets Point properties of each champion object. low/high for columnrange graph, y for column
function setDataSet(dataSet, infoType, info) {
	var range = getRange(dataSet,'d_'+info);
	var min = range[0];
	var max = range[1];
	for (var i = 0; i < dataSet.length; i++) {
		if (dataSet[i]['d_'+info] > 0) {// rate increases
			dataSet[i].low = dataSet[i]['pre_'+info]; 
			dataSet[i].high = dataSet[i]['post_'+info];
			//dataSet[i].color = 'green';
		} else { // rate decreases
			dataSet[i].low = dataSet[i]['post_'+info];
			dataSet[i].high = dataSet[i]['pre_'+info];
			//dataSet[i].color = 'red';
		}
		dataSet[i].currentInfo = info;
		dataSet[i].y = dataSet[i]['d_'+info];
		//console.log(dataSet[i].y,min,max);
		dataSet[i].color = getColor(dataSet[i].y,min,max);
		//console.log(dataSet[i].color);			
	}
	return dataSet;
}


function getColor(value, min, max) { 
	value -= min;
	var range = max-min;
	var green = Math.round(255*(value/range));
	var red = Math.round(255*(1.0-(value/range)));
	return 'rgb('+red+','+green+',0)';
}


function getRange(dataSet,property){
	var low = dataSet[0][property];
	var high = dataSet[0][property];
	for (var i = 0; i < dataSet.length; i++){
		var value = dataSet[i][property];
		if (value < low) {
			low = value;
		} else if (value > high) {
			high = value;
		}
	}
	return [low,high];
}



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

function getArrayOf(dataSet,property){
	var array = [];
	for (var i = 0; i < dataSet.length; i++){
		array.push(dataSet[i][property])
	}
	return array;
}

function roundOff(num) {
	return parseFloat((Math.round(num*100)/100).toFixed(2));
}


// may be removed. requires regeneration of entire series. if modification of variables works through setDataSet() this can probably be deleted
//infoType = 'prepost', 'change'
//info = 'wr','pr','br'
function getSeries(dataSet, infoType, info) {
	var series = [];
	if (true/*infoType == 'prepost'*/) {
		for (var i = 0; i < dataSet.length; i++) {
			var pre = roundOff(dataSet[i]['5.11']['wins']/dataSet[i]['5.11']['picks']*100);
			var post = roundOff(dataSet[i]['5.14']['wins']/dataSet[i]['5.14']['picks']*100);
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
	} else if (infoType == 'change') {
		for (var i = 0; i < dataSet.length; i++) {
			series.push(dataSet['d_'+infoType]);
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