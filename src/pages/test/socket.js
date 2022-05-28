const net = require('net')

var client = new net.Socket();
client.connect(32509, '127.0.0.1', ()=>{
    console.log('connected');
    client.write('This is a message from the client!');
});


client.on('data', function(data) {
	console.log('Received: ' + data);
  msg = JSON.parse(data)
  console.log(msg)
  document.querySelector(".msg").innerHTML += "<li><p>" + msg.nickname + "------" +  msg.chatid + "</p><p>" + msg.content + "</p></li>"
});
