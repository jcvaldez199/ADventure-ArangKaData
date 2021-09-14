DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  username VARCHAR(15) UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE route (
  name TEXT UNIQUE NOT NULL,
  PRIMARY KEY (name)
);


CREATE TABLE video (
  filename VARCHAR(30),
  userid INTEGER, 
  /* hash BINARY(64), */
  hash TEXT UNIQUE,
  FOREIGN KEY (userid) REFERENCES customer (id),
  PRIMARY KEY (hash)
);

CREATE TABLE location (
  locname VARCHAR(30),
  routename TEXT NOT NULL,
  userid INTEGER, 
  FOREIGN KEY (routename) REFERENCES route (name),
  FOREIGN KEY (userid) REFERENCES customer (id),
  PRIMARY KEY (userid,routename,locname)
);

CREATE TABLE request (
  id SERIAL PRIMARY KEY,
  routename TEXT NOT NULL,
  userid INTEGER, 
  /* videohash BINARY(64), */ 
  videohash TEXT UNIQUE,
  locname VARCHAR(30),
  FOREIGN KEY (routename) REFERENCES route (name),
  FOREIGN KEY (userid) REFERENCES customer (id),
  FOREIGN KEY (videohash) REFERENCES video (hash),
  FOREIGN KEY (userid,routename,locname) REFERENCES location (userid,routename,locname)
);

INSERT INTO customer (username, password) VALUES ('test','test');

INSERT INTO route (name) VALUES ('Route A');
INSERT INTO route (name) VALUES ('Route B');

INSERT INTO location (userid, locname, routename) VALUES (1,'Location Alpha','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Beta','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Gamma','Route B');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Sigma','Route B');

INSERT INTO video (filename, userid, hash) VALUES ('Tragedy.mp4', 1, 'tragedy-hash-test');
INSERT INTO video (filename, userid, hash) VALUES ('Comedy.avi', 1, 'comedy-hash-test');
INSERT INTO video (filename, userid, hash) VALUES ('Drama.webm', 1, 'drama-hash-test');


