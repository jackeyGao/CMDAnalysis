var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function init_line() {
    var box = getUrlParameter('box');
    $.getJSON('/api/command/line/?box__pk=' + box, function (data) {
        $('#container').highcharts({
            chart: {
                zoomType: 'x'
            },
            title: {
                text: '命令使用线图'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                        '单击并在绘图区域拖动选择时间' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    enabled: false
                }
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled:false   
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            series: [{
                type: 'area',
                name: '命令数',
                data: data
            }]
        });
    });
}

function init_top_list() {
    var box = getUrlParameter('box');
    $.getJSON('/api/command/top/?box__pk=' + box, function (data) { 
      var tops = data.slice(0,20);
      tops.forEach(function(entry) {
        $("#top-command" ).append("<div class=\"monospaced item\"><div class=\"right floated content\"><span class=\"yellow text\" style=\"position: absolute;right: 100px;\">" + entry["y"] + " times</span><span class=\"green text\"> " + (entry["m"] * 100).toFixed(2) + "%</span></div><div class=\"content\"> <span class=\"grey text\" style=\"font-size: 15px;\"><b>" + entry["command"] + "</b></span></div></div>");
      })
    });
}

function init_top_list() {
    var box = getUrlParameter('box');
    $.getJSON('/api/command/top/?box__pk=' + box, function (data) { 
      var tops = data.slice(0,20);
      tops.forEach(function(entry) {
        $("#top-command" ).append("<div class=\"monospaced item\"><div class=\"right floated content\"><span class=\"yellow text\" style=\"position: absolute;right: 100px;\">" + entry["y"] + " times</span><span class=\"green text\"> " + (entry["m"] * 100).toFixed(2) + "%</span></div><div class=\"content\"> <span class=\"grey text\" style=\"font-size: 15px;\"><b>" + entry["command"] + "</b></span></div></div>");
      })
    });
}

function init_top_pie() {
    var box = getUrlParameter('box');
    $.getJSON('/api/command/top/?box__pk=' + box, function (data) {
    $('#top-pie').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: '命令TOP分布图'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        credits: {
                enabled:false   
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: data
        }]
    });
});
}