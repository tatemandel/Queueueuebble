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
  console.log(options['username'])

  var id = Pebble.sendAppMessage({ "1" : options['username'] },
    function(e) {
      console.log("Success!");
    },
    function(e) {
      console.log("Failure :(");      
    }
  );

  // var http = new XMLHttpRequest();
  // var params = "username=" + options['username'] + "&password=" + options['password'];
  // http.open("POST", "HTTP://54.84.161.157/pebble_get_queues/", true);

  // http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  // http.setRequestHeader("Content-length", params.length);
  // http.setRequestHeader("Connection", "close");

  // http.onload = function() {
  //   if (http.status == 200) {
  //     console.log(http.responseText);
  //   }
  // }
  // http.send(params);
});
