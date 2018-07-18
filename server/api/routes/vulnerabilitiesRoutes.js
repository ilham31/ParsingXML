'use strict';
// var checkAuth = require('../middleware/checkAuth');

module.exports = function(app) {
    var vulnCtrl = require('../controllers/vulnerabilitiesController');

    app.route('/vulnerabilities/')
        .get(vulnCtrl.get_vulnerabilities);

    app.route('/vulnerabilities')
        .post(vulnCtrl.create_vulnerabilities);
        
    app.route('/vulnerabilities/:vulnId')
        .patch(vulnCtrl.edit_vulnerabilities);

    app.route('/vulnerabilities/:vulnId')
        .delete(vulnCtrl.delete_vulnerabilities);
};