var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var hbs = require('express-handlebars');
var mysql = require('./modules/consultas.js')
var routes = require('./routes/index');
const fs = require('fs');

var app = express();

// view engine setup
app.engine('hbs', hbs({ extname: 'hbs', defaultLayout: 'layout', layoutsDir: __dirname + '/views/layout/' }));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(require('stylus').middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});
app.set('port', 3000);
var http = require('http').createServer(app);
var io = require('socket.io').listen(http);
var spawn = require('child_process').spawn;
var proc;
var sockets = {};

io.on('connection', function (socket) {

    sockets[socket.id] = socket;
    console.log("Total clients connected : ", Object.keys(sockets).length);

    socket.on('disconnect', function () {
        delete sockets[socket.id];

        // no more sockets, kill the stream
        if (Object.keys(sockets).length == 0) {
            app.set('watchingFile', false);
            if (proc) proc.kill();
            fs.unwatchFile('./stream/image_stream.jpg');
        }
    });

    socket.on('start-stream', function () {
        startStreaming(io);
    });

});

function stopStreaming() {
    if (Object.keys(sockets).length == 0) {
        app.set('watchingFile', false);
        if (proc) proc.kill();
        fs.unwatchFile('./public/stream/image_stream.jpg');
    }
}

function startStreaming(io) {
    if (app.get('watchingFile')) {
        io.sockets.emit('liveStream', 'stream/image_stream.jpg?_t=' + (Math.random() * 100000));
        return;
    }

    var args = ["-w", "640", "-h", "480", "-o", "./stream/image_stream.jpg", "-t", "999999999", "-tl", "100"];
    proc = spawn('raspistill', args);

    console.log('Watching for changes...');
    io.sockets.emit('liveStream', 'stream/image_stream.jpg?_t=' + (Math.random() * 100000));
    app.set('watchingFile', true);

    fs.watchFile('./public/stream/image_stream.jpg', function (current, previous) {
        io.sockets.emit('liveStream', 'stream/image_stream.jpg?_t=' + (Math.random() * 100000));
    })
}

function port() {
    return app.get('port');
}

module.exports = http;
module.exports.port = port;
