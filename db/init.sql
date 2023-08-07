SELECT 'CREATE DATABASE fitsync'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fitsync')\gexec