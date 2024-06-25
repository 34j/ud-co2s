import plotext as plt

plt.clf()
dates = ["01/03 00:00:00", "01/04 00:00:00"]
nlvs = [1, 2]
plt.date_form("Y/m/d H:M:S")
plt.plot(dates, nlvs)
plt.show()
