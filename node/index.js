var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var request = require('request');
var bodyParser = require('body-parser');

app.use(bodyParser());

app.get('/realtime/', function(req, res){
  res.sendFile(__dirname + '/files/index.html');
});

app.post('/events/', function(req, res){
  if(req.body){
    console.log(req.body);
    if(req.body.is_admin){
      io.to("admin").emit("event", req.body);
    }else{
      io.emit("event", req.body);
    }
    res.status(201);
    res.send("{}");
    return;
  }
  res.status(400);
  res.send("400 Bad Request");
});

io.on("connection", function(socket){
  // Authentication Check
  var headers = socket.handshake.headers;
  request({
    url:"http://localhost:8000/api/auth/",
    json:true,
    headers:{
      "Cookie":headers.cookie,
      "Accept":"application/json"
    }
  },function (error, response, body){
    if (error || response.statusCode != 200){
      console.log("Connected from Unknown User");
      socket.disconnect();
    }else if(body.is_staff) {
      console.log("Connected from " + body.username + " (admin)");
      socket.join("admin");
    }else{
      console.log("Connected from " + body.username);
    }
  });




});


http.listen(8001, function(){
  console.log('listening on *:8001');
});





// Proxy Server for Development
var http = require('http');
var httpProxy = require('http-proxy');
var url = require('url');
var proxy = httpProxy.createProxyServer({});

var server = http.createServer(function (req, res) {

  var hostname = req.headers.host.split(":")[0];
  var pathname = url.parse(req.url).pathname;

  if(pathname.indexOf("/socket.io/") === 0 || pathname.indexOf("/realtime/") === 0 ){
    proxy.web(req, res, {
      target: "http://localhost:8001"
    });
    return;
  }

  proxy.web(req, res, {
    target: "http://localhost:8000"
  });
});

server.on('upgrade', function (req, socket, head) {
  console.log("upgrade");
  proxy.ws(req, socket, head, {
    target: {
      host: 'localhost',
      port: 8001
    }
  });
});

server.listen(8080, function(){
  console.log('listening on *:8080');
});
