

var mysql = require('./mysqlConnection.js');
var actualBuffer;

var validar = function (req) {
    var q = req.query;
    q.anio = q.anio == undefined ? "" : q.anio;
    q.facultad = q.facultad == undefined ? "" : q.facultad;
    q.estudios = q.estudios == undefined ? "" : q.estudios;
    q.departamento = q.departamento == undefined ? "" : q.departamento;
    q.programa = q.programa == undefined ? "" : q.programa;
    q.condicion = q.condicion == undefined ? "" : q.condicion;
}

var setLaser = function (req, res) {    
    var q = req.body;
    actualBuffer =  q.buffer
    res.json({ "ok": "200"})
 };

var getLaser = function (req, res) {    
    res.json({"buffer":actualBuffer})
};

var getParalelInfo = function (req, res) {
    validar(req);
    var q = req.query;
    mysql.handle_database(req, res, promedio(q.anio,q.estudios,q.facultad,q.departamento,q.programa,q.condicion));
};

var getParalelSI = function (req, res) {
    validar(req);
    var q = req.query;
    mysql.handle_database(req, res, satisinsatis(q.anio, q.estudios, q.facultad, q.departamento, q.programa, q.condicion));
};

var getTree = function (req, res) {  
    mysql.handle_database(req, res,tree);
};

var getRTotal = function (req, res)
{
    validar(req);
    var q = req.query;
    mysql.handle_database(req, res, resumenTotal(q.anio, q.estudios, q.facultad, q.departamento, q.programa, q.condicion));
}; 

module.exports.getLaser = getLaser;
module.exports.setLaser = setLaser;

