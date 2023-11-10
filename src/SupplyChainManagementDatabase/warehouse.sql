CREATE TABLE warehouse (
    id SERIAL PRIMARY KEY, 
    efficiency VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE latency (
    id SERIAL PRIMARY KEY, 
    produced TIMESTAMP NOT NULL, 
    consumed TIMESTAMP NOT NULL
);

CREATE TABLE exactlatency (
    id SERIAL PRIMARY KEY, 
    time_diff INT NOT NULL
);


CREATE TABLE mqttlatency (
    id SERIAL PRIMARY KEY, 
    produced TIMESTAMP NOT NULL, 
    consumed TIMESTAMP NOT NULL
);

CREATE TABLE exactmqttlatency (
    id SERIAL PRIMARY KEY, 
    time_diff INT NOT NULL
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY, 
    order_state VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventorymanagement (
    id SERIAL PRIMARY KEY, 
    buckets_of_raw_materials VARCHAR
);

INSERT INTO inventory (order_state) VALUES ('Pending');
INSERT INTO inventory (order_state) VALUES ('Processing');
INSERT INTO inventory (order_state) VALUES ('Delivered');

