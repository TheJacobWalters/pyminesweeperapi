const http = require('http');
const fs = require('fs').promises

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  fs.readFile(__dirname + "/index.html")
    .then(contents => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'text/html');
        res.end(contents);
    })
    .catch(err => {
        res.writeHead(500)
        res.end(err)
        return
    })
    return res
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});