import pandas as pd
from db_connection import import_db

engine = import_db()

# 🧩 EXTRACT — pull data from MySQL (filtering only what’s needed)
query = """
SELECT
    t.id,
    t.requested_at,
    t.fare_amount,
    CONCAT(p.first_name, ' ', p.last_name) AS pasajero,
    CONCAT(d.first_name, ' ', d.last_name) AS conductor,
    t.status
FROM trips t
JOIN passengers p ON t.passenger_id = p.id
JOIN drivers d ON t.driver_id = d.id
WHERE t.requested_at >= '2025-01-01';
"""
df = pd.read_sql(query, con=engine)

# ⚙️ TRANSFORM — cleaning and calculations with pandas
df = df[df['status'] == 'completed']                     # additional filter
df['fare_amount'] = df['fare_amount'].fillna(0)          # replace null values
df['Month'] = pd.to_datetime(df['requested_at']).dt.month  # new column
df['Year'] = pd.to_datetime(df['requested_at']).dt.year

# Group by driver
summary = (
    df.groupby('conductor')['fare_amount']
    .agg(['count', 'sum', 'mean'])
    .reset_index()
    .rename(columns={'count': 'Trip_Count', 'sum': 'Total_Amount', 'mean': 'Average_Amount'})
)

# Update the amount for a specific driver (e.g., "Carlos Benítez")
summary.loc[summary['conductor'] == 'Carlos Benítez', 'Total_Amount'] = 9999

# Example: Change a specific cell manually (e.g., row 3, column 2)
# sheet.cell(row=3, column=2, value=9999)

# 💾 LOAD — save or export the result
summary.to_excel('driver_trip_summary.xlsx', index=False)

print(summary)
