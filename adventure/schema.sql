DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS location;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
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
  FOREIGN KEY (userid) REFERENCES user (id),
  PRIMARY KEY (hash)
);

CREATE TABLE location (
  locname VARCHAR(30),
  routename TEXT NOT NULL,
  FOREIGN KEY (routename) REFERENCES route (name),
  PRIMARY KEY (routename,locname)
);

CREATE TABLE request (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  routename TEXT NOT NULL,
  userid INTEGER, 
  videohash BINARY(64), 
  locname VARCHAR(30),
  FOREIGN KEY (routename) REFERENCES route (name),
  FOREIGN KEY (userid) REFERENCES user (id),
  FOREIGN KEY (videohash) REFERENCES video (hash),
  FOREIGN KEY (routename,locname) REFERENCES location (routename,locname)
);

INSERT INTO user (username, password) VALUES ("test","test");

INSERT INTO route (name) VALUES ("Route A");
INSERT INTO route (name) VALUES ("Route B");

INSERT INTO location (locname, routename) VALUES ("Location Alpha","Route A");
INSERT INTO location (locname, routename) VALUES ("Location Beta","Route A");
INSERT INTO location (locname, routename) VALUES ("Location Gamma","Route B");
INSERT INTO location (locname, routename) VALUES ("Location Sigma","Route B");

INSERT INTO video (filename, userid, hash) VALUES ("Tragedy.mp4", 1, "tragedy-hash-test");
INSERT INTO video (filename, userid, hash) VALUES ("Comedy.avi", 1, "comedy-hash-test");
INSERT INTO video (filename, userid, hash) VALUES ("Drama.webm", 1, "drama-hash-test");


