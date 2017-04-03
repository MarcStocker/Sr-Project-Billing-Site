#!/mnt/c/Dropbox/WebSites/Sr-Project-Billing-Site/codingenv/bin/python
import os

print("Invoking Django Shell")

os.system('python ../manage.py shell')

print("Inkoked...")
print("printing a user:")
from billing.models import Roommates
for i in Roommates:
  print(i)

print("\nClosing Shell")
exit()
print("Closing script")
exit
