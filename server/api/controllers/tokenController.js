const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    try {
        var token = req.headers.authorization.split(" ")[1];
        console.log(token);
        var decode = jwt.verify(token, "secretkey");
        req.userData = decode; //
        console.log(req.userData)
        next(); // success auth
    } catch (error) {
        return res.status(401).json({
            message: 'Auth Failed'
        });
    }
};