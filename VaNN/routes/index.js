var express = require('express');
var router = express.Router();
var consultas = require('../modules/consultas.js');

/* GET home page. */
router.get('/', function (req, res) {        
    res.render('index', { title: 'USup Robot' });
});

router.get('/robotrt', function (req, res) {
    res.render('robotrt');
});

router.post('/data', function (req, res) {
    consultas.setData(req, res);
});

router.post('/dataSight', function (req, res) {
    consultas.setDataSight(req, res);
});

router.post('/dataNnet', function (req, res) {
    consultas.setDataNnet(req, res);
});

router.get('/laserStream', function (req, res) {
    consultas.getLaser(req, res);  
});

router.get('/positionStream', function (req, res) {
    consultas.getPositions(req, res);
});

router.get('/kmeans', function (req, res) {
    consultas.getKmeans(req, res);
});

router.get('/moments', function (req, res) {
    consultas.getMoments(req, res);
});

router.get('/nnetTraining', function (req,res) {
    consultas.getNneTraining(req, res);
});

router.get('/paralelinfo', function (req, res) {
    consultas.getParalelInfo(req, res);
});

router.get('/paralelsi', function (req, res) {
    consultas.getParalelSI(req, res);
});

module.exports = router;
