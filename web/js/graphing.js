var dataTypes = ['CHAMPIONS','ITEMS'];
var queueTypes = ['NORMAL_5X5', 'RANKED_SOLO'];
var regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
var abbrev = {'wr':'Win','pr':'Pick'}
var DEFAULT_INFO = 'wr';
// object to keep track of what data should be shown on the graph


$(function() {
	var selection = {'data':'','queue':[], 'region':[] };
	var jsonData;
	var chart;
	var startTime = new Date().getTime();
	var dataSeries = {
		'currentInfo' : DEFAULT_INFO,
		'type' : 'columnrange'
	};
	var markerSeries = {
		'currentInfo' : DEFAULT_INFO,
		'type' : 'scatter'
	};
	var options = generateChartOptions(DEFAULT_INFO);

	var request = $.getJSON('json/NORMAL_5X5_NA.json');
	request.done(function(data) {
		jsonData = data;
		dataSeries.data = prepareRangeData(jsonData,DEFAULT_INFO);
		markerSeries.data = prepareMarkerData(dataSeries.data,DEFAULT_INFO);
		options.xAxis.categories = getArrayOf(dataSeries.data,'name');
		options.series.push(dataSeries);
		options.series.push(markerSeries);

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
	$('input[type=radio]').change(function() {
		var value = this.value;
		options = generateChartOptions(value);
		dataSeries.data = prepareRangeData(jsonData,value);
		dataSeries.currentInfo = value;
		markerSeries.data = prepareMarkerData(dataSeries.data,value);
		markerSeries.currentInfo = value;
		options.xAxis.categories = getArrayOf(dataSeries.data,'name');
		options.series.push(dataSeries);
		options.series.push(markerSeries);

		chart = new Highcharts.Chart(options);
	})

	$('#sort-data').on('click', function() {
		//sample sort with time taken
		//var start = new Date().getTime();
		dataSeries.data.sort(sortByProperty($('#sort-type').val()));
		$('#currently-sorting-by').html($("option[value="+$('#sort-type').val()+"]").html());
		markerSeries.data = prepareMarkerData(dataSeries.data,dataSeries.currentInfo);
		chart.xAxis[0].setCategories(getArrayOf(dataSeries.data,'name'));
		chart.series[0].update(chart.series[0].options);
		chart.series[1].update(chart.series[1].options);
		//console.log('Update done in ' + (new Date().getTime()-start) + ' ms.');
	});
});

function generateChartOptions(info) {
	var infoType = abbrev[info];
	var options = {
		'chart': {
			'renderTo':'container',
			'inverted': true
		},
		'credits': {
			'enabled': false
		},
		'title': {
			'text': 'Change in '+ infoType + ' Rate after Patch 5.14'
		},

		'xAxis': {
			'categories': [],
			'labels' : {
				'step' : 1
			},
			'alternateGridColor': '#FAFAFA'
		},

		'yAxis': [{
			'title': {
				'text': infoType + ' Rate'
			},
			'plotLines': []			
		},
		{
			'title' : {
				'text': infoType + ' Rate'
			},
			'linkedTo':0,
			'opposite':true
		}],
		'legend': {
			'enabled':false
		},

		'series': [],
		'tooltip': {
			'shared':true,
			'crosshairs':true,
			'followPointer':true,
			'hideDelay':100,
			'formatter':function() {
				var pt;
				if (typeof this.points == 'undefined'){
					pt = this.point;
				} else {
					pt = this.points[0].point;
				}
				var info = infoType.toLowerCase() + ' rate';
					// if change is negative, 5.11 > 5.14 and there's a decrease
					if (pt['d_'+pt.currentInfo] < 0 ) { 
						return '<em>' + pt.name + '</em><br>5.11 ' + info + ': ' +pt.high + '%<br>5.14 ' + info + ': ' + pt.low + '%<br>Change in ' + info + ': ' + roundOff((pt.low-pt.high))+'%';
					}
					// if change is positive, 5.11 < 5.14 and there's an increase
					return '<em>'+pt.name + '</em><br>5.11 ' + info + ': ' + pt.low + '%<br>5.14 ' + info + ': '+ pt.high + '%<br>Change in '+ info + ': +' + roundOff((pt.high-pt.low))+'%';
				}
			},
			'plotOptions': {
				'stickyTracking' : true
			}

		};
		if (info == 'wr') {
			options['yAxis'][0]['plotLines'].push({
				'value': 50,
				'width': 2,
				'color': '#AAAAAA',
				'dashStyle':'Dash',
				'zIndex': 5
			});	
		}
		return options;
	}

//info = 'wr','pr'
//sets Point properties of each champion object.
function prepareRangeData(dataSet, info) {
	for (var i = 0; i < dataSet.length; i++) {
		if (dataSet[i]['d_'+info] > 0) {// rate increases
			dataSet[i].low = dataSet[i]['pre_'+info]; 
			dataSet[i].high = dataSet[i]['post_'+info];
		} else { // rate decreases
			dataSet[i].low = dataSet[i]['post_'+info];
			dataSet[i].high = dataSet[i]['pre_'+info];
		}
		dataSet[i].currentInfo = info;
		dataSet[i].color = (dataSet[i]['d_'+info] > 0) ? 'rgb(20,230,20)' : 'rgb(230,20,20)';		
	}
	return dataSet;
}

function prepareMarkerData(markerSet,info) {
	for (var i = 0; i < markerSet.length; i++) {
		markerSet[i].y = markerSet[i]['post_'+info];
		markerSet[i].marker = {
			'enabled':true,
			'symbol':(markerSet[i]['d_'+info] > 0) ? 'triangle' : 'triangle-down',
			'radius':5
		};
	}
	return markerSet;
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
