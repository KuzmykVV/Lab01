import matplotlib.pyplot as plt

# Розрахуйте середній час зупинки для кожної причини зупинки
stop_duration_by_violation = df.groupby("violation_raw")["stop_duration"].mean()

# Створіть стовпчикову діаграму
plt.bar(stop_duration_by_violation.index, stop_duration_by_violation.values)
plt.xlabel("Причина зупинки")
plt.ylabel("Середній час зупинки")
plt.show()
