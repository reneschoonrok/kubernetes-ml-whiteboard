
const express = require('express')
const app = express()
//const { exec } = require('child_process');

var path = require('path');
var fs = require('fs');
var url = require('url');
var https = require('https');
var router = express.Router();
var envtoken = 'empty';
var authtoken = 'also empty';
const util = require('util');
const exec = util.promisify(require('child_process').exec);

var privateKey  = fs.readFileSync('sslcert/key.pem', 'utf8');
var certificate = fs.readFileSync('sslcert/cert.pem', 'utf8');
var credentials = {key: privateKey, cert: certificate};

var httpsServer = https.createServer(credentials, app);

app.use(express.static('public'));
//require('./router/server')(app);
app.engine('html', require('ejs').renderFile);
app.set('views', __dirname + '\views');
app.set('view engine', 'ejs');

async function deployyamlcmd (name) {
    //console.log('envtoken'+ envtoken)
    //console.log('authtoken'+ authtoken)
    try {
        const { stdout, stderr } = await exec('kubectl apply -f ./public/yaml/'+name+'.yaml')
        //const { stdout, stderr } = await exec('dir',)
        console.log(stdout)
        return(stdout);
    } catch (err) {
        console.error('Error: ', err)
        return(stderr);
    }
}

async function deployhelmcmd (name) {
    //console.log('envtoken'+ envtoken)
    //console.log('authtoken'+ authtoken)
    try {
        name = name.split(" ").pop();
        const { stdout, stderr } = await exec('helm upgrade --install '+name+' stable/'+name)
        //const { stdout, stderr } = await exec('dir',)
        console.log(stdout)
        return(stdout);
    } catch (err) {
        console.error('Error: ', err)
        return(stderr);
    }
}

app.get("/deployyaml", function(httpRequest, httpResponse, next){
    var name =httpRequest.query.name;
    console.log("Start executing command deploy: "+name);

    var mydeployyamlcmd = deployyamlcmd(name)
    mydeployyamlcmd.then(function(result) {
        httpResponse.send("Deploying: " + name)
        //httpResponse.send(result);

    });
});

app.get("/deployhelm", function(httpRequest, httpResponse, next){
    var name =httpRequest.query.name;
    console.log("Start executing command deploy: "+name);

    var mydeployhelmcmd = deployhelmcmd(name)
    mydeployhelmcmd.then(function(result) {
        httpResponse.send("Deploying helm chart: " + name)
        //httpResponse.send(result);

    });
});

app.get('/', function (req, res) {
    res.render('../views/index.html');
    console.log("Home page displayed");

});

httpsServer.listen(8443);
console.log("Started listening on 8443!");


