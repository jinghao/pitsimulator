function ajax_handler()
{
	try
	{
		return new XMLHttpRequest();
	}
	catch(e)
	{
		try
		{
			return new ActiveXObject('Microsoft.XMLHTTP');
		}
		catch(e)
		{
			return false;
		}
	}
}

function game_init()
{
	setInterval(function() { get_xmlhttp(); }, 2000);
}

function ajax_ready(ajaxObj)
{
	return ajaxObj.readyState == 4;
}

function send_request(ajaxObj, callBack, sendQuery)
{
	if(ajaxObj != null)
	{
		ajaxObj.abort();

		if(ajaxObj.readyState == 0 || ajaxObj.readyState == 4)
		{
			ajaxObj.open('POST', gameObj.url, true);
			ajaxObj.setRequestHeader('Content-Type','application/x-www-form-urlencoded; charset=UTF-8');
			ajaxObj.onreadystatechange = function() { if(ajax_ready(ajaxObj)) callBack(); };
			ajaxObj.send("random=" + Math.random() + "&" + sendQuery);
		}
		else
		{
			setTimeout(function() { send_request(ajaxObj, callBack, sendQuery); }, 500);
		}
	}
}

function reload_page()
{
	window.location.reload();
}

function send_xmlhttp(action, extras)
{
	send_request(gameObj.ajaxObj, handle_send, "action=" + action + "&" + extras);
}

function handle_send()
{
	if(gameObj.ajaxObj.responseText != "OK")
		alert(gameObj.ajaxObj.responseText)
	else
		alert("Action successful")
}

function get_xmlhttp()
{
	send_request(gameObj.ajaxObj, handle_get, "ajax=get");
}

function handle_get()
{	
	response = gameObj.ajaxObj.responseText.split("||||");
	
	$('newsbox').innerHTML = response[0];
	$('queue').innerHTML = response[1];
	teams = response[2].split("\n");
	for(var i = 0; i < teams.length; i++) {
		values = teams[i].split("|");
		
		$("team" + values[0] + "_bid").innerHTML = values[1];
		$("team" + values[0] + "_ask").innerHTML = values[2];
	}
}

function $(element)
{
	if (document.getElementById) return document.getElementById(element);
	else if (document.all) return document.all[element];
	else if (document.layers) return document.layers[element];
	return element;
}

var gameObj = {
	url: "/ajax/",
	ajaxObj: ajax_handler(),
}