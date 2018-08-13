// Load required packages
var User = require('../models/userModels');
var jwt = require('jsonwebtoken');
var bcrypt = require('bcrypt-nodejs');


// Create endpoint /api/users for POST
exports.create_user = function(req, res) {
  var user = new User({
    username: req.body.username,
    password: req.body.password,
    privilege: req.body.privilege
  });

  user.save(function(err) {
    if (err){
      return res.status(409).json('username sudah terdaftar');;
    };
    return res.json('user created');
  });
};

exports.login_user = function(req, res) {
  User.findOne({ username: req.body.username })
  .exec()
  .then(user =>
  {
    if (!user) 
    {
      return res.status(401).json('user tidak ada');
    }
    user.verifyPassword(req.body.password, function(err, isMatch) {
      if (err) { return res.status(401).json(err) }

      // Password did not match
      if (!isMatch) { return res.status(401).json('password salah') }

      // Success
      token = jwt.sign({
        username: user.username,
        privilege: user.privilege
      }, 
      'secretkey',
      {
        expiresIn: "12h"
      });
      res.json(token);
    });
  })
}

exports.change_password = function(req, res) {
  console.log("username user", req.userData.username)
  User.findOne({ username: req.userData.username })
  .exec()
  .then(user =>
  {
    if (!user) 
    {
      return res.status(401).json('user tidak ada');
    }
    user.verifyPassword(req.body.old_password, function(err, isMatch) {
      if (err) { return res.status(401).json(err) }

      // Password did not match
      if (!isMatch) { return res.status(401).json('password lama salah') }

      bcrypt.genSalt(5, function(err, salt) {
        if (err) return res.json(err)
    
        bcrypt.hash(req.body.new_password, salt, null, function(err, hash) {
          if (err) return res.json(err)

          User.findOneAndUpdate(
            {username: req.userData.username}, { $set: { password: hash }}
          )
          .exec()
            .then(result => {
                res.status(200).json({
                    result,
                    message: "Password updated",
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
        });
      });

      
    });
  })
}

// Create endpoint /api/users for GET
exports.get_user = function(req, res) {
    res.json(req.userData);
}; 