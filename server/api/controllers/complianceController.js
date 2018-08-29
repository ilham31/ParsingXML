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
    Comp.find({}, 'name upload_date uploader')
        .sort({upload_date: -1})
        .exec(function(err, docs){
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
    var start = (req.query.page-1)*100
    var fileId = req.query.id
    Promise.all([
        Comp.aggregate().match({_id: mongoose.Types.ObjectId(fileId)}).project({ukuran: {$size: '$item'}}),
        Comp.findOne({_id:fileId}, {item: {$slice:[start,100]} })
      ]).then( ([ total, data ]) => {
        var obj = data.toObject();
        obj.total_item=total[0].ukuran
        res.json(obj)
      });
};

exports.get_all_data = function(req, res){
    var fileId = req.query.id
    console.log("id",fileId)
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
        data[i].index = i;
    }
        var comp = new Comp ({
            name: req.body.name,
            uploader: req.userData.username,
            upload_date: new Date().addHours(7),
            item: data
        });         
        comp.save()
          .then(result => {
              res.status(201).json({
                fileId: result._id
              });
          })
          .catch(err => {
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
    // console.log("privilege", req.userData.privilege)
    // if(req.userData.privilege=='user') res.status(401).json("user tidak bisa edit");
    Comp.findOneAndUpdate({"item._id": req.params.itemId}, { $set: {
            "item.$.status": "closed",
            "item.$.closed_date": new Date().addHours(7)
            } 
        }, {new: true}, function(err, result){
            if(err){
                return res.status(401).json(err);
            }
            return res.status(200).json(result);
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