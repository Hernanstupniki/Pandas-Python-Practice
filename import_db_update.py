import pandas as pd
from sqlalchemy import text
from db_connection import import_db

engine = import_db()

# 1READ — Load data from the database
df = pd.read_sql("SELECT id, fare_amount, status FROM trips", con=engine)

# VALIDATE — Detect invalid or incorrect values
errors = df[df['fare_amount'] <= 0]
print("Records with fare_amount <= 0:")
print(errors, "\n")

# 3FIX — Update database values directly (only if needed)
if not errors.empty:
    with engine.begin() as conn:  # opens a transaction and commits automatically on exit
        result = conn.execute(
            text("""
                UPDATE trips
                SET fare_amount = :new_amount
                WHERE fare_amount <= 0
            """),
            {"new_amount": 500}
        )
        print(f"Rows updated: {result.rowcount}\n")
else:
    print("No rows to update.\n")

# VERIFY — Check results after the update
updated_df = pd.read_sql(
    "SELECT id, fare_amount, status FROM trips WHERE fare_amount <= 500",
    con=engine
)
print("Rows with fare_amount <= 500 (verification):")
print(updated_df)
