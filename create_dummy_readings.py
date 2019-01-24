import csv
import random
from datetime import datetime
import time

with open('example_field_readings.csv', mode = 'w') as field_values:
	field_values_writer = csv.writer(field_values, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	field_values_writer.writerow(['Timestamp', 'Voltage', 'Temperature'])
	for i in range(10):
		field_values_writer.writerow([datetime.now().replace(microsecond=0), random.randint(2,7), random.randint(33,37)])
		random_sleep_interval = random.randint(1,2)
		time.sleep(random_sleep_interval)
