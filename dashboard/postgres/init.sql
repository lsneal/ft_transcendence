CREATE ROLE django WITH LOGIN PASSWORD 'mypassword';
GRANT USAGE ON SCHEMA public TO django; 
ALTER ROLE django WITH SUPERUSER;

CREATE ROLE devops WITH LOGIN PASSWORD 'mypassword';
GRANT USAGE ON SCHEMA public TO devops; 
ALTER ROLE devops WITH SUPERUSER;