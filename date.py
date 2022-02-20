from datetime import datetime

import calendar



laststr = "18/02/22 14:00"
lastwithdrawal = datetime.strptime(laststr, '%d/%m/%y %H:%M')


print(lastwithdrawal.day)
print(lastwithdrawal.year)
print(lastwithdrawal.hour)
print()
