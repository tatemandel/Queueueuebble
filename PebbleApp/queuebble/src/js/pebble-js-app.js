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
 // var req = new XMLHttpRequest();
 //  req.open('GET', 'http://api.openweathermap.org/data/2.1/find/city?lat=37.830310&lon=-122.270831&cnt=1', true);
 //  req.onload = function(e) {
 //    if (req.readyState == 4 && req.status == 200) {
 //      if(req.status == 200) {
 //        var response = JSON.parse(req.responseText);
 //        var temperature = result.list[0].main.temp;
 //        var icon = result.list[0].main.icon;
 //        Pebble.sendAppMessage({ "icon":icon, "temperature":temperature + "\u00B0C"});
 //      } else { console.log("Error"); }
 //    }
 //  }
 //  req.send(null);

   var req = new XMLHttpRequest();
   req.open("POST", "http://54.84.161.157/login/", {
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
