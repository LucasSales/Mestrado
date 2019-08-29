var app = require('express')(),
	bodyParser = require('body-parser'),
	amqp = require('amqplib/callback_api'),
	fs = require('fs'),
	multipartMiddleware = require('connect-multiparty')();
	
   app.use(bodyParser.json());
   app.use(bodyParser.urlencoded({extended: true}));


// fun pra fazer o encode da imagem
// function base64_encode (file) {
// 	let bitmap = fs.readFileSync(file, 'base64');

// 	return bitmap;
// }

// routa da requisicao
// app.post("/match", multipartMiddleware, function (req, res) {
// 	// coloca o ip do rabbitmq
// 	amqp.connect('amqp://172.17.0.2', function (err, conn) {
// 		conn.createChannel(function (err, ch) {
// 			ch.assertQueue('', {exclusive: true}, function (err, q) {
// 				let corr = generateUuid();

// 				ch.consume(q.queue, function (msg) {
// 					if (msg.properties.correlationId == corr) {
// 						console.log("[-] Found %s", msg.content.toString());
// 						res.send(msg.content.toString());
// 					}
// 				}, {noAck: true});

// 				ch.sendToQueue('rpc',
// 					// o que vai ser enviado vai como um Buffer
// 					new Buffer(base64_encode(req.files.file.path)),
// 					{ correlationId: corr, replyTo: q.queue});
// 			});
// 		});
// 	});
// });


// Isso aqui é outro serviço que eu testei
// app.post("/", function (req, res) {
// 	amqp.connect('amqp://172.17.0.2', function (err, conn) {
// 		conn.createChannel(function (err, ch) {
// 			ch.assertQueue('', {exclusive: true}, function (err, q) {
// 				let corr = generateUuid();
// 				// let jsonImagem = JSON.stringify(req.body);

// 				console.log("[*] Received Request Json");

// 				ch.consume(q.queue, function (msg) {
// 					if (msg.properties.correlationId == corr) {
// 						console.log("[-] Found %s matches", msg.content.toString());
// 						res.send(msg.content.toString());
// 					}
// 				}, {noAck: true});

// 				ch.sendToQueue('rpc',
// 					new Buffer("data"),
// 					{ correlationId: corr, replyTo: q.queue});
// 			});
// 		});
// 	});
// });


app.get('/', function(req, res) {
  res.send('hello world');
});

app.post("/", multipartMiddleware,function(req, res) {
	amqp.connect('amqp://192.168.0.88:5672', function (err, conn) {
		conn.createChannel(function (err, ch) {
			ch.assertQueue('', {exclusive: true}, function (err, q) {
				let corr = generateUuid();
				
				console.log("[*] Received " + req.files.data_file.name);

				ch.consume(q.queue, function (msg) {
					if (msg.properties.correlationId == corr) {
						console.log("[-] Found %s matches", msg.content.toString());
						res.send(msg.content.toString());
					}
				}, {noAck: true});

				ch.sendToQueue('rpc',
					new Buffer(fs.readFileSync(req.files.data_file.path)),
					{ correlationId: corr, replyTo: q.queue});
			});
		});
	});
});






function generateUuid () {
	return Math.random().toString() +
		   Math.random().toString() +
		   Math.random().toString();
}

app.listen(8085, function () {
	console.log("[*] Listening on port 8085.");
});

