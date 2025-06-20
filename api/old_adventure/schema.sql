DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  isAdmin BOOLEAN DEFAULT False,
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
  FOREIGN KEY (userid) REFERENCES customer (id),
  PRIMARY KEY (userid, filename)
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
  userid INTEGER NOT NULL, 
  videoname VARCHAR(30) NOT NULL,
  locname VARCHAR(30) NOT NULL,
  date_decision TIMESTAMP,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  approved BOOLEAN DEFAULT False,
  remarks TEXT,
  FOREIGN KEY (routename) REFERENCES route (name),
  FOREIGN KEY (userid) REFERENCES customer (id),
  FOREIGN KEY (userid, videoname) REFERENCES video (userid, filename),
  FOREIGN KEY (userid, routename, locname) REFERENCES location (userid, routename, locname)
);

INSERT INTO customer (username, password) VALUES ('test','test');
INSERT INTO customer (username, password, isAdmin) VALUES ('admin','admin', TRUE);

INSERT INTO route (name) VALUES ('Route A');
INSERT INTO route (name) VALUES ('Route B');

INSERT INTO location (userid, locname, routename) VALUES (1,'Location Alpha','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Beta','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Gamma','Route B');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Sigma','Route B');

INSERT INTO video (filename, userid) VALUES ('top_500_cheese.mp4', 1);

INSERT INTO request (routename, userid, videoname, locname) VALUES ('Route A', 1, 'top_500_cheese.mp4', 'Location Alpha');
INSERT INTO request (routename, userid, videoname, locname) VALUES ('Route B', 1, 'top_500_cheese.mp4', 'Location Gamma');

