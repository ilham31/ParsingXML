var mongoose = require('mongoose');

var Vuln = require('../models/vulnerabilitiesModels');
var jwt = require('jsonwebtoken');

Date.prototype.addHours = function(h){
    this.setHours(this.getHours()+h);
    return this;
}

exports.get_vulnerabilities = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // const userId = decode.userId
    var fileId = req.params.fileId
    Vuln.find({_id : fileId})
        .exec()
        .then(docs => {
            res.status(200).json(docs);
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
};

exports.create_vulnerabilities = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // for (var i = 0; i < req.body.hostname.length; i++) {
    //     for (var j = 0; j < req.body.hostname[i].length; j++) {
            
    //     }
    // }
        console.log("hostname adalah",req.body.hostname);
        var vuln = new Vuln ({
            _idFIle: mongoose.Types.ObjectId(),
            hostname: req.body.hostname
            
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