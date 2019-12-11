# Tables
The `tables.py` file defines the Object Relational Mapping (ORM) that allows
the honeypot to easily interface with the database from Python. The ORM uses the `sqlalchemy` 
module, which will interact the same with any flavor of database (PostGreSQL, SQLite, MySQL, etc), 
so long as it is a relational database.

## Table Structure
There are three different tables defined in the ORM: `Connections`, `Credentials`, and `Requests`. 
Both the `Credentials` and `Requests` tables have a relationship to the `Connections` table.

### Connections Table
The connections table has six columns:

| id  | created_at | sourceIP | sourcePort | destPort | localRemote | proto |
|:---:|:----------:|:--------:|:----------:|:--------:|:-----------:|:-----:|
| The primary key | Time of connection | Source IP of connection | Source port of connection | Destination port of connection | Whether IP address is from a private (local) or global (remote) network | Protocol number, either TCP (6) or UDP (17) 

### Credentials Table
The credentials table stores the usernames and passwords used to log in via the Telnet and SSH services. The 
credentials table has a relationship to its corresponding connection from the connections table, and has five 
columns:

| id  | username | password | connections_id | connection |
|:---:|:----------:|:--------:|:----------:|:--------:|
| The primary key | Username used to log in | Password used to log in | The primary key of the corresponding connection from the `Connections` table | The connection object referred to by `connections_id` |

The username and password columns in the database are restricted to a length of 256, which can be controlled by the 
`CREDS_LENGTH` variable in `tables.py`.

### Requests Table
The requests table stores payload data from the HTTP/HTTPs, Shell, or SQL connections to the honeypot. The requests 
table also has a relationship to its corresponding connection from the connections table, and also has five columns:
  
| id  | request | request_type | connections_id | connection |
|:---:|:----------:|:--------:|:----------:|:--------:|
| The primary key | The payload data from the request | The type of request (HTTP/HTTPs, Shell, SQL) | The primary key of the corresponding connection from the `Connections` table | The connection object referred to by `connections_id` |

The request column is restricted to a length of 4096, and the request_type column is restricted to a length of 10,
which are controlled by the `COMMAND_LENGTH` and `REQUEST_TYPE_LENGTH` variables in `tables.py`, respectively.

## Check For Tables
The `check_for_tables()` function in `tables.py` serves the purpose of checking if the tables specified above
exist in the database or not, and if they don't it will create the tables to avoid database errors.
