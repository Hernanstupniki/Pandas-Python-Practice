import pandas as pd

data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C'],
    'Sales': [100, 150, 200, 250, 300, 350, 400, 450, 500],
    'Bills': [30, 45, 50, 60, 75, 85, 90, 100, 110]
}
df = pd.DataFrame(data)

sum_groups = df.groupby('Category').sum()
print(sum_groups)
print("\n")

sum_groups = df.groupby('Category').mean()
print(sum_groups)
print("\n")

aggregate_results = df.groupby('Category').agg(['sum','mean','max'])
aggregate_results.columns = ['Sales_sum', 'Sales_promedy', 'Sales_max', 'Bills_sum', 'Bills_promedy', 'Bills_max']
print(aggregate_results)
print("\n")

personalized_results = df.groupby('Category').agg({'Sales':'sum','Bills':'mean'})
personalized_results.columns = ['Sales_sum', 'Bills_promedy']
print(personalized_results)
print("\n")