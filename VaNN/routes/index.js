var express = require('express');
var router = express.Router();
var consultas = require('../modules/consultas.js');

/* GET home page. */
router.get('/', function (req, res) {        
    res.render('index', { title: 'ESAT' });
});

router.get('/robotrt', function (req, res) {
    res.render('robotrt');
});

router.post('/laser', function (req, res) {
    consultas.setLaser(req, res);
});

router.get('/laserStream', function (req, res) {
    consultas.getLaser(req, res);  
});

router.get('/tree', function (req, res) {
    consultas.getTree(req, res);
});

router.get('/rtotal', function (req, res) {
    consultas.getRTotal(req, res);
});

router.get('/paralelinfo', function (req, res) {
    consultas.getParalelInfo(req, res);
});

router.get('/paralelsi', function (req, res) {
    consultas.getParalelSI(req, res);
});

module.exports = router;
