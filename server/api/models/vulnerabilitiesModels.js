'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var ItemSchema =  new Schema({
    _id: mongoose.Schema.Types.ObjectId,

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

var VulnSchema = new Schema({

    hostname: [{
        item: [ItemSchema]
    }]
     
});

module.exports = mongoose.model('Vuln', VulnSchema);