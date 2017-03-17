import pandas as pd

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
print("=======================")
print("== Running importcsv ==")
print("=======================")
print("")

fields=['ID','Name','Payment Type','Amount','Pay To','Date','Details']

print("---- Reading from Payments.cvs ----")
paymentsdf=pd.read_cvs('Payments.cvs',skipinitialspace=True,usecols=fields,encoding="ISO-8859-1")

print(paymentsdf)
