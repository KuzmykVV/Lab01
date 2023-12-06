import matplotlib.pyplot as plt

# Створіть стовпчикову діаграму
plt.hist(df[df["violation_raw"] == "Drugs"].groupby("stop_time").size())
plt.xlabel("Час доби")
plt.ylabel("Частота зупинок")
plt.show()
