'use strict';
// var checkAuth = require('../middleware/checkAuth');
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var compCtrl = require('../controllers/complianceController');

    app.route('/compliance')
        .get(tokenController, compCtrl.get_all_compliance);

    app.route('/compliance')
        .post( tokenController, compCtrl.create_compliance);
        
    app.route('/compliance/comp')
        .get(tokenController, compCtrl.get_compliance);    

    app.route('/compliance/item')
        .post(tokenController, compCtrl.create_item);

    app.route('/compliance/item')
        .delete(tokenController, compCtrl.delete_item);
        
    app.route('/compliance/:itemId')
        .patch(compCtrl.edit_compliance);

    app.route('/compliance/:fileId')
        .delete( compCtrl.delete_compliance);
};