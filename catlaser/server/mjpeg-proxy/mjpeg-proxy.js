// mjpeg-proxy bootstrap code
// This will run a small webserver on port 8080 that serves up the Pi's video
// stream on the path /index1.jpg.  Make sure to modify the videoSource URL
// variable so that it points to the URL of the MJPEG stream from your Pi on
// your home network.

// Configuration:
var videoSource = 'http://<your home IP address>:8080/?action=stream';  // Path to the source
                                                                        // MJPEG stream on the Pi.
var port        = 8080;           // Port for the webserver this tool creates.
var path        = '/index1.jpg';  // The path to the MJPEG stream that will be
                                  // served by this tool.
// Setup MjpegProxy instance and basic express webapp.
var MjpegProxy = require('mjpeg-proxy').MjpegProxy;
var express = require('express');
var app = express();
const session = require('express-session')
const { ExpressOIDC } = require('@okta/oidc-middleware');

app.use(session({
    secret: 'beth has two cats',
    resave: true,
    saveUninitialized: false,
}));

const oidc = new ExpressOIDC({
    issuer: 'https://${yourOktaDomain}/oauth2/default',
    client_id: '{clientId}',
    client_secret: '{clientSecret}',
    redirect_uri: 'http://localhost:3000/authorization-code/callback',
    scope: 'openid profile'
});

app.use(oidc.router);

// Define route for the proxied MJPEG stream and start listening.
app.get(path, oidc.ensureAuthenticated(), new MjpegProxy(videoSource).proxyRequest);
app.listen(port);
