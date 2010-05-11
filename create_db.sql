create database ion;
use ion;
create user ion_user identified by 'ion_pass';
grant usage on *.* to ion_user@localhost identified by 'ion_pass';
grant all privileges on ion.* to ion_user@localhost;
create table user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);
commit;