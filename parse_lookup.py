import csv
from datetime import datetime
import numpy as np

def return_fit_line(x,y):
	m,b = np.polyfit(x,y,1) #Linear fit
	return [m,b]

lookup_A = []
lookup_B = []
lookup_thermistor = []
lookup_unit = []

fit_A = np.array(0)
fit_B = np.array(0)
fit_thermistor = np.array(0)

rawLookupDataDict = [row for row in csv.DictReader(open('example_lookup.csv'), ('A', 'B', 'Thermistor', 'Unit'))]
rawLookupData = [row for row in csv.reader(open('example_lookup.csv'))]
#print("num of observations: ", len(rawLookupData)-1)

keyedLookupA = {}
keyedLookupB = {}
keyedLookupThermistor = {}
for row in rawLookupData[1:]:
	lookup_A.append(float(row[0]))
	lookup_B.append(float(row[1]))
	lookup_thermistor.append(float(row[2]))
	lookup_unit.append(float(row[3]))
for row in rawLookupDataDict[1:]:
	keyedLookupA[row['A']] = row
	keyedLookupB[row['B']] = row
	keyedLookupThermistor[row['Thermistor']] = row
#print("Values for 6V: ", keyedLookupData['6'])

fit_A = return_fit_line(lookup_A, lookup_unit)
fit_B = return_fit_line(lookup_B, lookup_unit)
fit_thermistor = return_fit_line(lookup_thermistor, lookup_unit)

#print("Interpolated value at 2V for B: ", round(fit_B[0]*2 + fit_B[1]))

with open('example_output.csv', mode = 'w') as output_file:
	with open('example_field_readings.csv', mode = 'r') as field_values_readonly:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		field_values_reader = csv.reader(field_values_readonly, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		all = []
		row = next(field_values_reader)
		row.extend(['Unit'])
		all.append(row)
		for row in field_values_reader:
			if row[1] in keyedLookupA:
				value = keyedLookupA[row[1]]
				temp_at_A = value['Unit']
			else:
				temp_at_A = round(float(row[1])*float(fit_A[0])+fit_A[1],4)

			if row[2] in keyedLookupB:
				value = keyedLookupB[row[2]]
				temp_at_B = value['Unit']
			else:
				temp_at_B = round(float(row[2])*float(fit_B[0])+fit_B[1],4)

			if row[3] in keyedLookupThermistor:
				value = keyedLookupThermistor[row[3]]
				temp_at_therm = value['Unit']
			else:
				temp_at_therm = round(float(row[3])*float(fit_thermistor[0])+fit_thermistor[1],4)

			all_temps = [temp_at_B, temp_at_B, temp_at_therm]
			row.append(round(np.average(all_temps)))
			all.append(row)

		output_writer.writerows(all)
