    $('document').ready(function(){
        var username = {{ userprofile.user.username }} ;
        socket = new io.Socket('localhost',{port:8080});
        socket.connect();
        socket.on('connect',function(data){
            socket.send({'conectat':username});
        });

    })
