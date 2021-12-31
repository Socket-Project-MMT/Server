
URL="https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"

var data = '{"name":"journal2"}';
var http_request = new XMLHttpRequest();
http_request.open( "post", URL, true );
http_request.setRequestHeader('Content-Type', 'application/json');
http_request.send(JSON.stringify(data));
