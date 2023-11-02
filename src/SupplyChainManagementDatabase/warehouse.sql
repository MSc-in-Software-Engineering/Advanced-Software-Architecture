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

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY, 
    order_state VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO inventory (order_state) VALUES ('Pending');
INSERT INTO inventory (order_state) VALUES ('Processing');
INSERT INTO inventory (order_state) VALUES ('Delivered');

