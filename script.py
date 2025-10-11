import pandas as pd

data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C'],
    'Sales': [100, 150, 200, 250, 300, 350, 400, 450, 500],
    'Bills': [30, 45, 50, 60, 75, 85, 90, 100, 110]
}

df = pd.DataFrame(data)
group_category = df.groupby('Category')
for name_group, group in group_category:
    print(f'Grup: {name_group}')
    print(group)
    print("\n")

print('GET_GROUP')
print('Group: A')
grupo_a = group_category.get_group('A')
print(grupo_a)

print('Describe')
print(group_category.describe())