'use strict';
// var checkAuth = require('../middleware/checkAuth');

module.exports = function(app) {
    var compCtrl = require('../controllers/complianceController');

    app.route('/compliance')
        .get(compCtrl.get_compliance);

    app.route('/compliance')
        .post(compCtrl.create_compliance);
        
    app.route('/compliance/:compId')
        .patch(compCtrl.edit_compliance);

    app.route('/compliance/:compId')
        .delete(compCtrl.delete_compliance);
};