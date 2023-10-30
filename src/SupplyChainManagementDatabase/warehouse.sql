CREATE TABLE warehouse (
    id SERIAL PRIMARY KEY, 
    efficiency VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE latency (
    id SERIAL PRIMARY KEY, 
    produced VARCHAR(255) NOT NULL, 
    consumed TIMESTAMP NOT NULL
);


