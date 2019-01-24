import csv
from datetime import datetime
import numpy as np

def return_fit_line(x,y):
	m,b = np.polyfit(x,y,1) #Linear fit
	return [m,b]

lookup_voltage = []
lookup_A = []
lookup_B = []
lookup_unit = []

fit_A = np.array(0)
fit_B = np.array(0)
fit_unit = np.array(0)

rawLookupDataDict = [row for row in csv.DictReader(open('example_lookup.csv'), ('Voltage', 'A', 'B', 'Unit'))]
rawLookupData = [row for row in csv.reader(open('example_lookup.csv'))]
#print("num of observations: ", len(rawLookupData)-1)

keyedLookupData = {}
for row in rawLookupData[1:]:
	lookup_voltage.append(int(row[0]))
	lookup_A.append(float(row[1]))
	lookup_B.append(float(row[2]))
	lookup_unit.append(float(row[3]))
for row in rawLookupDataDict[1:]:
	keyedLookupData[row['Voltage']] = row
#print("Values for 6V: ", keyedLookupData['6'])

print(lookup_voltage)

fit_A = return_fit_line(lookup_voltage, lookup_A)
fit_B = return_fit_line(lookup_voltage, lookup_B)
fit_unit = return_fit_line(lookup_voltage, lookup_unit)

#print("Interpolated value at 2V for B: ", round(fit_B[0]*2 + fit_B[1]))

with open('example_output.csv', mode = 'w') as output_file:
	with open('example_field_readings.csv', mode = 'r') as field_values_readonly:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		field_values_reader = csv.reader(field_values_readonly, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		all = []
		row = next(field_values_reader)
		row.extend(['A','B', 'Unit'])
		all.append(row)
		for row in field_values_reader:
			if row[1] in keyedLookupData:
				value = keyedLookupData[row[1]]
				row.append(value['A'])
				row.append(value['B'])
				row.append(value['Unit'])
			else:
				row.append(round(float(row[1])*float(fit_A[0])+fit_A[1],1))
				row.append(round(float(row[1])*float(fit_B[0])+fit_B[1],1))
				row.append(round(float(row[1])*float(fit_unit[0])+fit_unit[1],1))
			all.append(row)

		output_writer.writerows(all)
