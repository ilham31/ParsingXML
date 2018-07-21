var mongoose = require('mongoose');

var Comp = require('../models/complianceModels');
var jwt = require('jsonwebtoken');

Date.prototype.addHours = function(h){
    this.setHours(this.getHours()+h);
    return this;
}

exports.get_all_compliance = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // const userId = decode.userId
    Comp.find({}, function(err, docs){
        if(err) res.status(500).json({
            error: err
        })
        res.status(200).json(docs)
    })
};

exports.get_compliance = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    // const userId = decode.userId
    var fileId = req.query.id
    Comp.findOne({_id:fileId}, function(err, docs){
        if(err) res.status(500).json({
            error: err
        })
        res.json(docs)
    })
};

exports.create_compliance = function (req, res) {
    // const token = req.headers.authorization.split(" ")[1];
    // const decode = jwt.verify(token, "rahasia");
    var data = req.body.item;
    for (var i = 0; i < data.length; i++) {
        data[i].open_date = new Date().addHours(7);
        data[i].status = "open";
    }
    console.log("data adalah", data);
        var comp = new Comp ({
            name: req.body.name,
            upload_date: new Date().addHours(7),
            item: data
        });         
        comp.save()
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
        Comp.update({_id:req.body.fileId}, {$push: {'item': req.body.report}})
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
    Comp.update({_id:req.body.fileId}, {$pull: {item: {_id:req.body.itemId}}})
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

exports.edit_compliance = function (req, res) {
    Comp.update({"item._id": req.params.itemId}, { $set: {
            "item.$.status": req.body.status,
            "item.$.closed_date": new Date().addHours(7)
            } 
        })
        .exec()
        .then(result => {
            res.status(200).json({
                result,
                message: "Comp updated",
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

exports.delete_compliance = function (req, res) {
    Comp.remove({ _id: req.params.fileId })
    .exec()
        .then(result => {
            res.status(200).json({
                result,
                message: "Comp Deleted" 
            });
        })
        .catch(err => {
            res.status(500).json({
                error: err
            });
        });
};