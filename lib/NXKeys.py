import os.path as path
import re
from binascii import hexlify as hx, unhexlify as uhx
from pathlib import Path
homeKeys = path.expanduser('~/.switch/prod.keys')
keysFile0 = Path(homeKeys)
keysFile1 = Path('keys.txt')
keysFile2 = Path('ztools\\keys.txt')

print()

class Keys(dict):
	def __init__(self, keys_type):
		self.keys_type = keys_type
		is_key  = re.compile(r'''\s*([a-zA-Z0-9_]*)\s* # name
								=
								\s*([a-fA-F0-9]*)\s* # key''', re.X)
		try:
			if keysFile0.is_file():
				f = open(keysFile0, 'r')
			if keysFile1.is_file():
				f = open(keysFile1, 'r')
			if keysFile2.is_file():
				f = open(keysFile2, 'r')
		except FileNotFoundError:
			try:
				f = open(path.join(path.dirname(path.abspath(__file__)), '%s' % self.keys_type), 'r')
			except FileNotFoundError:
				raise FileNotFoundError('Need key file %s.keys in either %s or %s' % (self.keys_type, 
					path.expanduser('~/.switch'), path.dirname(path.abspath(__file__))))
		iterator = (re.search(is_key, l) for l in f)
		super(Keys, self).__init__({r[1]: uhx(r[2]) for r in iterator if r is not None})
		f.close()

	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			raise KeyError('Missing key %s in %s' % (item, self.keys_type))

class ProdKeys(Keys):
	def __init__(self):
		super(ProdKeys, self).__init__('prod')
		if 'header_key' in self:
			self['nca_header_key'] = self.pop('header_key')

class DevKeys(Keys):
	def __init__(self):
		super(DevKeys, self).__init__('dev')

class TitleKeys(Keys):
	def __init__(self):
		super(TitleKeys, self).__init__('title')
		if 'header_key' in self:
			self['nca_header_key'] = self.pop('header_key')
