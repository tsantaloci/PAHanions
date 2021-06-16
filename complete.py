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
 
        ### To find the difference in symmetry do a minimal basis set guess and compare the energies..... ###
        
 #Benzene: c1ccccc1
 #Naphathalene: c1cccc2c1cccc2
 # Anthracene: c1cccc2c1cc3c(c2)cccc3   
        

#filename = open('benz.smi','r')
#onefunctional = input('what is one of the functional groups (insert # for triple & no hydrogens): ')

nonfunctionalizedsmi = 'c1cccc2c1cccc2'
types = 'C2HOH'
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
basis = 'apvdz'


#nonfunctionalizedsmi = 'c1ccccc1'
#nonfunctionalizedsmi = 'c1cccc2c1cc3c(c2)cccc3'


onefunctional = 'C#C'
otherfunctional = 'C#C'
#position = 'ortho'
#position = '1'
#path = '1Naph'

typeofnaph = '1Naph/'
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
    if amountofrings == 'c1cccc2c1cccc2' and position == '1':
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
    if amountofrings == 'c1cccc2c1cccc2' and position == '2':
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



aa = difunctionalNaph(nonfunctionalizedsmi,onefunctional,otherfunctional,position)


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
    final = naphdeproton(aa)
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
        #    os.chdir('../../')
        print(smiles[i])
   # elif position == '2':
   #     for i in range(len(smiles)):
   #         os.mkdir('2Naph/'+str(i)) 
   #       #  os.chdir('1Naph/'+ str(i))
   #         filename = open('2Naph/' + str(i) + '/' + str(i)+'.smi','w+')
   #         filename.write(str(smiles[i]))
   #         filename.close()
   #         cmd = 'obabel -ismi' + ' 2Naph/' + str(i) +'/' + str(i) + '.smi ' + ' -oxyz  -O ' + '2Naph/'+str(i) + '/' + str(i) + '.com '+ ' --gen3D' 
            
   #         print(cmd)
   #         os.system(cmd)
        #    os.chdir('../../')
   #         print(smiles[i])


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

   # if position =='2':
   #     for i in range(len(smiles)):
   #         with open('2Naph/' + str(i) + '/' + str(i)+ '.com','r') as file:
   #         #    filename = open('1Naph/' + str(1) + '/' + str(1)+'.smi','w+')
   #             data = file.readlines()
   #             data[0] = '#N B3LYP/STO-3G OPT \n'
   #             data.insert(2,'2Naph\n')
   #             data.insert(3,'\n')
   #             if Type == 'anion' or Type == 'Anion':
                ## If Anion -1 1 and if Radical 0 2
   #                 data.insert(4,'-1 1 \n')
                    #print(data)
   #             elif Type == 'radical' or Type == 'Radical':
   #                 data.insert(4,'0 2 \n')
   #                 file.close()

    #                
    #            else:
    #                print('give a type')

    
    #        filename = open('2Naph/' + str(i) + '/' + str(i)+'.com','w+')
    #        for i in data:
    #            filename.write(str(i))
    #        filename.write('\n')
    #        filename.close()        

           

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




def energydict(path,smiles):
    '''
    gather all the energies from the output files

    '''
    #totenergydict = {}
    totenergylist = []
    filnumber = []
    for i in range(len(smiles)):
        try:
            with open(path + '/' + str(i) + '/' + str(i)+ '.out','r') as file:
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
        except FileNotFoundError:
            pass

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
                print(data[i])
            file = open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','w+')
            for i in data:
                print(i)

                file.write(i)
            file.close()
        


    return





def Main():
    #To generate the smiles strings and place in minimum basis set guess uncomment
    
    aa = difunctionalNaph(nonfunctionalizedsmi,onefunctional,otherfunctional,position)
    print(naphdeproton(aa))
    print(len(smileweeder()))
    smiles = smileweeder()
    xyzcoordsfilegen(smiles)
    mininputfilecreator('Anion',smiles)     
    pbsfilecreator('seq',path,smiles)
    
    '''
     to edit out the same and add the xyz coords for apvdz
    
    '''
    '''
    smiles = smileweeder()
    
    #pbsfilecreator('map',path,smiles)
    filelist, totalenergylist = energydict(path,smiles)
   # print(len(smiles))
    leftoverdirect = pandadataframe(path,filelist, totalenergylist)
    print(leftoverdirect)
    for smiles in leftoverdirect:
        #print(x)
        coords = gatheroptxyzcoords(path,smiles)
      #  print(coords)
   # print(len(smiles))
        optmizedinputfile('anion',path,coords,smiles)
    '''



    return
Main()