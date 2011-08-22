var http = require('http'), 
    io = require('./socket.io'),
    sys = require('sys'),
    url = require('url');

var logged_users;
var users = [];
var alliance

server = http.createServer(function(req, res){
    
    pathname=url.parse(req.url).pathname;
    switch(pathname){
        case '/index.html':
            var body= '_testcb(\'{"message": "Hello world!"}\')';
            res.writeHead(200, {
                          'Content-Type': 'text/plain' });
            user_room=url.parse(req.url,true).query["id"];
            sys.puts(user_room);
            res.end('_testcb(\'{"message": "Hello world!"}\')');
            break;
    }


});

server.listen(8080);
var socket = io.listen(server);
var users_name = [];
socket.on('connection', function(client){
    sys.puts('on');
  client.on('message', function(message){
       
     if(message.type == 'up_notification'){
         for(var i in users_name)
         {
             for(var j in message.recipients){
                 if(i == j)users[i].send({'checkin' : 'test'})
             }

         }
     }else{
         if(message.type == 'conectat' ){
             users.push(client);
             users_name.push(message.recipients);
         }
     }
  });
});