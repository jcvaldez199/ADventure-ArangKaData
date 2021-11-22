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
  startindex INTEGER DEFAULT 0,
  lastindex INTEGER DEFAULT 0,
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

INSERT INTO route (name) VALUES ('EDSA');
INSERT INTO route (name) VALUES ('CRMT');


INSERT INTO location (userid, locname, routename, startindex, lastindex) VALUES (1,'Entire','EDSA',0,852);
INSERT INTO location (userid, locname, routename, startindex, lastindex) VALUES (1,'Entire','CRMT',0,562);
INSERT INTO location (userid, locname, routename, startindex, lastindex) VALUES (1,'EDSA Generic','EDSA',100,350);
INSERT INTO location (userid, locname, routename, startindex, lastindex) VALUES (1,'CRMT Generic','CRMT',100,350);
--INSERT INTO location (userid, locname, routename, startinglat, startinglon, lastlat, lastlon) VALUES (1,'Entire','EDSA',14.657421, 120.987622, 14.508795, 120.990605);
--INSERT INTO location (userid, locname, routename, startinglat, startinglon, lastlat, lastlon) VALUES (1,'Entire','CRMT',14.70145, 121.08679, 14.761697, 121.159134);

INSERT INTO video (filename, userid, thumbnail) VALUES ('minecraft.mp4', 1, 'minecraft_thumbnail.jpeg');

INSERT INTO request (routename, userid, videoname, locname) VALUES ('EDSA', 1, 'minecraft.mp4', 'Entire');
INSERT INTO request (routename, userid, videoname, locname) VALUES ('CRMT', 1, 'minecraft.mp4', 'Entire');

