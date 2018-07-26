var express = require('express'),
    app = express(),
    port = process.env.PORT || 3000,
    mongoose = require('mongoose'),
    cors = require('cors');
    bodyParser = require('body-parser'),
    passport = require('passport');

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/NessusParser');

app.use(passport.initialize());
// app.use(passport.serializeUser(function(user, done) {
//     done(null, user);
//   }));
// app.use(passport.deserializeUser(function(user, done) {
//     done(null, user);
//   }));
app.use(bodyParser.urlencoded({limit: '50mb', extended: false }));
app.use(bodyParser.json({limit: '50mb'}));

app.use(cors());

var userRoutes = require('./api/routes/userRoutes');
var vulnRoutes = require('./api/routes/vulnerabilitiesRoutes');
var compRoutes = require('./api/routes/complianceRoutes');

userRoutes(app); 
vulnRoutes(app);
compRoutes(app);

app.listen(port);

console.log('NessusParser RESTful API server started on: ' + port);