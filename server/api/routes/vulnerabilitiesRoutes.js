'use strict';
// var checkAuth = require('../middleware/checkAuth');
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var vulnCtrl = require('../controllers/vulnerabilitiesController');

    app.route('/vulnerabilities')
        .get(tokenController,vulnCtrl.get_all_vulnerabilities);

    app.route('/vulnerabilities')
        .post( tokenController,vulnCtrl.create_vulnerabilities);

    app.route('/vulnerabilities/vuln')
        .get( tokenController,vulnCtrl.get_vulnerabilities);

 
    app.route('/vulnerabilities/:itemId')
        .patch( tokenController,vulnCtrl.edit_vulnerabilities);

    app.route('/vulnerabilities/:fileId')
        .delete( tokenController,vulnCtrl.delete_vulnerabilities);
};