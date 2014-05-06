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
  function sendNextMessage() {
    if (messages.length == 0) {
      return;
    }

    var message = messages.shift();
    Pebble.sendAppMessage(message,
      function(e) {
        console.log("ack");
        sendNextMessage();
      },
      function(e) {
        console.log("nack");
        messages.unshift(message);
        sendNextMessage();
      }
    );
  }
  sendNextMessage();
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
      // Make sure this resends.
      console.log("Failure :(");      
    }
  );
});

function getOwned(username) {
  var http = new XMLHttpRequest();
  var params = "username=" + username;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_admin/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 1;
        d["12"] = 0;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["2"] = e['id'];
        d["3"] = e['name'];
        d["4"] = e['size'];
        d["5"] = e['status'] ? 1 : 0;
        d["6"] = ob.length;
	d["12"] = 0;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function getUpdatedOwned(username) {
  var http = new XMLHttpRequest();
  var params = "username=" + username;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_admin/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 1;
        d["12"] = 1;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["2"] = e['id'];
        d["3"] = e['name'];
        d["4"] = e['size'];
        d["5"] = e['status'] ? 1 : 0;
        d["6"] = ob.length;
	d["12"] = 1;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function getMember(username) {
  var http = new XMLHttpRequest();
  var params = "username=" + username;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_member/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 2;
        d["12"] = 0;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["2"] = e['id'];
        d["3"] = e['name'];
        d["5"] = e['status'] == "true" ? 1 : 0;
        d["6"] = ob.length;
        d["7"] = e['creator'];
        d["8"] = e['position'];
	d["12"] = 0;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function getUpdatedMember(username) {
  var http = new XMLHttpRequest();
  var params = "username=" + username;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_member/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 2;
        d["12"] = 1;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["2"] = e['id'];
        d["3"] = e['name'];
        d["5"] = e['status'] == "true" ? 1 : 0;
        d["6"] = ob.length;
        d["7"] = e['creator'];
        d["8"] = e['position'];
	d["12"] = 1;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function getQueue(id, type) {
  var http = new XMLHttpRequest();
  var params = "id=" + id;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_queue/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 3;
	d["9"] = type;
        d["12"] = 0;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["1"] = e['username'];
        d["2"] = e['id'];
        d["5"] = e['status'];
        d["6"] = ob.length;
        d["8"] = e['position'];
        d["9"] = type;
	d["12"] = 0;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function getUpdatedQueue(id, type) {
  var http = new XMLHttpRequest();
  var params = "id=" + id;
  http.open("POST", "HTTP://54.84.161.157/pebble_get_queue/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (ob.length == 0) {
        d = {};
	d["10"] = 3;
	d["9"] = type;
        d["12"] = 1;
        data.push(d);  
      }
      ob.forEach(function(e) { 
        d = {};
        d["1"] = e['username'];
        d["2"] = e['id'];
        d["5"] = e['status'];
        d["6"] = ob.length;
        d["8"] = e['position'];
        d["9"] = type;
	d["12"] = 1;
        data.push(d);
      });
      sendMessages(data);
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

function updateStatus(id, username, type, admin) {
  var http = new XMLHttpRequest();
  var params = "id=" + id + "&username=" + username + "&type=" + type;
  http.open("POST", "HTTP://54.84.161.157/pebble_update_status/", true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.setRequestHeader("Content-length", params.length);
  http.setRequestHeader("Connection", "close");

  http.onload = function() {
    if (http.status == 200) {
      console.log("status");
      console.log(http.responseText);
      var ob = JSON.parse(http.responseText);
      var data = [];
      if (type == "remove" || type == "up" || type == "down") {
        if (ob.length == 0) {
          d = {};
          d["10"] = 3;
          d["9"] = type;
          d["12"] = 0; // 0 for don't show
          data.push(d);  
        }
        ob.forEach(function(e) { 
          d = {};
          d["1"] = e['username'];
          d["2"] = e['id'];
          d["5"] = e['status'];
          d["6"] = ob.length;
          d["8"] = e['position'];
          d["9"] = admin;
          d["11"] = 0; // 0 for don't show
          d["12"] = 0; // 0 for don't show
          data.push(d);
        });
        sendMessages(data);
      }
    } else {
      console.log(http.responseText);
    }
  }
  http.send(params);
}

Pebble.addEventListener("appmessage", function(e) {
  console.log("Received message: " + e.payload[1] + " " + e.payload[2]);
  var t = e.payload[1];
  if (t == "admin") {
    getOwned(e.payload[2]);
  } else if (t == "member") {
    getMember(e.payload[2]);
  } else if (t == "mqueue") {
    // 1 is admin, 2 is member
    getQueue(e.payload[2], 2);
  } else if (t == "aqueue") {
    // 1 is admin, 2 is member
    getQueue(e.payload[2], 1);
  } else if (t == "nstart" || t == "progress" || t == "aremove" || t == "up" || 
             t == "down" || t == "favorite" || t == "mremove") {
    updateStatus(e.payload[2], 
                 e.payload[3], 
                 t == "mremove" || t == "aremove" ? "remove" : t, 
                 t == "mremove" ? 2 : 1);
  } else if (t == "memberUpdate") {
    getUpdatedMember(e.payload[2]);
  } else if (t == "adminUpdate") {
    getUpdatedOwned(e.payload[2]);
  } else if (t == "aqueueUpdate") {
      getUpdatedQueue(e.payload[2], 1);
  } else if (t == "mqueueUpdate") {
      getUpdatedQueue(e.payload[2], 2);
  }
 });
