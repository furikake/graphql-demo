# Service Qualification REST API for GraphQL demo

## REST API

Two resources:

### Address API

```
curl http://localhost:8000/addresses/<location_id> \
-H "Accept: application/json" \
-H "Content-Type: application/json"
```

curl example:

```
curl http://localhost:8000/addresses/LOC000000000005 \
-H "Accept: application/json" \
-H "Content-Type: application/json"
```

httpie example

```
http :8000/addresses/LOC000000000005 -j
```

### Service Qualification API

```
curl http://localhost:8000/service-qualifications/<location_id> \
-H "Accept: application/json" \
-H "Content-Type: application/json"
```

curl example:

```
curl http://localhost:8000/service-qualifications/LOC000000000005 \
-H "Accept: application/json" \
-H "Content-Type: application/json"
```

httpie example:

```
http :8000/service-qualifications/LOC000000000005 -j
```

## Start App Locally

```
./run.sh
```

## Start App in Docker

### Build docker image

```
docker build -t furikake/graphqldemo-rest:latest .
```

### Run docker image

```
docker run -itd -p 8000:8000 -v /tmp/demodb:/restapi/db --name restapi furikake/graphqldemo-rest:latest
```

### Stop docker image

```
docker stop restapi
```

### Cleanup

```
docker rm -v restapi
```