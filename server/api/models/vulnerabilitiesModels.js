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
    }
})

var HostNameSchema = new Schema({
    item: [ItemSchema],

    child: ItemSchema
})

var VulnSchema = new Schema({
    hostname: [HostNameSchema],

    child: HostNameSchema
});

module.exports = mongoose.model('Vuln', VulnSchema);