'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ItemSchema = new Schema({
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
});

var CompSchema = new Schema({

    hostname: [{
        item: [ItemSchema]
    }]
     
});

module.exports = mongoose.model('Comp', CompSchema);