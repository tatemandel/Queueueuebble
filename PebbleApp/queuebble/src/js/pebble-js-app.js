Pebble.addEventListener("ready",
  function(e) {
    console.log("JavaScript app ready and running!");
  }
);

Pebble.addEventListener("showConfiguration",
  function(e) {
    console.log("Configuration window shown");
    Pebble.openURL("http://54.84.161.157/pebble_login/");
  }
);

Pebble.addEventListener("webviewclosed", function(e) {
  console.log("Configuration window closed");

  var options = JSON.parse(decodeURIComponent(e.response));
  console.log("Options = " + JSON.stringify(options));
  console.log(options['username'])
  console.log(options['password'])

  var http = new XMLHttpRequest();
  var params = "username=" + options['username'] + "&password=" + options['password'];
  http.open("POST", "HTTP://54.84.161.157/pebble_get_queues/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onreadystatechange = function() {
    if (http.status == 200) {
      console.log(http.responseText);
    }
  }
  http.send(params);
});
