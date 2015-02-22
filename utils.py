import hashlib

def md5(string):
	md5 = hashlib.md5(string.encode())
	return md5.hexdigest()