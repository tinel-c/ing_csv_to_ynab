﻿## ING csv to YNAB csv converter
##
## What does YNAB look for in a CSV file?
## In order to import a CSV file into YNAB it must follow a specific structure. The 3 line example below outlines exactly how a file might look if it contained only 2 transactions.
##
## Date,Payee,Category,Memo,Outflow,Inflow
## 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,
## 01/26/12,Sample Payee 2,,Sample memo for an inflow,,500.00
##
## To format your file the way YNAB requires, open it in a text editor and make your transactions look like the sample ones above.
##
## You'll notice every field is separated by a comma so it's important that every field is present in each line, even if your transactions don't fill every field. Always include the "Date,Payee,Category,Memo,Outflow,Inflow" line at the very top as it is required. 
##
## Any field can be left blank except the date. Valid date formats:
##
## DD/MM/YY
## DD/MM/YYYY
## DD/MM//YYYY
## MM/DD/YY
## MM/DD/YYYY
## MM/DD//YYYY
##
## Categories will only import if the category already exists in your budget file with the exact same name. Otherwise the categories will be ignored when importing the file.  Also, make sure that the categories are listed with the master category, followed by a colon, then the sub category.  For example Everyday Expenses: Groceries
##
## FREE online conversion tools
## Custom YNAB specific tool → http://halloffame.github.io/ynab-csv/ 
## Instructions on how to use it → https://github.com/halloffame/ynab-csv/blob/gh-pages/README.md
##
## Generic CSV conversion → http://csvconverter.gginternational.net/
##
## CSV Desktop software
## Windows - CSVed - Cardware
##
## Mac - XTabulator - $19.99 USD



import csv
import glob

mappingCategory = [ ('CARREFOUR ROMANIA', 'Everyday Expenses: Mancare'),
                    ('LIDL', 'Everyday Expenses: Mancare'),
                    ('EON GAZ FURNZARE', 'Monthly Bills: Gaz'),
                    ('WWW.MYLINE-EON.RO', 'Monthly Bills: Gaz'),
                    ('DEDEMAN', 'Everyday Expenses: Household Goods'),
                    ('EMAG SHOWR', 'Everyday Expenses: Household Goods'),
                    ('DM FIL', 'Everyday Expenses: Household Goods'),
                    ('MOL', 'Everyday Expenses: Benzina/Motorina'),
                    ('IASI ETAX', 'Yearly bills: Impozite'),
                    ('ING Gold', 'Yearly bills: Impozite'),
                    ('digicare.rcs-rds.ro', 'Monthly Bills: RCS/RDS'),
                    ('Netflix', 'Monthly Bills: Netflix'),
                    ('ARCADIA', 'Everyday Expenses: Medical'),
                    ('ARTIMA', 'Everyday Expenses: Medical'),
                    ('SMILE DENT SRL', 'Everyday Expenses: Medical'),
                    ('FITERMAN', 'Everyday Expenses: Medical'),
                    ('SENSIBLU', 'Everyday Expenses: Medical'),
                    ('KOTON', 'Everyday Expenses: Haine'),
                    ('TAKKO', 'Everyday Expenses: Haine'),
                    ('ZARA', 'Everyday Expenses: Haine'),
                    ('ZARA', 'Everyday Expenses: Haine'),
                    ('H&M', 'Everyday Expenses: Haine'),
                    ('INA IULIUS MALL', 'Everyday Expenses: Haine'),
                    ('HBOEUROPESRO', 'Monthly Bills: HBOgo'),
                    ('PASTICCERIA MONTECAT', 'Everyday Expenses: Restaurante'),
                    ('KFC', 'Everyday Expenses: Restaurante'),
                    ('Rata Credit In contul: 9999', 'Debt: Credit apartament Buni'),
                    ('ORANGE ROMANIA', 'Monthly Bills: Telefon Tinel'),
                    ('GLOBEHOSTIN', 'Yearly bills: Site-uri')]
data = ""
detalii_tranzactie = ""
debit = ""
credit = ""
category = ""

## map category to usual stores
## eg. Lidl, Everyday Expenses: Mancare
def findCategory( memoString ):
        for stringMapping, mappedCategory in mappingCategory:
                if memoString.find(stringMapping)>0:
                        return mappedCategory
        return ""


for filename in glob.glob('*.csv'):
        witeToFilename = "ynab_"+filename
        with open(witeToFilename, 'wb') as csvfile:
                fieldnames = ['Date','Payee','Category','Memo','Outflow','Inflow']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                with open(filename) as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:        
                                if row['Data']:
                                        if data:
                                                print 'output: '+data+','+detalii_tranzactie+',"'+debit+'","'+credit+'"'
                                                ## try to identify category
                                                category = findCategory(detalii_tranzactie)
                                                ## write the entry in YNAB csv
                                                writer.writerow({'Date': data, 'Memo': detalii_tranzactie, 'Outflow': debit , 'Inflow': credit, 'Category' : category})
                                        print '----->'+row['Data']+','+row['Detalii tranzactie']+',"'+row['Debit']+'","'+row['Credit']+'"'
                                        data = row['Data']
                                        ## Replace the romanian month by the number of the month
                                        data = data.replace(" ianuarie ","/01/")
                                        data = data.replace(" februarie ","/02/")
                                        data = data.replace(" martie ","/03/")
                                        data = data.replace(" aprilie ","/04/");
                                        data = data.replace(" mai ","/05/");
                                        data = data.replace(" iunie ","/06/");
                                        data = data.replace(" iulie ","/07/");
                                        data = data.replace(" august ","/08/");
                                        data = data.replace(" septembrie ","/09/");
                                        data = data.replace(" octombrie ","/10/");
                                        data = data.replace(" noiembrie ","/11/");
                                        data = data.replace(" decembrie ","/12/");
                                        detalii_tranzactie = row['Detalii tranzactie']
                                        debit = row['Debit'] 
                                        credit = row['Credit']
                                else:
                                        detalii_tranzactie = detalii_tranzactie + ' ' + row['Detalii tranzactie']
                        print 'output: '+data+','+detalii_tranzactie+',"'+debit+'","'+credit+'"'
                        ## try to identify category
                        category = findCategory(detalii_tranzactie)
                        ## write the entry in YNAB csv
                        writer.writerow({'Date': data, 'Memo': detalii_tranzactie, 'Outflow': debit , 'Inflow': credit, 'Category' : category})                   
                        
