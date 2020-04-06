from fyspider import FySpyder
from weather import Weather
fy = FySpyder()

fy.parse()
# print(s)
w = Weather()
print(w.parse()[0], w.parse()[1])
