// Load required packages
var User = require('../models/userModels');
var authController = require('../controllers/authController');
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
      res.send(err);

    res.json({ message: 'User created!' });
  });
};

exports.login_user = function(req, res) {
  token = jwt.sign({
    username: req.user.username,
    privilege: req.user.privilege
  }, 
  'secretkey',
  {
    expiresIn: "1h"
  });
  res.json(token)
}
// Create endpoint /api/users for GET
exports.get_user = function(req, res) {
    res.json(req.userData);
}; 