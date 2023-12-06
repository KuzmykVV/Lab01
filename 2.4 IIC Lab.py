# Визначте мінімальний допустимий час зупинки
min_duration = 1

# Замініть всі значення менше мінімального на NaN
df["stop_duration"].replace(to_replace=lambda x: x < min_duration, value=np.nan, inplace=True)
