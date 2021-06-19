import numpy as np
import os
import itertools
import glob
import subprocess
import time
import sys
#import system
import subprocess
import pandas as pd
import shutil



def checkifreadyfornextstep(path):
	#os.system("grep 'Normal termination '"  + str(path) + '*/*.out')
        os.chdir(path)
#       os.system('grep ' + 'Normal termination' + ' */*.out')
        os.system("grep -rl 'Normal termination' */*.out | xargs sed -i 's/Normal termination/Has been brought to next step/g'")
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




def energydict(path):
    '''
    gather all the energies from the output files

    '''
    #totenergydict = {}
    totenergylist = []
    filnumber = []
    os.chdir(path)
    for i in os.listdir():
        print(i)

        with open(str(i) + '/' + str(i)+ '.out','r') as file:
            data = file.readlines()
                    #print(data)
                    
            for x in data:
                if 'Normal termination' in x :
                    iterenergy = []
                    for num in data:
                        if 'SCF Done' in num:
                                
                            iterenergy.append(num)
                                #  print((i,iterenergy[-1][23:23+21]))
                    #    print(i,iterenergy[-1][23:23+21])
                        # print(x)
                #print(len(iterenergy))
        #  print(iterenergy)
        
                    totenergylist.append(float(iterenergy[-1][23:23+21])*627.509) #kcal/mol
                    filnumber.append(i) 

    os.chdir('../../../../src/')
    return filnumber, totenergylist
#print(energydict(smileweeder()))

def pandadataframe(path,filelist,energylist):
    d = {'filename': filelist, 'energy (kcal/mol)': energylist}
    df = pd.DataFrame(data=d).sort_values('energy (kcal/mol)')
    df.to_csv('energy.csv',index=False)
    with open('energy'+ '.csv','r') as file:
        data = file.readlines()
        data.pop(0)
        uptdata = []
        for i in data:
            i = i.replace(',',' ')
            uptdata.append(i)
        #print(uptdata)
        for i in range(1,len(uptdata)):
            differ = float(uptdata[i-1][2:])-float(uptdata[i][2:])
            #print(differ)
            if abs(differ) <= .001:
                num = int(uptdata[i-1][0:2])
               # print(str(uptdata[i-1][0:2]))
                for x in os.listdir(path + '/' + str(num)):
                    print(str(uptdata[i-1][0:2]))
                    os.remove(path +'/'+ str(num)  + '/' + x)
                os.rmdir(path + '/'+ str(num))
        remainderdir = []
        for abc in os.listdir(path):
            remainderdir.append(abc)
        #print(data)
             
    return remainderdir

#filelist, totalenergylist = energydict(path,smileweeder())
#pandadataframe(path,filelist, totalenergylist)


def gatheroptxyzcoords(path,smiles):

    with open(path +'/' + str(smiles) + '/' + str(smiles) + '.out') as file:
        data = file.readlines()
        abc = []
        for num,i in enumerate(data):
            if  'Population analysis using the SCF density' in data[num]:
                abc.append(num)
        amountoflinesabovepop = 5
        # print(data[abc[-1]-6][5:7])
        lastatomnum = int(data[abc[-1]-6][5:7])
        
        minxyzguesscoords = data[abc[-1]-lastatomnum-amountoflinesabovepop:abc[-1]-amountoflinesabovepop]
        file.close()


    return minxyzguesscoords

def optmizedinputfile(Type,path,coords,smiles):
        #print(x)
    with open(path +'/' + str(smiles) + '/' + str(smiles) + '.out') as file:
        data = file.readlines()
        data[0] = '#N B3LYP/aug-cc-pVDZ OPT \n'
        data[1] = '\n'
        data.insert(2,'2Naph\n')
        data.insert(3,'\n')
        if Type == 'anion' or Type == 'Anion':
            ## If Anion -1 1 and if Radical 0 2
            data.insert(4,'-1 1 \n')
                #print(data)
        elif Type == 'radical' or Type == 'Radical':
            data.insert(4,'0 2 \n')
                    
        data[5:] = ''

    #    file.close()

        filename = open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','w+')
        for i in data:
           # print(i)
            i
            filename.write(str(i))
        file.close()
        filename = open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','a')
    
        
        for i in coords:
            i
            #print(i[16:])
            filename.write(i[16:])
        filename.write('\n')
        filename.close()
    #print(x)
        
        with open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','r') as file:
            data = file.readlines()
            for i in range(4,len(data)):
             #   print(i)
                data[i] = data[i].replace(data[i][10:20],'')
                #print(data[i])
            file = open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','w+')
            for i in data:
                print(i)

                file.write(i)
            file.close()
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
    nonfunctionalizedsmi = 'c1cccc2c1cccc2'
    types = ''
    basis = 'apvdz'
    onefunctional = ''
    otherfunctional = ''
    typeofnaph = ''
    #path = '../' + str(types) + '/' + str(basis) + '/' + typeofnaph 
    path_to_apvdz = '/Users/tsantaloci/Desktop/PAHcode/src/CNCNt/apvdz/1Naph'
    name = path_to_apvdz.split('/')
   # print(name)
    for i in name:
        i = i.upper()
    #    print(i)
        types = i
        if i == 'OHOH':
            onefunctional = 'O'
            otherfunctional = 'O'
        if i == 'C2HC2H':
            onefunctional = 'C#C'
            otherfunctional = 'C#C'
        if i == 'CNCN':
            onefunctional = 'C#N'
            otherfunctional = 'C#N'
        if i == 'CNC2H' or i == 'C2HCN':
            onefunctional = 'C#N'
            otherfunctional = 'C#C'
        if i == 'CNOH' or i == 'OHCN':
            onefunctional = 'C#N'
            otherfunctional = 'O'
        if i == 'C2HOH' or i == 'OHC2H':
            onefunctional = 'C#C'
            otherfunctional = 'O'
    for x in name:
        x = x.upper()
        if x == '1NAPH':
            typeofnaph = '1Naph/'
        if x == '2NAPH':
            typeofnaph = '2Naph/'


    #print(onefunctional)
    #print(otherfunctional)
    #print(types)
    #p

        #pbsfilecreator('map',path,smiles)
    filelist, totalenergylist = energydict(path_to_apvdz)
   # print(len(smiles))
    leftoverdirect = pandadataframe(path_to_apvdz,filelist, totalenergylist)
    #print(leftoverdirect)
    checkifreadyfornextstep(path_to_apvdz)
    for smiles in leftoverdirect:
        #print(x)
        coords = gatheroptxyzcoords(path_to_apvdz,smiles)
      #  print(coords)
   # print(len(smiles))
        optmizedinputfile('anion',path_to_apvdz,coords,smiles)

       # runjobs(path_to_apvdz,smiles)
    checkifreadyfornextstep(path_to_apvdz)



    return
Main()
