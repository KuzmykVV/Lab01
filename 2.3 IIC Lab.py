import matplotlib.pyplot as plt

# Створіть стовпчикову діаграму
plt.hist(df.groupby("stop_time").size())
plt.xlabel("Час доби")
plt.ylabel("Частота зупинок")
plt.show()
