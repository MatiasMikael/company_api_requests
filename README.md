## company_api_requests

### Project overview
This project fetches company data from the Kaupparekisterin Rekisteröidyt Ilmoitukset API, stores it in Snowflake, and analyzes it using SQL queries. The results are exported as .csv files for further use.

### Technologies Used

* Python Libraries: requests, snowflake-connector-python, dotenv, csv
* Database: Snowflake
* Tools: VS Code, CLI

### Steps to Run

1. `pip install requirements.txt`
2.  Create a .env file with Snowflake credentials:
env

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

3. Run the script:
`python 1_scripts/get_companies.py`

4. Execute SQL queries from 2_sql_queries and save results in 3_results.

### Project Structure

- 1_scripts: Python scripts.
- 2_sql_queries: SQL queries.
- 3_results: Query results in .csv format.
- 4_docs: Screenshot of successful execution.

### License

This project is licensed under the MIT License. Data from the Kaupparekisterin Rekisteröidyt Ilmoitukset API is licensed under Creative Commons Attribution 4.0 International License. https://www.avoindata.fi/data/fi/apiset/kaupparekisterin-rekisteroidyt-ilmoitukset-api
