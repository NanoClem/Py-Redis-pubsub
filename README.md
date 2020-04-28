# Py-Redis-pubsub
A simple use-case of [Redis](https://redis.io/) with python for geospatial querying.


**Since it is an exemple of use of python-redis, I encourage you to enhance it. This is NOT a tutorial for Redis or python-redis.**

## Context / Scenario
<p align="justify">
You work in a digital company as a consultant. You have been assigned on a fresh new mission in which a customer wishes to operate in job hunting area. As he already has his own job search engine, he had an idea to keep a certain degree of relevance : base the research in priority close to a residential place. He asked you to do a quick benchmark of geospacial-data processing methods provided by Redis, since he doesn't know yet its potential.
</p>

## How to use it

### Installation
1. If you don't have Python installed yet, [get it here](https://www.python.org/downloads/).
2. A docker environment is provided to run Redis whatever your os is. See [here](https://www.docker.com) how to install docker. 
3. The config is composed of three containers : a redis server, a redis client and a phpRedisAdmin. Simply open a terminal in "redis-docker" folder path and run `docker-compose -d up`.
4. If you want to use your own version of Redis, you can install it [here](https://redis.io/download).

### Setup and Run
You have two different ways to use the redis client :
1. Redis runs on default configurations with docker, just open a terminal and run `docker-compose run rcli` to get the redis client.
2. Open a web browser and search `localhost:your_port` (8081 by default) to get the php interface.

## Benchmark
<p align="justify">
You found out that Redis manages perfectly geospacial data, so you decided to test it out with some datasets that you found on the web (see the data folder). You're able to find all places within a given radius, with all their informations. Now, to meet your customer's expectations, you have to find out how to get job ads within a given radius around a city. You should obviously save geospatial data about your job ads in a key before doing this.
</p>  

### Get all job ads within a radius around a city
Pretty simple for your experienced programmer's skills. You just used [this](https://redis.io/commands/georadius) :
```bash
GEORADIUS yourkey long lat radius km WITHCOORD WITHDIST
```
<p align="justify">
This command gives you all members which are within the radius of given coords. It only needs coords (long, lat) of a city, a radius (either in meter/km/miles/feet) and some optional parameter such as WITHCOORD/WITHDIST to diplsay informations about job ads.
</p>  

## Further on
<p align="justify">
Since you want to cover as much possibilties as you can, you decided to lead additionnal researches to suggest other solutions to your customer if they are more suitable.
</p>  

### Geospatial in other main relationnal DBMS

#### [PostGIS](https://postgis.net/)
<p align="justify">
  It is a spatial database extender for PostgreSQL object-relationnal database. It adds support for geographic objects allowing location   queries to be run in SQL. Could be useful to associate as much information (metadata) as you want to a location, since it just adds a   geographic dimension to sql objects.
</p>

#### [Oracle spatial features](https://www.oracle.com/database/technologies/spatialandgraph/spatial-features.html)
<p align="justify">
</p>

#### [Neo4j Spatial](https://neo4j-contrib.github.io/spatial/0.24-neo4j-3.1/index.html)
<p align="justify">
</p>

#### [IBM cloud geospaatial](https://researcher.watson.ibm.com/researcher/view_group.php?id=9646)

#### Conclusion
<p align="justify">
  Relationnal DBMS can manage geospatial data. However, they seem to be inadequate because of the complex structure of geometric           information and its topological relationship between sets of spacially related objects. In other words, since DBMS can only store       standart alphanumeric data types, it forces a geospacial object to be decomposed into immutable data types. This fataly leads to a       distribution of these data framgents into several columns, which complicate the formulation and efficiency of each querry.
</p>
I you want to see more about geospatial data in DBMS : https://www.nap.edu/read/10661/chapter/5#52

### Elasticsearch and Kibana

### PUB/SUB with Redis
