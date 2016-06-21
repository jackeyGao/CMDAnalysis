$.getJSON('http://127.0.0.1:8000/api/command/top/?box__pk=396e5460', function (data) { 
	var tops = data.slice(0,20);
	tops.forEach(function(entry) {
		$("#top-command" ).append("<div class=\"monospaced item\"><div class=\"right floated content\"><span class=\"yellow text\" style=\"position: absolute;right: 100px;\">" + entry["y"] + " times</span><span class=\"green text\"> " + (entry["m"] * 100).toFixed(2) + "%</span></div><div class=\"content\"> <span class=\"grey text\" style=\"font-size: 15px;\"><b>" + entry["command"] + "</b></span></div></div>");
	})
});