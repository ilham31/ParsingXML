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
    console.log("file id adalah",fileId)
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
    // for (var i = 0; i < req.body.hostname.length; i++) {
    //     for (var j = 0; j < req.body.hostname[i].length; j++) {
            
    //     }
    // }
        var vuln = new Vuln ({
            item: req.body.item
            
            // {
            //     _id: mongoose.Types.ObjectId(),
            //     system: req.body.system,
            //     name: req.body.name,
            //     port_protocol: req.body.port_protocol,
            //     risk_level: req.body.risk_level,
            //     synopsis: req.body.synopsis,
            //     detail: req.body.detail,
            //     solution: req.body.solution,
            //     severity: req.body.severity
            // }
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

exports.create_report_item = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // for (var i = 0; i < req.body.hostname.length; i++) {
    //     for (var j = 0; j < req.body.hostname[i].length; j++) {
            
    //     }
    // }
        console.log("hostname adalah",req.body.hostnameId);
        console.log("hostname adalah",req.body.fileId);
        Vuln.update({_id:req.body.fileId}, {$push: {'item': req.body.reportItem}})
        .exec()
        .then(result => {
            // var hostname = result.hostname.id(req.body.hostnameId);
            // hostname.item.push(req.body.reportItem);
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

exports.delete_report_item = function (req, res) {
    Vuln.update({_id:req.body.fileId}, {$pull: {item: {_id:req.body.reportId}}})
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
    Vuln.update({ _id: req.params.vulnId }, { $set: {
            system: req.body.system,
            name: req.body.name,
            port_protocol: req.body.port_protocol,
            risk_level: req.body.risk_level,
            synopsis: req.body.synopsis,
            detail: req.body.detail,
            solution: req.body.solution,
            severity: req.body.severity
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
    Vuln.remove({ _id: req.params.vulnId })
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