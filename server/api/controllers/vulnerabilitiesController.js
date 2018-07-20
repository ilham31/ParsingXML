var mongoose = require('mongoose');

var Vuln = require('../models/vulnerabilitiesModels');
var jwt = require('jsonwebtoken');

Date.prototype.addHours = function(h){
    this.setHours(this.getHours()+h);
    return this;
}

exports.get_all_vulnerabilities = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // const userId = decode.userId
    Vuln.find({}, function(err, docs){
        if(err) res.status(500).json({
            error: err
        })
        res.json(docs)
    })
};

exports.get_vulnerabilities = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // const userId = decode.userId
    var fileId = req.query.id
    Vuln.findOne({_id:fileId}, function(err, docs){
        if(err) res.status(500).json({
            error: err
        })
        res.json(docs)
    })
};

exports.create_vulnerabilities = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
        var vuln = new Vuln ({
            item: req.body.item
        });         
        vuln.save()
          .then(result => {
              res.status(201).json({
                  result
              });
          })
          .catch(err => {
              console.log(err);
              res.status(500).json({
                  error: err
              });
          });
};

exports.create_item = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
        Vuln.update({_id:req.body.fileId}, {$push: {'item': req.body.report}})
        .exec()
        .then(result => {
            res.status(201).json({
                result
            });
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
};

exports.delete_item = function (req, res) {
    Vuln.update({_id:req.body.fileId}, {$pull: {item: {_id:req.body.itemId}}})
    .exec()
        .then(result => {
            res.status(200).json({
                message:"report deleted",
                result
            });
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
};

exports.edit_vulnerabilities = function (req, res) {
    Vuln.update({"item._id": req.params.itemId}, { $set: {
            "item.$.system": req.body.system,
            "item.$.name": req.body.name,
            "item.$.port_protocol": req.body.port_protocol,
            "item.$.risk_level": req.body.risk_level,
            "item.$.synopsis": req.body.synopsis,
            "item.$.detail": req.body.detail,
            "item.$.solution": req.body.solution,
            "item.$.severity": req.body.severity
            } 
        })
        .exec()
        .then(result => {
            res.status(200).json({
                result,
                message: "Vuln updated",
                request: {
                    type: "PATCH"
                }
            });
        })
        .catch(err => {
            console.log(err);
            res.status(500).json({
                error: err
            });
        })
};

exports.delete_vulnerabilities = function (req, res) {
    Vuln.remove({ _id: req.params.fileId })
    .exec()
        .then(result => {
            res.status(200).json({
                result,
                message: "Vuln Deleted" 
            });
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
};