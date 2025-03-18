import psycopg2

# Database connection details
database_url = "postgresql://postgres:Pp75982723@test-usuario.crgygo2mye4q.us-east-2.rds.amazonaws.com:5432/postgres"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    # Get all tables in the 'public' schema
    cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
    tables = cur.fetchall()

    print("Fetching data from all tables...\n")
    
    # Iterate through each table and select all rows
    for table in tables:
        table_name = table[0]
        print(f"📌 Table: {table_name}")
        
        try:
            cur.execute(f'SELECT * FROM "{table_name}" LIMIT 10;')  # Limit to 10 rows per table
            rows = cur.fetchall()
            
            if rows:
                for row in rows:
                    print(row)
            else:
                print("⚠️ No data found.")

        except Exception as table_error:
            print(f"⚠️ Error reading table {table_name}: {table_error}")

        print("\n" + "-"*50 + "\n")

    # Close connection
    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)
