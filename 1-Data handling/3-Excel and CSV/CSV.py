import csv 
import os
os.chdir(r'E:\HASOB\1-Data handling\3-Excel and CSV')

#read csv
'''
with open('actor2.csv',newline='') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')#delimiter=';' for ; separator
    for row in reader:
        print(', '.join(row))   

'''

#write one row in csv 
'''
with open('names.csv','w',newline='') as csvfile:
    csvwriter=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL,quotechar="'")
    #QUOTE_MINIMAL :will make quote in the values the contain the same of the delimiter like f,irst_name here
    csvwriter.writerow(['id','first_name','second_name']) 
    csvwriter.writerow([1,'ahmed','adel'])
  '''  

#write many rows
"""
names=[
    (1,'ziad','adel'),
    (2,'ahemd','adel'),
    (3,'nada','adel'),
    (4,'alaa','adel')
]

with open('namesManyRows.csv','w',newline='') as csvfile:
    csvwriter=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_NONNUMERIC,quotechar="'")
    csvwriter.writerows(names)


"""

#read result in dictionary form
"""

with open('actor.csv',newline='') as csvfile:
    reader=csv.DictReader(csvfile)#delimiter=';' for ; separator
    for row in reader:
        print(row) 

"""

#write in dictionary form
#note we can add QUOTE and quotechar here like previous example
names=[{'id':2,'first_name':'klk','last_name':'adel'},
       {'id':3,'first_name':'olo','last_name':'adel'},
       {'id':4,'first_name':'hlh','last_name':'adel'}]
with open('names2.csv','w',newline='') as csvfile:
    filednames=['id','first_name','last_name']
    writer=csv.DictWriter(csvfile,fieldnames=filednames)

    writer.writeheader()
    writer.writerow({'id':1,'first_name':'zoz','last_name':'adel'})
    writer.writerows(names)