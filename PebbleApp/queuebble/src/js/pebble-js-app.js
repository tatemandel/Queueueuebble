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


Pebble.addEventListener("webviewclosed",
  function(e) {
    console.log("Configuration window returned: " + e.response);
  }
);
