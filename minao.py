import numpy as np
import os
import itertools
import glob
import subprocess
import time
import sys
#import system
import subprocess
import shutil

nonfunctionalizedsmi = 'c1cccc2c1cccc2'
types = 'CNOH'
if types == 'C2HC2H':
    onefunctional = 'C#C'
    otherfunctional = 'C#C'


#types = 'CNCN'
if types == 'CNCN':
    onefunctional = 'C#N'
    otherfunctional = 'C#N'



#types = 'CNC2H'
if types == 'CNC2H':
    onefunctional = 'C#N'
    otherfunctional = 'C#C'

if types == 'CNOH':
    onefunctional = 'C#N'
    otherfunctional = 'O'

if types == 'C2HOH':
    onefunctional = 'C#C'
    otherfunctional = 'O'



basis = 'minao'


#nonfunctionalizedsmi = 'c1ccccc1'
#nonfunctionalizedsmi = 'c1cccc2c1cc3c(c2)cccc3'


onefunctional = 'C#C'
otherfunctional = 'C#C'
#position = 'ortho'

#path = '1Naph'

typeofnaph = '2Naph/'
path = '../' + str(types) + '/' + str(basis) + '/' + typeofnaph 
#otherfunctional = input('what is the other functional group')




def functionalgroupadderbenz(amountofrings,x,y,position):
    if amountofrings == 'c1ccccc1' and position == 'ortho':
        difunct = onefunctional[::-1] +'(2)' + '.' + 'c(2)1ccccc(3)1' + '.' + otherfunctional[::-1] + '(3)'   
   
    elif amountofrings == 'c1ccccc1' and position == 'meta':
        difunct = onefunctional[::-1] +'(2)' + '.' + 'c1c(2)cccc(3)1' + '.' + otherfunctional[::-1] + '(3)'  
 
    elif  amountofrings == 'c1ccccc1' and position == 'para':
        difunct = onefunctional[::-1] +'(2)' + '.' + 'c1cc(2)ccc(3)1' + '.' + otherfunctional[::-1] + '(3)' 
    else:
        print('change the position argument to ortho') 

    return difunct

#print(functionalgroupadderbenz(nonfunctionalizedsmi,onefunctional,otherfunctional,position))


def difunctionalNaph(amountofrings,x,y,position):
    if amountofrings == 'c1cccc2c1cccc2' and typeofnaph == '1Naph/':
        placeOne = onefunctional[::-1] +'(3)' + '.' + 'c(3)1cccc2c1cccc2' + '.' + otherfunctional[::-1] + '(4)'
        placeOne = list(placeOne)
        difunct = []
        for num,i in enumerate(placeOne):
            if i == 'c':
                placeOne[num] = 'c(4)'
                final = ''
                for i in placeOne:
                        final += i
                placeOne[num] = 'c'
                combosmiles = []
                combosmiles.append(final)
                for i in combosmiles:
                    if ')(' in i or 'c(4)2c1' in i or 'c2c(4)1' in i :
                        combosmiles.remove(i)
                    else:
                        difunct.append(i)
    if amountofrings == 'c1cccc2c1cccc2' and typeofnaph == '2Naph/':
        placeOne = onefunctional[::-1] +'(3)' + '.' + 'c1c(3)ccc2c1cccc2' + '.' + otherfunctional[::-1] + '(4)'
        placeOne = list(placeOne)
        difunct = []
        for num,i in enumerate(placeOne):
            if i == 'c':
                placeOne[num] = 'c(4)'
                final = ''
                for i in placeOne:
                        final += i
                placeOne[num] = 'c'
                combosmiles = []
                combosmiles.append(final)
                for i in combosmiles:
                    if ')(' in i or 'c(4)2c1' in i or 'c2c(4)1' in i :
                        combosmiles.remove(i)
                    else:
                        difunct.append(i)
                
    return  difunct






def naphdeproton(aa):
    final1 = []
    for i in aa:
        difunct = list(i)
        for num,i in enumerate(difunct):
            if i == 'c':
                difunct[num] = '[c]'
                final = ''
                for i in difunct:
                    final += i
                final1.append(final)
                difunct[num] = 'c'
            if i =='C':
                difunct[num] = '[C]'
                final = ''
                for i in difunct:
                    final += i
                final1.append(final)
                difunct[num] = 'C'
            if i == 'O':
                difunct[num] = '[O]'
                final = ''
                for i in difunct:
                    final += i
                final1.append(final)
                difunct[num] = 'O'
    return final1

def singledeprotonator(difunct):

    difunct = list(difunct)
   # print(difunct)
    final1 = []
    for num,i in enumerate(difunct):
        if i == 'c':
            difunct[num] = '[c]'
            final = ''
            for i in difunct:
                final += i
            final1.append(final)
            difunct[num] = 'c'
        if i =='C':
            difunct[num] = '[C]'
            final = ''
            for i in difunct:
                final += i
            final1.append(final)

     
            difunct[num] = 'C'
        if i == 'O':
            difunct[num] = '[O]'
            final = ''
            for i in difunct:
                final += i
            final1.append(final)

      
            difunct[num] = 'O'
    return final1


def smileweeder():
    final = naphdeproton(difunctionalNaph(nonfunctionalizedsmi,onefunctional,otherfunctional,typeofnaph))
    #final = singledeprotonator(functionalgroupadderbenz(nonfunctionalizedsmi,onefunctional,otherfunctional,position))
    cleansmi = []
    for i in final:
        if  '2[c]1' not in i and '[c]2c1' not in i and '[C](' not in i and '[c](' not in i:
            cleansmi.append(i)
        

    return cleansmi

def xyzcoordsfilegen(smiles):
    '''
    converts SMILES strings from cleansmi list into xyz coords and places them in the correct directory and file

    '''
    #if position == '1':
    for i in range(len(smiles)):
        os.mkdir(path+str(i)) 
          #  os.chdir('1Naph/'+ str(i))
        filename = open(path + str(i) + '/' + str(i)+'.smi','w+')
        filename.write(str(smiles[i]))
        filename.close()
            #path = '../' + str(types) + '/' + str(basis) + '/' + typeofnaph 
        cmd = 'obabel -ismi ' + path + str(i) +'/' + str(i) + '.smi ' + ' -oxyz  -O ' + path + str(i) +'/' + str(i) + '.com ' + ' --gen3D' 
          #  cmd = 'obabel -ismi ' + path + str(i) +'/' + str(i) + '.smi ' + ' -oxyz  -O ' +  path + str(i) +'/' + str(i) + '.com '+ ' --gen3D' 
            
        print(cmd)
        os.system(cmd)

        print(smiles[i])



    return


def mininputfilecreator(Type,smiles):
    '''
    creates minimum basis set guess input file
    '''
   # if position == '1':
   #     print(path)
    for i in range(len(smiles)):
            
        with open(path + str(i) + '/' + str(i)+ '.com','r') as file:
            #    filename = open('1Naph/' + str(1) + '/' + str(1)+'.smi','w+')
            data = file.readlines()
            data[0] = '#N B3LYP/STO-3G OPT \n'
            data.insert(2,'1Naph\n')
            data.insert(3,'\n')
            if Type == 'anion' or Type == 'Anion':
                ## If Anion -1 1 and if Radical 0 2
                data.insert(4,'-1 1 \n')
                    #print(data)
            elif Type == 'radical' or Type == 'Radical':
                data.insert(4,'0 2 \n')
                file.close()        
            else:
                print('give a type')

        filename = open(path + str(i) + '/' + str(i)+'.com','w+')
        for i in data:
            filename.write(str(i))
        filename.write('\n')
        filename.close()           

    return
        


def pbsfilecreator(cluster,path,smiles):
    '''
    creates pbs scripts
    '''
    
    for i in range(len(smiles)):
        outName = str(types) +  typeofnaph  + str(i)
        mem_pbs_opt ='10'
        baseName = str(i)
        output_num = ''
        i = str(i)

        if cluster == 'seq':
            with open('%s/%s.pbs' % (path + '/' + i, i), 'w') as fp:
                fp.write("#!/bin/sh\n")
                fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
                fp.write("mem={0}gb\n".format(mem_pbs_opt))
                fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
                fp.write("export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n")
                fp.write("scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
                fp.write("printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n")
                fp.write("/usr/local/apps/bin/g09setup %s.com %s.out%s" % (baseName, baseName, output_num))
        elif cluster == 'map':
            with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
                fp.write("#!/bin/sh\n")
                fp.write("#PBS -N %s\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l" % outName)
                fp.write("mem={0}gb\n".format(mem_pbs_opt))
                # r410 node
                fp.write("#PBS -q r410\n")
                fp.write(
                    "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
                fp.write(
                    "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
                fp.write(
                    """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
                fp.write("then\n")
                fp.write(
                    "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
                fp.write(
                    """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
                fp.write(
                    "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
                fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
                fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
                fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
                fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 {0}.com {0}.out".format(baseName, baseName) +
                        str(output_num) + "\n\nrm -r $scrdir\n")

    return

def runjobs(name,number):
    a = number
    os.chdir(path)
    for i in range(a):
       print(i)
       os.chdir(str(i) + '/')
       os.system('qsub ' + str(i) + '.pbs')
       os.chdir('../')  
    return


def Main():
    
    aa = difunctionalNaph(nonfunctionalizedsmi,onefunctional,otherfunctional,typeofnaph)
    print(naphdeproton(aa))
    print(len(smileweeder()))
    smiles = smileweeder()
    xyzcoordsfilegen(smiles)
    mininputfilecreator('Anion',smiles)     
    pbsfilecreator('seq',path,smiles)
    runjobs(path,len(smiles))

    return
Main()
