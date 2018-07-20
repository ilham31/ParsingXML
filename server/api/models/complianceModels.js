'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ItemSchema = new Schema({
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
    date: Date,

    item: [ItemSchema],
    
    child: ItemSchema
});

module.exports = mongoose.model('Comp', CompSchema);