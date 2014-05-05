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

function sendMessages(messages) {
  var failed = [];

  function sendMessage(message) {
    Pebble.sendAppMessage(message,
      function(e) {
        // ack yay
      },
      function(e) {
        failed.push(message);
      }
    );
  }

  while (messages.length > 0) {
    messages.forEach(sendMessage);
    messages = failed;
  }
}

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
});

function getOwned(username) {
  var http = new XMLHttpRequest();
  var params = "username=" + username;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_admin/", true);

  console.log("getOwned: " + username);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      ob.forEach(function(e) { 
        console.log(e['size']); 
        console.log(e['name']); 
        console.log(e['id']); 
        // send the messages
      });
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

Pebble.addEventListener("appmessage", function(e) {
  console.log("Received message: " + e.payload[1] + " " + e.payload[2]);
  if (e.payload[1] == "admin") {
    getOwned(e.payload[2]);
  }
});
