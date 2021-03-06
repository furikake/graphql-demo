# GraphQL Demo

Quick demo of GraphQL in Node.js interacting with a several REST APIs implemented in Flask.

Demo will prime the necessary test data and the graph looks a little like this.

```
                             +----------------------+
                             |                      |
                             |       /graphql       |
                             |                      |
                             +----------------------+
                                        |
                                        |
                                        |
                                        |
+-----------------------+    +----------v-----------+    +----------------+     +---------+
| Service Qualification |    |       Address        |    | Medical Alarm  |     | Contact |
+-----------------------+    +----------------------+    +----------------+     +---------+
| location_id           +----+ location_id          +----+ location_id    |  +--+ crm_id  |
| service_class         |    | rollout_region_id    |    | description    |  |  | name    |
| service_class_desc    |    | distribution_area_id |    | contact_crm_id +--+  | email   |
| service_class_reason  |    | road_number          |    |                |     | phone   |
| service_type          |    | road_suffix_code     |    +----------------+     |         |
| expected_date_of_rfs  |    | road_type_code       |                           +---------+
|                       |    | locality_name        |
+-----------------------+    | state_territory_code |
                             | full_address         |
                             |                      |
                             +----------------------+
```

## Example Queries

### Simple hardcoded query

```
query{
  location(locationId:"LOC000000000001"){
    fullAddress
    medicalAlarms{
      description
      contact{
        name
        email
      }
    }
    serviceQualification{
      serviceClassDesc
      expectedDateOfRfs
    }
  }
}
```

### Parameterised query

```
query($locationId:ID!){
  location(locationId:$locationId){
    fullAddress
    medicalAlarms{
      description
      contact{
        name
        email
      }
    }
    serviceQualification{
      serviceClassDesc
      expectedDateOfRfs
    }
  }
}
```

Variables

```
{
  "locationId": "LOC000000000001"
}
```

### curl

```
curl 'http://localhost:5000/graphql?' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  --data-binary '{"query":"query($locationId:ID!){location(locationId:$locationId){\nfullAddress\n}}","variables":"{\"locationId\":\"LOC000000000001\"}"}'
```

### Introspection Query

```
{
  __schema{
    types{
      name
      fields(includeDeprecated:true){
        name
        description
        args {
          name
          description
          defaultValue
        }
        type {
          kind
          name
          description
        }
      }
    }
  }
}
```

## Docker Services

The applications used in this demo utilises Docker Swarm.

### Build Docker Images

```
docker-compose build
```

### Start Docker Services

Note, this mounts `/tmp/demodb` as `/restapi/db` in the container. A very small SQLite DB will be created in your `/tmp`.

```
docker-compose up -d
```

GraphiQL is available at: http://localhost:5000/graphql

### Stop Docker Services

```
docker-compose stop
```

### Bin It

```
docker-compose down
```