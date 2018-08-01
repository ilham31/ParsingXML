'use strict';
// var checkAuth = require('../middleware/checkAuth');
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var vulnCtrl = require('../controllers/vulnerabilitiesController');

    app.route('/vulnerabilities')
        .get(vulnCtrl.get_all_vulnerabilities);

    app.route('/vulnerabilities')
        .post( tokenController,vulnCtrl.create_vulnerabilities);

    app.route('/vulnerabilities/vuln')
        .get( vulnCtrl.get_vulnerabilities);

    app.route('/vulnerabilities/item')
        .post( vulnCtrl.create_item);

    app.route('/vulnerabilities/item')
        .delete( vulnCtrl.delete_item);
        
    app.route('/vulnerabilities/:itemId')
        .patch( vulnCtrl.edit_vulnerabilities);

    app.route('/vulnerabilities/:fileId')
        .delete( vulnCtrl.delete_vulnerabilities);
};