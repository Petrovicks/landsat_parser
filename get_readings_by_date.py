import csv

#reading * 1000000/10521
MICROVOLTS_SCALING_FACTOR = float(1000000/10521)

def interpolate(microvolts, channel):
	return {
		'A': (microvolts + 369.61) / 1.2706,
		'B': (microvolts + 628.65) / 1.9534,
		'Thermistor': microvolts,
	}.get(channel, 'Invalid argument.')

print("================================")
print("Parser for Landsat data")
print("================================")
output_name = raw_input("\nEnter desired output filename (e.g: specific_readings.csv)\nFilename: ")

with open (output_name, mode = 'w') as output_file:
	with open ('field_readings.csv', mode = 'r') as field_readings:
		output_write = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		field_values = csv.reader(field_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		print("\nType 0 to read in desired dates from a csv file.")
		user_input = raw_input("Type 1 to manually type a single desired reading by date.\nInput: ")
		output_write.writerow(['Time', 'A (uV)', 'A (C)', 'B (uV)', 'B (C)', 'Thermistor (uV) ?', 'Thermistor (C) ?'])

		if user_input == '1':
			reading_num = raw_input("\nEnter date (YYYY-MM-DD HH:MM:SS): ")
		elif user_input == '0':
			file_with_dates = raw_input("\nFile with dates (e.g: 'date_list.csv'): ")
			try:
				with open (file_with_dates, mode = 'r') as dates:
					date_values = csv.reader(dates, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					reading_num = []
					for rows in date_values:
						reading_num.append(rows[0])
				print reading_num
				dates.close()
			except Exception, e:
				print("Invalid filename or file format.\n")
				raise TypeError(e)
		else:
			raise TypeError("Invalid input, exiting..")

		everything_to_write = []
		new_row = []

		for row in field_values:
			if row[0] in reading_num:
				new_row = []
				scaled_A = MICROVOLTS_SCALING_FACTOR*float(row[1])
				scaled_B = MICROVOLTS_SCALING_FACTOR*float(row[2])
				new_row.extend([row[0]])
				new_row.extend([scaled_A, interpolate(scaled_A, 'A')])
				new_row.extend([scaled_B, interpolate(scaled_B, 'B')])
				new_row.extend([row[3], interpolate(float(row[3]), 'Thermistor')])
				everything_to_write.append(new_row)
		try:
			output_write.writerows(everything_to_write)
			print("Successfully wrote readings to {}".format(output_name))
		except Exception, e:
			print("Error writing to file.\n")
			raise TypeError(e)
