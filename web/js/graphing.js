var dataTypes = ['CHAMPIONS','ITEMS'];
var queueTypes = ['NORMAL_5X5', 'RANKED_SOLO'];
var regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']

// object to keep track of what data should be shown on the graph
var selection = {'data':'','queue':[], 'region':[] };
var chart;
var sortProperties = ['name', 'pre_wr', 'post_wr'];
var currentSortIndex = 0;

$(function() {

	var startTime = new Date().getTime();
	var dataSet = [];
	var options = {
		'chart': {
			'renderTo':'container',
			'zoomType': 'xy',
			'inverted': true
		},
		'title': {
			'text': 'Change in Pick Rates after Patch 5.14'
		},

		'xAxis': {
			'categories': getArrayOf(dataSet,'name'),
			'labels' : {
				'step' : 1
			},
			'alternateGridColor': '#FCFCFC'
		},

		'yAxis': [{
			'title': {
				'text': 'Win Rate'
			},
			'plotLines':[{
				'value': 50,
				'width': 2,
				'color': '#AAAAAA',
				'dashStyle':'Dash',
				'zIndex': 5
			}]
			
		},
		{
			'title' : {
				'text': 'Win Rate'
			},
			'linkedTo':0,
			'opposite':true
		}],
		'legend': {
			'enabled':false
		},

		'series': [{
			'type': 'columnrange',
			'data': [] //prepareDataSet(dataSet,'wr')
		}],
		'tooltip': {
			'shared': true,
			'crosshairs':true,
			'followPointer' : true,
			'hideDelay' : 100,
			'formatter': function() {
				var pt = this.points[0].point;
				// if change is negative, 5.11 > 5.14 and there's a decrease
				if (pt['d_'+pt.currentInfo] < 0 ) { 
					return '<em>' + pt.name + '</em><br>5.11 ' + pt.currentInfo + ': ' +pt.high + '%<br>5.14 ' + pt.currentInfo + ': ' + pt.low + '%<br>Change in winrate: ' + roundOff((pt.low-pt.high))+'%';
				}
				// if change is positive, 5.11 < 5.14 and there's an increase
				return '<em>'+pt.name + '</em><br>5.11 winrate: ' + pt.low + '%<br>5.14 winrate: ' + pt.high + '%<br>Change in winrate: +' + roundOff((pt.high-pt.low))+'%';
			}
		},
		'plotOptions': {
			'stickyTracking' : true
		}

	};


	var request = $.getJSON('json/NORMAL_5X5_NA.json');
	request.done(function(data) {
		dataSet = prepareDataSet(data,'wr');
		options.series[0].data = dataSet;
		
		chart = new Highcharts.Chart(options);
		console.log('Initialization done in ' + (new Date().getTime()-startTime) + ' ms.');
	});

	
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

    $('#cycle-sorting').on('click', function() {
		//sample sort with time taken
		var start = new Date().getTime();
        currentSortIndex = (currentSortIndex + 1) % sortProperties.length
		dataSet.sort(sortByProperty(sortProperties[currentSortIndex]));
        $('#currently-sorting-by').html(sortProperties[currentSortIndex]);
		//var chart = $('#container').highcharts();
		chart.xAxis[0].setCategories(getArrayOf(dataSet,'name'));
		chart.series[0].update(chart.series[0].options);
		console.log('Update done in ' + (new Date().getTime()-start) + ' ms.');
	});
});



//info = 'wr','pr','br'
//sets Point properties of each champion object. low/high for columnrange graph, y for column
function prepareDataSet(dataSet, info) {
	var range = getRange(dataSet,'d_'+info);
	var min = range[0];
	var max = range[1];
	for (var i = 0; i < dataSet.length; i++) {
		if (dataSet[i]['d_'+info] > 0) {// rate increases
			dataSet[i].low = dataSet[i]['pre_'+info]; 
			dataSet[i].high = dataSet[i]['post_'+info];
		} else { // rate decreases
			dataSet[i].low = dataSet[i]['post_'+info];
			dataSet[i].high = dataSet[i]['pre_'+info];
		}
		dataSet[i].currentInfo = info;
		dataSet[i].color = getColor(dataSet[i]['d_'+info],min,max);			
	}
	return dataSet;
}


function getColor(value, min, max) { 	
	var maxValue = Math.max(Math.abs(max),Math.abs(min));
	if (value > 0) {
		var greenness = Math.round(150*value/maxValue);
		return 'rgb('+ (150-greenness) + ',230,' + (150-greenness)+ ')';
	} else {
		var redness = Math.round(-150*value/maxValue);
		return 'rgb(230,' + (150-redness) + ',' + (150-redness)+')';
	}
}

// returns 2-length array with [min, max] of the property in the given dataSet
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
	return parseFloat((Math.round(num*100.0)/100.0).toFixed(2));
}


// may be removed. requires regeneration of entire series. if modification of variables works through prepareDataSet() this can probably be deleted
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
			jsons.push('jsons/champions/'+ queueList[i]+'_'+regionList[j]+'.json');
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