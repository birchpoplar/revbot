# Revbot Development Notes

## Initial Project Creation

### PostGRES SQL - create local database

Here are the general steps to create a user and database with PostgreSQL:

`sudo -u postgres psql`

Create a new database (replace "mydatabase" with your desired database name):

`CREATE DATABASE mydatabase;`

Create a new user (replace "myuser" with your desired username and "mypassword" with your desired password):

`CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';`

Grant all privileges on the database to the new user:

`GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;`

Exit the PostgreSQL command line interface:

`\q`

## Next up 6/5/23
- Invoiced before/after revenue earned (unbilled rev etc.)
- Then if works can implement API