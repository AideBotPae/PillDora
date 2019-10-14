# python Canny.py -i images/pills5.jpg
from PillCounter import PillCounter

Image = PillCounter('images/pills.jpg')
Number_of_Pills = Image.count()

# Output
print("{} pills detected.".format(Number_of_Pills))