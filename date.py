from datetime import date , timedelta , datetime
from datetime import datetime , time
import locale
locale.setlocale(locale.LC_ALL,"russian")

dt_2 = date(2020 , 10 , 15  )

delta = timedelta(days=1 )

dt_2 - delta
print(dt_2 - delta)

dt_2 + delta
print(dt_2 + delta)




delta2= timedelta(days=30)
print(dt_2 - delta2)





dt_now2 = datetime.now()
ht = dt_now2.strftime("%d. %m.%Y %H:%M")
print(ht)


from datetime import datetime
c = datetime.strptime('01/01/17 12:10:03.099000', '%m/%d/%y %H:%M:%S.%f')
print(c)


c = datetime.now()
print(c)

print(c.strftime("%A %d %B %Y  "))
print(c)

