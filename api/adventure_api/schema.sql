DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS route;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS admin;

CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  username VARCHAR(15) UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE admin (
  username VARCHAR(15) PRIMARY KEY,
  password TEXT NOT NULL
);

CREATE TABLE route (
  name TEXT UNIQUE NOT NULL,
  PRIMARY KEY (name)
);


CREATE TABLE video (
  filename VARCHAR(50),
  thumbnail VARCHAR(50),
  userid INTEGER, 
  FOREIGN KEY (userid) REFERENCES customer (id),
  PRIMARY KEY (userid, filename)
);

CREATE TABLE location (
  locname VARCHAR(50),
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
  videoname VARCHAR(50) NOT NULL,
  locname VARCHAR(50) NOT NULL,
  date_decision TIMESTAMP,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  approved BOOLEAN DEFAULT False,
  remarks TEXT,
  FOREIGN KEY (routename) REFERENCES route (name),
  FOREIGN KEY (userid) REFERENCES customer (id),
  FOREIGN KEY (userid, videoname) REFERENCES video (userid, filename),
  FOREIGN KEY (userid, routename, locname) REFERENCES location (userid, routename, locname)
);

INSERT INTO customer (username, password) VALUES ('test', 'test');
INSERT INTO admin (username, password) VALUES ('admin', 'admin');

INSERT INTO route (name) VALUES ('Route A');
INSERT INTO route (name) VALUES ('Route B');
INSERT INTO route (name) VALUES ('Route C');
INSERT INTO route (name) VALUES ('Route D');


INSERT INTO location (userid, locname, routename) VALUES (1,'Location Alpha','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Beta','Route A');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Gamma','Route B');
INSERT INTO location (userid, locname, routename) VALUES (1,'Location Sigma','Route B');


INSERT INTO video (filename, userid, thumbnail) VALUES ('minecraft.mp4', 1, 'minecraft_thumbnail.jpeg');

INSERT INTO request (routename, userid, videoname, locname) VALUES ('Route A', 1, 'minecraft.mp4', 'Location Alpha');
INSERT INTO request (routename, userid, videoname, locname) VALUES ('Route B', 1, 'minecraft.mp4', 'Location Gamma');

