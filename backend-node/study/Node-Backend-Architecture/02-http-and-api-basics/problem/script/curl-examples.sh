curl -i http://localhost:3000/health
curl -i http://localhost:3000/books
curl -i -X POST http://localhost:3000/books \
  -H 'content-type: application/json' \
  -d '{"title":"Node for Backend Engineers","author":"Alice","publishedYear":2026}'
