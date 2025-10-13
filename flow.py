import pandas as pd
from db_connection import import_db

# Establish the database connection
engine = import_db()

# SQL query to retrieve trip data
query = """
SELECT
    t.id AS 'Trip ID',
    t.requested_at AS 'Request Date',
    CONCAT(p.first_name, ' ', p.last_name) AS 'Passenger',
    CONCAT(d.first_name, ' ', d.last_name) AS 'Driver',
    t.fare_amount AS 'Fare Amount'
FROM trips t
JOIN passengers p ON t.passenger_id = p.id
JOIN drivers d ON t.driver_id = d.id
WHERE t.status = 'completed'
ORDER BY t.requested_at DESC;
"""

# Read SQL query into a DataFrame
df = pd.read_sql(query, con=engine)

# Convert to datetime
df['Request Date'] = pd.to_datetime(df['Request Date'], errors='coerce')

# Localize timezone to Argentina (Buenos Aires)
df['Request Date'] = df['Request Date'].dt.tz_localize('America/Argentina/Buenos_Aires')

# Extract datetime components
df['year'] = df['Request Date'].dt.year
df['month'] = df['Request Date'].dt.month
df['day'] = df['Request Date'].dt.day
df['hour'] = df['Request Date'].dt.hour
df['weekday'] = df['Request Date'].dt.day_name()

# Display key columns
print(df[['Request Date', 'year', 'month', 'day', 'hour', 'weekday']])
print("\n")

# Create a column with only the date (no time)
normalized_date = df['Request Date'].dt.normalize()
date_only = normalized_date.dt.date
df['date_only'] = date_only

# Optional secondary DataFrame with selected columns
df2 = pd.DataFrame({
    'Date': date_only,
    'Fare Amount': df['Fare Amount'],
    'Driver': df['Driver']
})

# Group trips by day and count total trips
trips_per_day = (
    df.groupby('date_only')
      .size()
      .reset_index(name='Trip_Count')
)

print(trips_per_day)

# Example for handling large datasets in chunks
# chunks = pd.read_sql(query, con=engine, chunksize=100000)
# results = []

# for chunk in chunks:
#     chunk['Request Date'] = pd.to_datetime(chunk['Request Date'], errors='coerce')
#     chunk['Request Date'] = chunk['Request Date'].dt.tz_localize('America/Argentina/Buenos_Aires')
#     chunk['date_only'] = chunk['Request Date'].dt.normalize().dt.date
#     summary = chunk.groupby('date_only').size().reset_index(name='Trip_Count')
#     results.append(summary)

# Combine partial results
# trips_per_day = pd.concat(results).groupby('date_only').sum().reset_index()
