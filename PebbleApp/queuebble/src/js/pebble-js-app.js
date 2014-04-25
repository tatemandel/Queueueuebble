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

  var options = JSON.stringify(JSON.parse(decodeURIComponent(e.response)));
  console.log("Options = " + options);
  var req = new XMLHttpRequest();
  req.open("POST", "http://54.84.161.157/pebble_get_queues/", {
    "username" : options['username'],
    "password" : options['password']
  });
  req.onload = function(e) {
    if (req.status == 200) {
      var result =  JSON.parse(req.responseText);
      console.log(result);
    } else {
      console.log("FUUUUUCKKKKK");
    }
  };
  req.send(null);
});
