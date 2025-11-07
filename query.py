import duckdb

# Connect to your database
con = duckdb.connect('dev.duckdb')

# Query 1: Row counts
print("\n=== Row Counts ===")
result = con.execute("""
    SELECT 'ad_events' as table_name, COUNT(*) as rows FROM main.ad_events
    UNION ALL
    SELECT 'content_catalog', COUNT(*) FROM main.content_catalog
    UNION ALL
    SELECT 'conversions', COUNT(*) FROM main.conversions
""").fetchdf()
print(result)

# Query 2: Viewability rate
print("\n=== Viewability Rate ===")
result = con.execute("""
    SELECT 
        COUNT(*) as total_impressions,
        SUM(CASE WHEN view_time_ms >= 2000 THEN 1 ELSE 0 END) as viewable_impressions,
        ROUND(100.0 * SUM(CASE WHEN view_time_ms >= 2000 THEN 1 ELSE 0 END) / COUNT(*), 2) as viewability_rate_pct
    FROM main.ad_events
""").fetchdf()
print(result)

# Query 3: Click-through rate
print("\n=== Click-Through Rate ===")
result = con.execute("""
    SELECT 
        COUNT(*) as total_impressions,
        SUM(clicked) as clicks,
        ROUND(100.0 * SUM(clicked) / COUNT(*), 2) as ctr_pct
    FROM main.ad_events
""").fetchdf()
print(result)

# Query 4: Date range
print("\n=== Date Range ===")
result = con.execute("""
    SELECT 
        MIN(event_ts) as first_event,
        MAX(event_ts) as last_event,
        COUNT(DISTINCT user_id_hash) as unique_users
    FROM main.ad_events
""").fetchdf()
print(result)

con.close()
print("\n✓ Queries complete!")
