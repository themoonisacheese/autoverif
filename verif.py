# -*- coding: utf-8 -*-

#this file is a lobotomy of squirell.py, taken from NSCB.
#i basically removed entire parts of its code until i was left only with a verification routine, which i patched up a bit because code quality in the original squirrel.py is horrendous.
#usage: .venv/bin/python verif.py "file"



import argparse
import sys
import os
# import urllib3

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, 'lib')
try:
	sys.path.insert(0, 'private')
except:pass	
import Config
import Status	

# # SET ENVIRONMENT
# squirrel_dir=os.path.abspath(os.curdir)
# NSCB_dir=os.path.abspath('../'+(os.curdir))

def verify(file):
	try:
		# urllib3.disable_warnings()
		parser = argparse.ArgumentParser()
		parser.add_argument('file',nargs='*')

		Status.start()


		import Fs	


	
		filename = file
		# filename = "/home/themoon/Downloads/Cult_of_the_Lamb_-_Cult_of_the_Lamb_-_Cthulhu_Follower_Form_01002E7016C47001v0DLC(1).nsz"
		dir=os.path.dirname(os.path.abspath(filename))
		tmpfolder =os.path.join(dir,'tmp')
		feed=''
		buffer = 65536

		f = Fs.Nsp(filename, 'rb')

		check,feed=f.verify()
		if check == False:
			return False

		verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
		if verdict == False:
			return False
		print(filename)
		if filename.endswith('.nsz') :
			verdict,feed=f.nsz_hasher(buffer,headerlist,verdict,feed)
		elif filename.endswith('.xcz') :
			verdict,feed=f.xcz_hasher(buffer,headerlist,verdict,feed)
		else:
			verdict,feed=f.verify_hash_nca(buffer,headerlist,verdict,feed)
		f.flush()
		f.close()



		Status.close()
  
		return verdict
	except KeyboardInterrupt:
		Config.isRunning = False
		Status.close()
	except BaseException as e:
		Config.isRunning = False
		Status.close()
		raise e
		





