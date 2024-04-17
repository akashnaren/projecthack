const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 5001;

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    fs.readFile(path.join(__dirname, 'map.html'), (err, data) => {
      if (err) {
          res.statusCode = 500;
          res.end('Error loading map.html');
      } else {
          res.setHeader('Content-Type', 'text/html');
          res.end(data);
      }
    });
  } else if (req.method === 'POST' && req.url === '/') {
    let body = '';
    req.on('data', chunk => {
        body += chunk.toString(); // convert Buffer to string
    });
    req.on('end', () => {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ address: 'Some Address' }));
    });
  } else {
    res.statusCode = 404;
    res.end('Not found');
  }
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${5001}`);
});

// do server and map have to have some connection