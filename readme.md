
```
version: '3'
services:
  geospatial-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: geospatial-api
    ports:
      - "5000:5000"
```
