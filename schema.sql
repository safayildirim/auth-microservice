CREATE TABLE IF NOT EXISTS USER (
  RECORD_ID varchar(32),
  USERNAME varchar(32) unique not null,
  EMAIL varchar(64) unique not null,
  FIRSTNAME varchar(64),
  LASTNAME varchar(64),
  PASSWORD varchar(128),
  STATUS varchar(16),
  primary key(id)
);
