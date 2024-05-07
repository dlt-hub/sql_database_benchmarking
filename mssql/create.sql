CREATE DATABASE dlt_data;

CREATE LOGIN loader WITH PASSWORD = 'loader-xXx$%';  

-- this part must be created in one run
USE dlt_data;
GO;
CREATE USER loader_user FOR LOGIN loader;
GO;
-- make user dbowner
USE dlt_data;
GO;
ALTER ROLE [db_owner] ADD MEMBER loader_user;
GO;
