-- create the databases
CREATE DATABASE IF NOT EXISTS melidatabase;

-- create the users for each database
CREATE USER 'meliuser'@'%' IDENTIFIED BY 'melipsw123';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `melidatabase`.* TO 'meliuser'@'%';

FLUSH PRIVILEGES;

USE melidatabase;

CREATE TABLE IF NOT EXISTS product (
        id VARCHAR(128) NOT NULL,
        site VARCHAR(8) NOT NULL,
        price DOUBLE(11,2) UNSIGNED,
        start_time DATETIME,
        name VARCHAR(128),
        description TEXT,
        nickname VARCHAR(128),
 CONSTRAINT pk_id_site PRIMARY KEY (id, site)
);