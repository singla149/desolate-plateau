import datetime, re

def date(_date):
	"""Validations for date"""
	try:
		datetime.datetime.strptime(_date, '%Y-%m-%d')
		return True
	except ValueError:
		print "Incorrect date format, should be YYYY-MM-DD"
		return False

def sex(_sex):
	"""Validations for sex"""
	if _sex in ["M", "F", "m", "f"]:
		return True
	print "Incorrect format, should be M/F"
	return False

def name(_name):
	"""Validations for name"""
	if re.match(r"[a-z.A-Z\s]+$",_name):
		return True
	print "Incorrect format, name shouldn't contain any special characters or numbers."
	return False

def phno(_phno):
	"""Validations for phone number"""
	if re.match(r"^[0-9]{10}$",_phno):
		return True
	print "Incorrect format, phone number should be of 10 digits long and should contain numbers only."
	return False