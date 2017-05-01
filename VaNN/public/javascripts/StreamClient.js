var socket = io();
socket.on('liveStream', function (url) {
    $('#stream').attr('src', url);
    $('.start').hide();
});

socket.on('liveStream-gray', function (url) {
    $('#stream_gray').attr('src', url);
});

socket.on('liveStream-laplacian', function (url) {
    $('#stream_laplacian').attr('src', url);
});

socket.on('liveStream-canny', function (url) {
    $('#stream_canny').attr('src', url);
});

socket.on('liveStream-nnet', function (url) {
    $('#stream_nnet').attr('src', url);
});

socket.on('liveStream-best', function (url) {
    $('#stream_best').attr('src', url);
});

socket.on('liveStream-bad', function (url) {
    $('#stream_bad').attr('src', url);
});


socket.on('image_stream', function (data) {
    stream('image_stream',data)
});
socket.on('image_stream_canny', function (data) {
    stream('image_stream_canny', data)
});
socket.on('image_stream_gray', function (data) {
    stream('image_stream_gray', data)
});
socket.on('image_stream_laplacian', function (data) {
    stream('image_stream_laplacian', data)
});
socket.on('image_stream_bad', function (data) {
    stream('image_stream_bad', data)
});
socket.on('image_stream_nnet', function (data) {
    stream('image_stream_nnet', data)
});
socket.on('image_stream_best', function (data) {
    stream('image_stream_best', data)
});


function stream(canvas,data) {
    var canvas = document.getElementById(canvas);
    var context = canvas.getContext('2d');
    var img = new Image();    
    var base64String = data.buffer
    img.onload = function () {
        context.drawImage(this, 0, 0, canvas.width, canvas.height);
    };
    img.src = 'data:image/jpeg;base64,' + base64String;
}

function startStream() {
    socket.emit('start-stream');  
    socket.emit('start-stream-laplacian');
    socket.emit('start-stream-gray');
    socket.emit('start-stream-canny');
    socket.emit('start-stream-nnet');
    socket.emit('start-stream-best');
    socket.emit('start-stream-bad');
   
}
