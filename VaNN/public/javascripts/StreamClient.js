var socket = io();
socket.on('liveStream', function (url) {
    $('#stream').attr('src', url);
    $('.start').hide();
});

function startStream() {
    socket.emit('start-stream');
    //$('.start').hide();
}