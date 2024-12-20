import os
from dotenv import load_dotenv
import requests
import snowflake.connector

# Load environment variables from .env file
load_dotenv()

# Fetch Snowflake credentials from environment variables
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

# API URL
url = "https://avoindata.prh.fi/opendata-registerednotices-api/v3/?companyForm=OY&registrationDateStart=2024-12-01"

try:
    # Fetch data from API
    print("Fetching data from API...")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Check if the 'companies' key exists
        if "companies" in data:
            results = data["companies"]
            print(f"Total records fetched: {len(results)}")

            # Connect to Snowflake
            print("Connecting to Snowflake...")
            conn = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                schema=schema
            )
            cursor = conn.cursor()

            # Create table if not exists
            print("Ensuring the table exists...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    businessId STRING PRIMARY KEY,
                    name STRING,
                    registrationDate DATE,
                    companyForm STRING
                )
            """)

            # Insert data into Snowflake
            inserted_count = 0
            print("Inserting data into Snowflake...")
            for company in results:
                try:
                    # Extract fields from the JSON structure
                    business_id = company["businessId"]["value"]
                    name = company["names"][0]["name"]
                    registration_date = company["businessId"]["registrationDate"]
                    company_form = company["companyForms"][0]["descriptions"][2]["description"]  # Finnish name

                    # Insert into the database
                    cursor.execute("""
                        INSERT INTO companies (businessId, name, registrationDate, companyForm)
                        VALUES (%s, %s, %s, %s)
                    """, (business_id, name, registration_date, company_form))
                    inserted_count += 1
                except Exception as e:
                    print(f"Error inserting record for businessId {company['businessId']['value']}: {e}")

            # Commit the transaction
            conn.commit()
            print(f"Data insertion complete. Total rows inserted: {inserted_count}")

            # Close connections
            cursor.close()
            conn.close()

            # Final message
            if inserted_count > 0:
                print(f"Data successfully sent to Snowflake. Total rows inserted: {inserted_count}")
            else:
                print("No data was inserted into Snowflake.")
        else:
            print("Unexpected API response structure. Key 'companies' not found.")
    else:
        print(f"API Error: {response.status_code}, Message: {response.text}")

except Exception as e:
    print(f"Unexpected error: {e}")