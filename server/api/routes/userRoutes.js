'use strict';
// var checkAuth = require('../middleware/checkAuth');
var authController = require('../controllers/authController');
var tokenController = require('../controllers/tokenController');


module.exports = function(app) {
    var userCtrl = require('../controllers/userController');

    app.route('/users')
        .post(userCtrl.create_user);

    app.route('/users/login')
        .post(authController.isAuthenticated, userCtrl.login_user);

    app.route('/users')
        .get(tokenController, userCtrl.get_user);
};