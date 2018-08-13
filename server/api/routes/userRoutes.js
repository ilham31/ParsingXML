'use strict';
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var userCtrl = require('../controllers/userController');

    app.route('/users')
        .post(userCtrl.create_user);

    app.route('/users/login')
        .post(userCtrl.login_user);

    app.route('/users')
        .get(tokenController, userCtrl.get_user);

    app.route('/users/password')
        .patch(tokenController, userCtrl.change_password);
};