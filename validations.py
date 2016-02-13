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
	if _sex in ["M", "F"]:
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

def cred(_cred):
	"""Validations for credits"""
	try:
		if int(_cred) in xrange(1, 5):
			return True
	except:
		pass
	print "Incorrect credits, should be between 1 and 4 only."
	return False

def c_type(_c_type):
	"""Validations for credits"""
	if _c_type in ["UG", "PG"]:
		return True
	print "Incorrect course type, should be UG or PG only."
	return False

def sem(_sem, _type):
	limit = {"UG": 8, "PG": 2}
	lim = limit[_type]
	try:
		if int(_sem) in xrange(1, lim+1):
			return True
	except:
		pass
	print "Incorrect sem, should be within 1-8 for UG and 1-2 for PG."
	return False

