var express = require('express'),
    app = express(),
    port = process.env.PORT || 3000,
    mongoose = require('mongoose'),
    cors = require('cors');
    bodyParser = require('body-parser');

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/NessusParser');

app.use(bodyParser.urlencoded({limit: '50mb', extended: false }));
app.use(bodyParser.json({limit: '50mb'}));

app.use(cors());

// var userRoutes = require('./api/routes/userRoutes');
var vulnRoutes = require('./api/routes/vulnerabilitiesRoutes');
var compRoutes = require('./api/routes/complianceRoutes');
// userRoutes(app); 
vulnRoutes(app);
compRoutes(app);

app.listen(port);

console.log('NessusParser RESTful API server started on: ' + port);