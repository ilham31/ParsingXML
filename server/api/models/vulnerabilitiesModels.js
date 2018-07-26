'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ItemSchema =  new Schema({

    system: {
        type: String
    },

    name: {
        type: String
    },
    
    port_protocol: {
        type: String
    },
    
    risk_level: {
        type: String
    },

    synopsis: {
        type: String
    },

    detail: {
        type: String
    },
    
    solution: {
        type: String
    },

    severity: {
        type: Number
    },

    open_date: Date,

    closed_date: {
        type: Date,
        default: null
    },

    status: String
})

var VulnSchema = new Schema({
    name: String,

    upload_date: Date,

    uploader: String,

    item: [ItemSchema],

    child: ItemSchema
});

module.exports = mongoose.model('Vuln', VulnSchema);