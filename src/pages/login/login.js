const net = require('net')

var client = new net.Socket();
client.connect(32400, '127.0.0.1', ()=>{
    console.log('connected');

    out = {
            "type"    : "INTER",
            "content" : "Logged in!",
            "special" : {}
    }
    client.write(JSON.stringify(out));
});

document.querySelector("#login-button").addEventListener("click", ()=> {

    out = {
            "type"    : "LOGIN",
            "content" : "Someone clicked me!",
            "special" : {}
    }
    out.special.username = document.querySelector("#form-email").value
    out.special.password = document.querySelector("#form-pass").value

    client.write(JSON.stringify(out));
});
