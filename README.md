Simple python-based csv parser used to correlate voltage and temperatures with field readings and Landsat data.

Should be compatable with both Python2 and Python3.

Usage Notes:
- CURRENTLY ONLY WORKS WITH CSV FILES
	- This can be changed if desired.
- field_readings.csv is hardcoded at the moment but can be changed.
- Changing the current working directory of the script can also be made dynamic, if that's something that could be helpful.
- User inputs an output filename
	- NOTE: Filename needs its extension "file.csv" instead of just "file".
- Input can either be a single user-inputted date, or a csv with a list of dates in its first column.
