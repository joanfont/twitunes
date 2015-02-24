import hashlib

def md5(string):
	md5 = hashlib.md5(string)
	return md5.hexdigest()