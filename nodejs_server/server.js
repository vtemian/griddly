var io = require('socket.io').listen(8080);
var users = new Array();
var clients = new Array();

io.sockets.on('connection', function (socket) {
    socket.emit('identified', { message: 'handshaking' });
    
    socket.on('handshaking', function (data) {
        users.push(data.user)
        clients.push(socket)
    });

    socket.on('disconnect', function (data){
        var index = clients.indexOf(socket)
        clients.splice(index, 1)
        users.splice(index, 1)
    });
    socket.on('notification', function (data){
        var user = data.recipient

        var index = users.indexOf(user)
        if(index != -1)
            clients[index].emit('notification', {'notification': data.message, 'type': data.type})
    });

    socket.on('news-stream', function (data){
        var user = data.recipient

        var index = users.indexOf(user)

        if(index != -1)
            clients[index].emit('news-stream', {'news': data.news})
    })

    socket.on('checkin', function (data){
        var user = data.user
        var index = users.indexOf(user)
        if(index != -1)
            clients[index].emit('checkin', {'message': data.message, 'locationLat': data.locationLat, 'locationLng': data.locationLng})
    });
});