
# GraphQL
GraphQL is a query language and provides a way to interface with that query language via the tools it provides. 
GraphQL can be used as a replacement for REST JSON API.

## GraphQL Query Structure
GraphQL provides a simple way to query for data using a JSON-like structure. Consider we have a `Credentials` table 
object with the following attributes:

* id
* username
* password
* connection (relation to another table)
* connections_id (id from the related table)
 

Then below would be what a query to the database using GraphQL would look like asking for a `Credentials` table 
entry with an ID of 5:

```javascript
query {
  credential(id: 5) {
    username
    password
    connection {
      id
      createdAt
      sourceIP
      sourcePort
      destPort
      proto
    }
    connectionsId
  }
}
```

To explain what the different components of the query are doing:

<p align="center">
<img width="500" height="300" src="https://user-images.githubusercontent.com/32188816/69482578-75496f80-0dda-11ea-9914-5e2c7da866c7.png">
</p>

The return response will be in JSON, and we only get back the attributes that we ask for. The response for the query 
above will look as follows:

```json5
{
  "data": {
    "credential": {
      "username": "root",
      "password": "toor",
      "connection": {
        "id": "20",
        "createdAt": "2019-11-03T18:45:24",
        "sourceIP": "127.0.0.1",
        "sourcePort": 23,
        "destPort": 23,
        "proto": 6
      },
      "connectionsId": 20
    }
  }
}
```

## Running and Developing
There is a demo flask app to test GraphQL queries for development. To run the demo flask app, from the 
`HPotter/hpotter-server/` directory do:
    
    export FLASK_APP=hpotter/graphql/app.py
    
Then do:
    
    flask run
    
This will start up a simple GraphQL server running on http://localhost:5000. This URL will not show anything in the 
browser, because we need to send it query data in order to get a response back. It is easy to interact with the GraphQL
server in one of the following ways:

### GraphiQL
 GraphiQL provides an interface to your GraphQL endpoint. GraphiQL has many features, and can be thought of as an IDE
 for GraphQL services. GraphiQL provides code completion for models, attributes, and pretty much anything else, and
 is a very useful tool for developing GraphQL queries.

<p align="center">
    <img src="https://user-images.githubusercontent.com/32188816/69482681-ad9d7d80-0ddb-11ea-98f0-93c81c2cac05.png">
</p>

GraphiQL can be obtained [here](https://electronjs.org/apps/graphiql). After starting the flask app as specified above,
open GraphiQL and specify the GraphQL endpoint URL before beginning development. 

<p align="center">
    <img src="https://user-images.githubusercontent.com/32188816/69482718-33212d80-0ddc-11ea-81ed-1fa01816eb4d.png">
</p>

The GraphiQL interface also provides a very nice summary and auto documentation of the schema and mutations that 
can be performed against the GraphQL server in the Documentation Explorer. To open the Documentation Explorer:

<p align="center">
    <img src="https://user-images.githubusercontent.com/32188816/69482905-4fbe6500-0dde-11ea-857e-e8d4352eb48d.png">
</p>

Once the Documentation Explorer is opened, we can view the documentation for getting data from the GraphQL server
(Query), and also the documentation for creating, modifying, or deleting data within the GraphQL server (Mutations):

<p align="center">  
    <img src="https://user-images.githubusercontent.com/32188816/69482872-e0e10c00-0ddd-11ea-8a04-4185ee183052.png">
</p>

#### Query Operations:

<p align="center">
    <img src="https://user-images.githubusercontent.com/32188816/69482968-1fc39180-0ddf-11ea-8c3f-ae2c2d56625e.png">
</p>

#### Mutation Operations:

<p align="center">
    <img src="https://user-images.githubusercontent.com/32188816/69482980-50a3c680-0ddf-11ea-8e25-af7caeac1b7f.png">
</p>

## Database Tables
The default database is SQLite and requires no configuration. The tables are written into the default 
("main.db") database. The following tables and relations are defined in the database:

* Connections
* Credentials
* Requests

The `Connections` table object consists of the following attributes:
* id
* created_at
* sourceIP
* sourcePort
* destPort
* proto

The `Credentials` table object consists of the following attributes:
* id
* username
* password
* connection (relation to another table)
* connections_id (id from the related table)

The `Requests` table object serves as a table to hold all of the HTTP/HTTPs, SQL, and Shell connections data, and
consists of the following attributes:
* id
* request
* request_type (HTTP/HTTPs, SQL, or Shell)
* connection (relation to another table)
* connections_id (id from the related table)

## Directory Structure
* HPotter/hpotter-server/hpotter/graphql/app.py
    * This is the simple flask app mentioned above.
    
* HPotter/hpotter-server/hpotter/graphql/mutators.py
    * This is where all of the mutation classes are defined, each of which implement the functionality shown above in  
    the `Mutation Operations` subsection. This class defines the CUD (Create Update Delete) services for each table
    we have defined above in the database.
    
* HPotter/hpotter-server/hpotter/graphql/objects.py
    * This file defines the serializers for GraphQL, which are meta objects of the actual tables defined
    in our ORM.  

* HPotter/hpotter-server/hpotter/graphql/schema.py
    * This file defines the container of all of the GraphQL objects (tables in our database) that are 
    available to query through the GraphQL query language.
    
    * Inside of `HPotter/hpotter-server/hpotter/graphql/schema.py` we have several "resolvers", which are defined
    functions that get executed to give back data for a particular table defined in our ORM. 
    
    * Also inside of `HPotter/hpotter-server/hpotter/graphql/schema.py` are defined queries and mutations that can be 
    executed on each table in our ORM. 

## Graphene
Graphene is the GraphQL implementation for Python. Graphene has integration with a number of frameworks and ORMs. We
are using the SQLAlchemy ORM, and Graphene has support for SQLAlchemy with the `graphene_sqlalchemy` module.

#### Graphene Implementation
* Objects
    * The graphene objects are defined in `HPotter/hpotter-server/hpotter/graphql/objects.py`, which construct meta
    data about the actual table objects and their respective attributes that we have defined in 
    `HPotter/hpotter-server/hpotter/tables.py`.
    
    * Each object must inherit from `graphene_sqlalchemy.SQLAlchemyObjectType` to properly map each meta table
    to the SQLAlchemy ORM defined in `HPotter/hpotter-server/hpotter/tables.py`.

* Mutators
    * The mutations (CUD services) are defined in individual classes in 
    `HPotter/hpotter-server/hpotter/graphql/mutators.py`, and each class must inherit from `graphene.Mutation`.
    
    * Each mutation class defines a subclass `Input` which defines the input attributes required to mutate a particular 
    graphene object.
        * Each input class also defines the data types of each attribute defined in the meta tables. 
        
    * Each mutation class also defines a `mutate` function which specifies exactly what is returned once the mutation
    is performed on the graphene object.
    
* Schema
    * The schema defines the container for all GraphQL objects and the operations that can be performed against those
    objects.
    
    * The `Query` class defines the field types defined in each meta table, and contains a set of `resolver` functions
    which are functions that get called when data is queried, and the resolvers are responsible for actually returning
    the requested data.
    
    * There is also a `Mutations` class which defines the names of all of the CUD services that can be executed, which
    are all inherited from `HPotter/hpotter-server/hpotter/graphql/mutators.py`.
    
    * It is important to always keep the `Query` and `Mutations` classes separate, as the `Query` class is only 
    responsible for getting data, whereas the `Mutations` class is responsible for setting data. 
    
The hpotter application utilizes the `schema` object that is defined at the bottom of 
`HPotter/hpotter-server/hpotter/graphql/schema.py`, using the `Query` and `Mutations` classes to define the possible
operations that can be executed against the database and GraphQL server.