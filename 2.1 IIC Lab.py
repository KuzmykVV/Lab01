import pandas as pd

# Завантажте набір даних
df = pd.read_csv("police_project.csv")

# Перетворіть расу на числові значення
df["race"] = df["race"].replace("White", 0)
df["race"] = df["race"].replace("Black", 1)

# Розрахуйте частоту зупинок за расою
stop_counts = df.groupby("race").size()

# Виведіть результати
print(stop_counts)
