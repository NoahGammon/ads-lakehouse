import duckdb

con = duckdb.connect('ads_lakehouse.duckdb')

# Show all tables
print("\n=== All Tables in Database ===")
result = con.execute("SHOW TABLES").fetchall()
for row in result:
    print(row)

# Show all schemas
print("\n=== All Schemas ===")
result = con.execute("SHOW SCHEMAS").fetchall()
for row in result:
    print(row)

# Try to find ad_events in any schema
print("\n=== Searching for ad_events ===")
result = con.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_name LIKE '%ad%'
""").fetchall()
for row in result:
    print(row)

con.close()