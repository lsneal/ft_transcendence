CREATE ROLE django WITH LOGIN PASSWORD 'mypassword';
GRANT USAGE ON SCHEMA public TO django; 
ALTER ROLE django WITH SUPERUSER;

CREATE ROLE logstash WITH LOGIN PASSWORD 'mypassword';
GRANT USAGE ON SCHEMA public TO logstash; 
ALTER ROLE logstash WITH SUPERUSER;