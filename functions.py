import pandas as pd

data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C'],
    'Sales': [100, 150, 200, 250, 300, 350, 400, 450, 500],
    'Bills': [30, 45, 50, 60, 75, 85, 90, 100, 110]
}

df = pd.DataFrame(data)

def rango(x):
    return x.max() - x.min()

sales_rango = df.groupby('Category') ['Sales'].agg(rango).to_frame('Sales_rango')
print(sales_rango)
print("\n")

sales_stadistic = df.groupby('Category') ['Sales'].agg(['mean', rango])
print(sales_stadistic)
print("\n")

some_rangos = df.groupby('Category').agg({
    "Sales":rango,
    "Bills":['mean', rango]
    })
some_rangos.columns = ['_'.join(col).strip() for col in some_rangos.columns.values]
print(some_rangos)
print("\n")

def margin_promedy(group):
    group['Margin'] = group['Sales'] - group['Bills']
    return group['Margin'].mean()
margin_per_category = df.groupby('Category').apply(margin_promedy, include_groups=False)
print(margin_per_category)
print("\n")