// Load required packages
var User = require('../models/userModels');
var jwt = require('jsonwebtoken');

// Create endpoint /api/users for POST
exports.create_user = function(req, res) {
  var user = new User({
    username: req.body.username,
    password: req.body.password,
    privilege: req.body.privilege
  });

  user.save(function(err) {
    if (err)
      return res.status(409).send(err);

      return res.status(201).json({ message: 'User created!' });
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
      if (err) { return res.json(err) }

      // Password did not match
      if (!isMatch) { return res.json('password tidak cocok') }

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

// Create endpoint /api/users for GET
exports.get_user = function(req, res) {
    res.json(req.userData);
}; 