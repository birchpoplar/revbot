# Revbot - Revenue Recognition Concept API

## Goals

Create environment with API endpoints for creating and managing customers, contracts, revenue segments and invoices in a SaaS-like construct. Ultimate goal is to interface with an LLM enabling natural language specification of revenue contracts and demonstrate the translation to an accounting ledger with compliant revenue recognition.

## Main Definitions

- **Customer** Simple customer with name
- **Contract** Linked to a customer, specifies `booked_month`, which is the month (as integer) in which a contract is booked
- **RevenueSegment** Linked to a contract. A RevenueSegment comprises a revenue recognition schedule and associated invoices.
- **Invoice** Linked to a RevenueSegment.

Objects are created and linked together. A `populate_dataframe` function builds a Pandas dataframe that shows the following in a typical financial statement format:
- TCV, Total Contract Value
- Rev, Revenue
- DefRev, Deferred Revenue
- UnbilledRev, Unbilled Revenue
- AR, Accounts Receivable
- Cash, Cash

## Database Implementations

The `DevelopmentConfig` is for a localhost PostgreSQL database. The `TestingConfig` can use that or a temporary sqlite config.

Next step: cloud-hosted, probably Heroku, for `ProductionConfig`.

## API Definitions

### `POST /customers`
Creates a new customer

**Request Body:**
```json
{
    "name": "string"
}
```

**Response:**
```json
{
    "id": "int",
    "message": "string"
}
```

## Some Configuration Notes

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
