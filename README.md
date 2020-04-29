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
You found out that Redis manages perfectly geospacial data, so you decided to test it out with some datasets that you found on the web (see the data folder). You're able to find all places within a given radius, with all their informations. Now, to meet your customer's expectations, you have to find out how to get job ads within a given radius around a city. You should obviously save geospatial data about some cities before doing this.
</p>  

### Get all job ads within a radius around a city
Pretty simple for your experienced programmer's skills. When exporting your 'jobs.csv' dataset, you just had to index the 'ville' field in a set to know which job ad is in which city :
```python
HMSET jobs:1161166 offer digital_consultant city Amiens   # set our jobs ad hash
SADD Amiens jobs:1161166                                  # index it by city name
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
  This DBMS support natively geospatial data, such as geocoding/routing and map vizualisation, which merge easily with business intell     app and services. As it supports a large scale of modern application framework, it is really easy for devs to add spatial capabilities   to applications. It is standart-based SQL and Java APIs, but also JSON and REST. Offering a great query performance, partitioning,       distributed transactions and sharding, Oracle can manage large scale geospatial applications.
</p>

#### [IBM cloud geospaatial](https://researcher.watson.ibm.com/researcher/view_group.php?id=9646)
<p align="justify">
  "In location-based applications, geospatial data — including points, polygons and linestrings — captures the location, size and shape   of real-world objects. Geospatial indexes speed up searches based on location, enabling applications to take full advantage of the       spatial relationships within data. Web and mobile developers can enhance their applications with geospatial operations, enabling         advanced location-based features, mapping functionality and situational awareness."
</p>

#### Conclusion
<p align="justify">
  Relationnal DBMS can manage geospatial data. However, they seem to be rather inadequate because of the complex structure of geometric   information and its topological relationship between sets of spacially related objects. In other words, since DBMS can only store       standart alphanumeric data types, it forces a geospacial object to be decomposed into immutable data types. This fataly leads to a       distribution of these data framgents into several columns, which complicate the formulation and efficiency of each querry. Sometimes,   some DBMS are just "overkilled" for the use-case, with a risk to put more energy on understanding their process rather than focusing on the   main use of your application.
</p>
I you want to read more about geospatial data in DBMS : https://www.nap.edu/read/10661/chapter/5#52

### Elasticsearch and Kibana
<p align="justify">
  Elasticsearch offers a great flexibility when it's about data types. It can manage different types of queries and even merge them.       Providing very fast results whatever the type or the conception, Elasticsearch allows you to personalize your environment (store as     much metadata as you want) in order be best suited to your needs. Paired with Kibana map solution, it makes possible an intuitive       integration of geospatial data layers into temporal data. With this tool, you can build your own personalized dashboard and see the     evolution of your data in real-time.
</p>

It represents a great alternative, as it does not look very complex thanks to well documented solutions and its user-friendly           interfaces. Read more about Elasticsearch and Kibana for geospatial data : https://www.elastic.co/fr/maps

### PUB/SUB with Redis
Let's assume that we decided to develop an app allowing a job seeker to subsribe to a stream by giving the name of city. It would return to him all job ads within 30km of this town.

#### Pattern
<p align="justify">
  Since we are in a "publish-subscribe" conception, our job ads platform represents the brocker, a bridge for data delivery between the   sender and the receiver. We want to keep data about both sides, because it will give us informations about habits and behavior, with     the aim to find a trend.
</p>

### Implementation
You can run the docker configuration to get a full Redis environment. To implement this, the idea would subscribing to all towns within 35km and getting data every time a job ad is publishedd in one of these.

The first step is to create our receiver :
```python
# connect with redis server as job_seeker (default configs)
r1 = redis.Redis(host='localhost', port=6379)
job_seeker = r1.pubsub()
# subscribe to any offer within 30km of the given place
job_seeker.subscribe('job_ads')
```

Then, we should create our sender :
```python
# connect with redis server as job_advertiser (default configs)
r2 = redis.Redis(host='localhost', port=6379)
# create a job add and publish it
new_ad = 
job_adv.publish('job_ads', new_ad)
```
