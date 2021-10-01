import os
import pandas as pd



#types = 'C2HOH'
def energydict(path,path_to_src):
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
                if 'Move to dipole moment step' in x :
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

    os.chdir(path_to_src)
    return filnumber, totenergylist

def pandadataframe(filelist,energylist):
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
        remainderdir = []
        for i in range(1,len(uptdata)):
            differ = float(uptdata[i-1][2:])-float(uptdata[i][2:])
            print(differ)
            remainderdir.append(int(uptdata[i-1][0:2]))
            if abs(differ) <= .0005:
                num = int(uptdata[i-1][0:2])
                print(str(num) + 'SAME')
               # print(str(uptdata[i-1][0:2]))
              #  for x in os.listdir(path + '/' + str(num)):
                    #print(str(uptdata[i-1][0:2]))
             #       os.remove(path +'/'+ str(num)  + '/' + x)
                    
             #   os.rmdir(path + '/'+ str(num))
        
      #  for abc in os.listdir(path):
      #      remainderdir.append(abc)
        #print(data)
             
    return remainderdir



def checkifreadyfornextstep(path):
        #os.system("grep 'Normal termination '"  + str(path) + '*/*.out')
        os.chdir(path)
        os.system("grep -rl 'Normal termination' */*.out | xargs sed -i 's/Normal termination/Move to dipole moment step/g'")
        return


def pbsfilecreator(cluster,path,smiles):
    '''
    creates pbs scripts
    '''
    
        
    outName =  str(smiles)
    mem_pbs_opt ='10'
    baseName = str(smiles)
    output_num = ''
    i = str(smiles)

    if cluster == 'seq':
        with open('%s/%s.pbs' % (path + '/' + smiles, smiles), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write("export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n")
            fp.write("scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write("printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n")
            fp.write("/usr/local/apps/bin/g09setup %s.com %s.out%s" % (baseName, baseName, output_num))
    elif cluster == 'map':
        with open('%s/%s.pbs' % (path + '/' + smiles, smiles), 'w') as fp:
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



def xyzgrabber(name,path_1,path_2):
    print((path_1,'AAAAAAAAAA'))
    with open(path_1 + '/' + str(name) + '/' + str(name) + '.out','r') as file:
        data =file.readlines()
        #print(data)

        #print(ycoord)
        total2 = []
        startgeom = []
        endgeom = []
        for num,line in enumerate(data):
            zcoord = data[num][33:]
            #print(zcoord)
            if 'Standard orientation' in line:
                startgeom.append(num)
            if '---------------------------------------------------------------------' in line:
                endgeom.append(num)

        xyzcoords = data[startgeom[-1]+5:endgeom[-1]]
      #  for i in xyzcoords:
      #      print(i)
     #   atomnum = int(amountofatoms)
     #   print(atomnum)
        
        #xyzcoords = data[standnum[-1]+5:standnum[-1]+atomnum+5]        
        for i in xyzcoords:
           # print(i)
            a = i.replace('  0  ',' ')
            atom = a[10:20]
            xcoord = a[30:45]
            ycoord = a[43:56]
            zcoord = 0.0
            
        #    zcoord = 0.000
            total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)

            #print(total)
            total2.append(total)
    newfile = open(path_2 + '/' +str(name) +'/' + str(name)  + '.com', 'w+')
    newfile.write('#N B3LYP/aug-cc-pVDZ SP SCF(conver=6) \n')
    newfile.write('\n')
    newfile.write('aaaa'+  '\n')
    newfile.write('\n')
    newfile.write('-1 1\n') 
  #  print(total2)   
    for i in total2:
        print(i)
        newfile.write(str(i))
        newfile.write('\n')
 
    newfile.write('\n') 
    newfile.close()
        #    for i in total2:
        #        print(i)
    return total2


def amount(path,smiles):
    with open(path + '/' + str(smiles) +'/' + str(smiles) + '.com','r') as file:
        data =file.readlines()
        if '%mem' in data[0]:
             num = len(data[5:])-2
        else:
             num = len(data[5:])-1       
    return num


    





def optmizedinputfile(Type,path,coords,smiles):
        #print(x)
    filename = open(path +'/' + str(smiles) + '/' + str(smiles) + 'com','w+') 
    filename.write('#N B3LYP/aug-cc-pVDZ SP SCF(conver=6) \n')
    filename.write('\n')
    filename.write('2Naph\n')
    filename.write('\n')
    filename.write('-1 1 \n')


  
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
           # print(data[i])
        file = open(path  +'/' + str(smiles) + '/' + str(smiles)+ '.com','w+')
        for i in data:
            print(i)

            file.write(i)
        file.close()
    
    return

def runjobs(name,number):
    os.chdir(name)
    print(number)
    os.chdir(str(number) + '/')
    os.system('qsub ' + str(number) + '.pbs')
    os.chdir('../')  
    return    



def Main():
    types = 'C2HC2H'
    if types == 'C2HC2H':
        onefunctional = 'C#C'
        otherfunctional = 'C#C'
    if types == 'CNCN':
        onefunctional = 'C#N'
        otherfunctional = 'C#N'
    if types == 'CNC2H':
        onefunctional = 'C#N'
        otherfunctional = 'C#C'
    if types == 'CNOH':
        onefunctional = 'C#N'
        otherfunctional = 'O'
    if types == 'C2HOH':
        onefunctional = 'C#C'
        otherfunctional = 'O'
    basis = 'apvdz'
    typeofnaph = '2Naph/'
    path_to_apvdz_opt = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/1Naph'
    path_dipole_bound_anion = '/Users/tsantaloci/Desktop/PAHcode/CNCN/EOM/dipole/1Naph'
    path_to_src = '/Users/tsantaloci/Desktop/PAHcode/src'


    leftoverdirect = [1,2,3,4,5,6]






    

    for smiles in leftoverdirect:
        try:
            smiles = str(smiles)
            os.mkdir(path_dipole_bound_anion + '/' + str(smiles))
            print(smiles)       
            pbsfilecreator('map',path_dipole_bound_anion,smiles)
            xyzgrabber(smiles,path_to_apvdz_opt,path_dipole_bound_anion)
        except FileExistsError:
            print(smiles)       
            pbsfilecreator('map',path_dipole_bound_anion,smiles)
            xyzgrabber(smiles,path_to_apvdz_opt,path_dipole_bound_anion)

        
      #  when us are ready to submit jobs uncommit runjobs 
        
       # runjobs(path_dipole_bound_anion,smiles)

    

    return
Main()

