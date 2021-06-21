import os

#path = '/ddn/home8/r2891/chem/quad/anion/naph/cncch/apVDZ/1'

def greper(path):
    cmd = 'grep ' + " '#N B3LYP/STO-3G OPT' " + path + '>>' + ' error/error.out'
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

def amount(filename):
    filename = filename.replace('.out','.com')
   # print(filename)
    with open(filename,'r') as file:
        data =file.readlines()
       
    return len(data[5:])-1

def xyzgrabber(name,amountofatoms ,Type,path):
    print(path)
    with open(path,'r') as file:
        data =file.readlines()
        #print(data)

        #print(ycoord)
        total2 = []
        standnum = []
        for num,line in enumerate(data):
            zcoord = data[num][33:]
            #print(zcoord)
            if 'Standard orientation' in line:
                standnum.append(num)
        atomnum = int(amountofatoms)
        xyzcoords = data[standnum[-1]+5:standnum[-1]+atomnum+5]        
        for i in xyzcoords:
            a = i.replace('  0  ',' ')
            atom = a[10:20]
            xcoord = a[30:45]
            ycoord = a[43:56]
            
            zcoord = 0.000
            total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
      #      print(total)
            total2.append(total)
      #  print(len(total2))
        
    path = path.replace('.out','.com')
    newfile = open(path, 'w+')
    newfile.write('#N B3LYP/aug-cc-pVDZ OPT SCF=YQC SCF=IntRep  Use=L506 Guess=Mix Guess=Sparse Guess=NoSymm\n')
    newfile.write('\n')
    newfile.write(str(name) + '\n')
    newfile.write('\n')
    if Type == 'Anion' or Type == 'anion':
        newfile.write('-1 1\n')    
    if Type == 'Radical' or Type == 'radical':
        newfile.write('0 2\n') 
    for i in total2:
        newfile.write(str(i)) 
        newfile.write('\n')  
    newfile.write('\n') 
    newfile.close()
    
    return 


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
    path_to_check_for_errors = '/Users/tsantaloci/Desktop/PAHcode/C2HC2H/apvdz/1Naph'
    greper(path_to_check_for_errors + '/' +'*' + '/' + '*' + '.out')
    readerror('error/error')
    for i in readerror('error/error'):
        path_with_errors = i
        amountofatoms = amount(path_with_errors)
        print(amountofatoms)
        if '1Naph' in i:
            name = '1Naph'
        if '2Naph' in i:
            name = '2Naph'
        print(xyzgrabber(name,amountofatoms ,'Anion',path_with_errors))
      #  runjobs(path_with_errors,path_with_errors)





#    runjobs(name,runjobs1)
    return
Main()
path_to_error = '/ddn/home6/r2532/chem/Diss/naph/src/error'
os.chdir(path_to_error)
os.remove('error.out')