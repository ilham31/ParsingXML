'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var CompSchema = new Schema({
    _idFile: mongoose.Schema.Types.ObjectId,

    file: {
        _id: mongoose.Schema.Types.ObjectId,

        system: {
            type: String
        },

        title: {
            type: String
        },
        
        status: {
            type: String
        },
        
        result: {
            type: String
        },

        i_status: {
            type: String
        },

        detail: {
            type: String
        }
    }
});

module.exports = mongoose.model('Comp', CompSchema);