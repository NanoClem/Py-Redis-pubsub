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
You have two different ways of using a client interface :
1. Redis runs on default configurations with docker, just open a terminal and run `docker-compose run rcli` to get the redis client.
2. Open a web browser and search `localhost:your_port` (8081 by default) to get the php interface.

## Benchmark
<p align="justify">
You found out that Redis manage perfectly geospacial data, so you decided to test it out with some datasets that you found on the web (see the data folder). You're able to find all places within a given radius, with all their informations. Now, to meet your customer's expectations, you have to find out how to get job ads within a given radius around a city. You should obviously save geospatial data about your job ads in a key before doing this.
</p>  

### Get all job ads within a radius around a city
Pretty simple for your experienced programmer's skills. You just used [this](https://redis.io/commands/georadius):
```bash
GEORADIUS yourkey long lat radius km WITHCOORD WITHDIST
```
<p align="justify">
This command gives you all members which are within the radius of given coords. It only needs coords (long, lat) of a city, a radius (either in meter/km/miles/feet) and some optional parameter such as WITHCOORD/WITHDIST to diplsay informations about job ads.
</p>  
