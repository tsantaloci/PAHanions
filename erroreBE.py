import os

#path = '/ddn/home8/r2891/chem/quad/anion/naph/cncch/apVDZ/1'

def greper(path):
   # cmd = 'grep ' + " 'Error' " + path + '>>' + ' error/error.out'
    cmd = 'grep ' + " 'Job has terminated with error flag' " +  path + ' >> ' + ' error/error.out'
    os.system(cmd)    
    return 

def readerror(filename):
    path_with_errors = []
    with open(filename + '.out','r') as file:
        data = file.readlines()
        for i in data:
            i = i.split(':')
            path_with_errors.append(i[0])
    return path_with_errors

def grabxyz(filename,num):
    #print(str(filename))
    with open(str(filename) + '/' + str(num) + '/' + str(num) + '.com') as file:
        data = file.readlines()
        optxyz = data[5:]
    return optxyz
  
def amount(filename):
    filename = filename.replace('output.dat','ZMAT')
    num = 0
    with open(filename,'r') as file:
        data =file.readlines()
        num = len(data[1:])-6
        
        print(num)
       # for i in data[1:]:
     #       print(i)
      #  print(data)
     #   if '%mem' in data[0]:
     #        num = len(data[5:])-2
     #   else:
    #         num = len(data[5:])-1   


def runjobs(name,name2):
    name = name.split('/')
    name.pop()
    newlist = ''
    for i in name:
       # i = i +'/'
        newlist += i +'/'
    print(newlist)

    os.chdir(newlist)
    name2=name2.replace('.out','.pbs')
    print(name2)
   
    
    
    os.system('qsub ' + name2)

    return
#runjobs(name,runjobs1)


def Main():
    '''
    before you run code make directory error in src
    '''
    path_to_check_for_errors = '/Users/tsantaloci/Desktop/PAHcode/eBE/1Naph'
    greper(path_to_check_for_errors + '/' +'*' + '/' + 'output.dat')
    readerror('error/error')
    for i in readerror('error/error'):
        print(i)
        path_with_errors = i
        amountofatoms = amount(path_with_errors)
  #      print(amountofatoms)
   #     if '1Naph' in i:
   #         name = '1Naph'
   #     if '2Naph' in i:
   #         name = '2Naph'
     #   print(xyzgrabber(name,amountofatoms ,'Anion',path_with_errors))
     #   runjobs(path_with_errors,path_with_errors)





#    runjobs(name,runjobs1)
    return
Main()
path_to_error = '/Users/tsantaloci/Desktop/PAHcode/src/error'
os.chdir(path_to_error)
os.remove('error.out')
