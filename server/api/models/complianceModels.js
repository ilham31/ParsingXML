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
    
    stats: {
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
    },
    open_date: Date,

    closed_date: Date,

    status: String


});

var CompSchema = new Schema({
    name: String,

    upload_date: Date,

    item: [ItemSchema],
    
    child: ItemSchema
});

module.exports = mongoose.model('Comp', CompSchema);