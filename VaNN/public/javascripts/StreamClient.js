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

function startStream() {
    socket.emit('start-stream');  
    socket.emit('start-stream-laplacian');
    socket.emit('start-stream-gray');
    socket.emit('start-stream-canny');
    socket.emit('start-stream-nnet');
    socket.emit('start-stream-best');
    socket.emit('start-stream-bad');
   
}
