'use strict';
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var userCtrl = require('../controllers/userController');

    app.route('/users')
        .post(userCtrl.create_user);

    app.route('/users/status')
        .get(tokenController, userCtrl.get_user_waiting);

    app.route('/users/delete/:idUser')
        .delete(userCtrl.delete_user);

    app.route('/users/edit')
        .patch(tokenController, userCtrl.edit_user_status);

    app.route('/users/login')
        .post(userCtrl.login_user);

    app.route('/users')
        .get(tokenController, userCtrl.get_user);

    app.route('/users/password')
        .patch(tokenController, userCtrl.change_password);
};