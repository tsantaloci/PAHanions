import os

path = '/Users/tsantaloci/Desktop/PAHcode/test/CNCNt/apvdz/2Naph'

def aaa(path):
	os.chdir(path)
#	os.system('grep ' + 'Normal termination' + ' */*.out')
	os.system("grep -rl 'Normal termination' */*.out | xargs sed -i 's/Normal termination/Has been brought to next step/g'")
	return
aaa(path)	



#def checkifreadyfornextstep(path):
#	os.chdir(path)
#	os.system("grep 'Normal termination ' + '*/*.out')
#	os.system("grep -rl 'Normal termination' path.out | xargs sed -i 's/Normal termination/Has been brought to next step/g'")	
#	return
#checkifreadyfornextstep(path)
