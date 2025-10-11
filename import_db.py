import pandas as pd
from db_connection import import_db

# Get the database engine
engine = import_db()

query = """
SELECT
    t.id AS 'ID Viaje',
    t.requested_at AS 'Fecha Solicitud',
    CONCAT(p.first_name, ' ', p.last_name) AS 'Pasajero',
    CONCAT(d.first_name, ' ', d.last_name) AS 'Conductor',
    t.fare_amount AS 'Monto'
FROM trips t
JOIN passengers p ON t.passenger_id = p.id
JOIN drivers d ON t.driver_id = d.id
WHERE t.status = 'completed'
ORDER BY t.requested_at DESC;
"""

# Read SQL query into a DataFrame
df = pd.read_sql(query, con=engine)
print(df.head())
print("\n")

# Aggregate total amount per driver
sum_amount = df.groupby('Conductor')['Monto'].sum().reset_index()
sum_amount.columns = ['Driver', 'Amount']
print(sum_amount)
print("\n")
