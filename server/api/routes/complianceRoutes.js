'use strict';
// var checkAuth = require('../middleware/checkAuth');
var tokenController = require('../controllers/tokenController');

module.exports = function(app) {
    var compCtrl = require('../controllers/complianceController');

    app.route('/compliance')
        .get( tokenController,compCtrl.get_all_compliance);

    app.route('/compliance')
        .post( tokenController, compCtrl.create_compliance);
        
    app.route('/compliance/comp')
        .get( tokenController,compCtrl.get_compliance);    

    
    app.route('/compliance/:itemId')
        .patch(tokenController,compCtrl.edit_compliance);

    app.route('/compliance/:fileId')
        .delete( tokenController,compCtrl.delete_compliance);
};