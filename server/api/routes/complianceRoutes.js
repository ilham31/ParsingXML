'use strict';
// var checkAuth = require('../middleware/checkAuth');
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var compCtrl = require('../controllers/complianceController');

    app.route('/compliance')
        .get( compCtrl.get_all_compliance);

    app.route('/compliance')
        .post( compCtrl.create_compliance);
        
    app.route('/compliance/comp')
        .get( compCtrl.get_compliance);    

    app.route('/compliance/item')
        .post( compCtrl.create_item);

    app.route('/compliance/item')
        .delete( compCtrl.delete_item);
        
    app.route('/compliance/:itemId')
        .patch( compCtrl.edit_compliance);

    app.route('/compliance/:fileId')
        .delete( compCtrl.delete_compliance);
};