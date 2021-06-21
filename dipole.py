import os



#types = 'C2HOH'
types = 'CNCN'
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
typeofnaph = '1Naph/'
path_to_apvdz_opt = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/1Naph'
path_dipole_bound_anion = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/aniondipole/1Naph'

def checkifreadyfornextstep(path):
        #os.system("grep 'Normal termination '"  + str(path) + '*/*.out')
        os.chdir(path)
        os.system("grep -rl 'Normal termination' */*.out | xargs sed -i 's/Normal termination/Move to dipole moment step/g'")
        return


def pbsfilecreator(cluster,path,smiles):
    '''
    creates pbs scripts
    '''
    
        
    outName = str(types) +  typeofnaph  + str(smiles)
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

def amount(path,smiles):
    with open(path + '/' + str(smiles) +'/' + str(smiles) + '.com','r') as file:
        data =file.readlines()


    return len(data[5:])-1

def xyzgrabber(amountofatoms,smiles,xyzcoords,path):
    data = xyzcoords
    #print(data)
    total2 = []
    standnum = []     
    for i in data:
        a = i.replace('  0  ',' ')
        atom = a[10:20]
        xcoord = a[30:45]
        ycoord = a[43:56]
        
        zcoord = 0.000
        total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
        total2.append(total)
        
    
    newfile = open(path + '/' +str(smiles) +'/' + str(smiles)  + '.com', 'w+')
    newfile.write('#N B3LYP/aug-cc-pVDZ SP SCF(conver=6) \n')
    newfile.write('\n')
    newfile.write(str(typeofnaph) + types + '\n')
    newfile.write('\n')
    newfile.write('-1 1\n')    
    for i in total2:
        newfile.write(str(i)) 
        newfile.write('\n')  
    newfile.write('\n') 
    newfile.close()
    
    return 



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
            print(data[i])
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
    checkifreadyfornextstep(path_to_apvdz_opt)

    
    os.chdir(path_to_apvdz_opt)
    leftoverdirect = []
    for smiles in os.listdir():
        filename = open(str(smiles) + '/' + str(smiles) + '.out')
        data = filename.readlines()
        for i in data:
            if 'Move to dipole moment step' in i:
                leftoverdirect.append(smiles)
    os.chdir(path_dipole_bound_anion)
    for smiles in leftoverdirect:
        
     #   atomnum = amount(path_to_apvdz_opt,smiles)
        os.mkdir(smiles)
        print(smiles)
     #   pbsfilecreator('seq',path_dipole_bound_anion,smiles)
     #   coords = gatheroptxyzcoords(path_to_apvdz_opt,smiles)
     #   xyzgrabber(atomnum,smiles,coords,path_dipole_bound_anion)
        #print(coords)
        '''
        when us are ready to submit jobs uncommit runjobs 
      #  runjobs(path_dipole_bound_anion,smiles)
        '''



    return
Main()

