import os


def grabxyz(filename,num):
    #print(str(filename))
    with open(str(filename) + '/' + str(num) + '/' + str(num) + '.com') as file:
        data = file.readlines()
        optxyz = data[5:]
    return optxyz

def atom_num_to_letter(xyz):
    '''
    only works for atom numbers in single digits 

    '''
    #print(xyz[0])
    xyz2 = []
    for i in xyz:
        #i = i.strip('  ')
    #    i = str(i[6:9])
        
        
       
        a = i[6:9]
        #print(a)
        
        if a == ' 7 ':
            a = a.replace(a,'N') 
        if a == ' 6 ':
            a = a.replace(a,'C')
        if a == ' 8 ':
            a = a.replace(a,'O')
        if a == ' 1 ':
            a = a.replace(a,'H')
        #print(a)
        letxyz = a + i[10:]
        xyz2.append(letxyz)
        #print(letxyz)



           # print(i)
       # if i == 7:
       #     print(i)
    return xyz2


def inputfilecfour(filename,xyz):
    filename2 = open(str(filename),'w+')
    #print(path + str(filename) +  '.com')
    filename2.write('CNCN\n')
    #print(xyzcoords)
    for i in xyz:
        print(i)
        filename2.write(str(i))
    filename2.write('\n')
    filename2.write('*CFOUR(CHARGE=-1,REFERENCE=RHF,SPHERICAL=ON,BASIS=AUG-PVDZ\n')
    filename2.write('       LINDEP_TOL=10,LINEQ_CONV=10,SCF_CONV=7\n')
    filename2.write('       CALC=CCSD,EXCITE=EOMIP,ESTATE_SYM=1/1\n')
    filename2.write('       COORDS=CARTESIAN\n')
    filename2.write('       FROZEN_CORE=ON,ABCDTYPE=AOBASIS\n')
    filename2.write('       CONVERGENCE=7,MEMORY_SIZE=8,MEM_UNIT=GB)\n')
    filename2.write('\n')
    filename2.close()
    return

def pbsfile(name,filename):
    filename = open(str(filename) + '.pbs','w+')
  #  print(filename)
    
    filename.write('#!/bin/csh\n')
    filename.write('#\n')
    filename.write('#PBS -N ' + str(name) + '\n')
    filename.write('#PBS -S /bin/csh\n')
    filename.write('#PBS -j oe\n')
    filename.write('#PBS -W umask=022\n')
    filename.write('#PBS -l cput=2400:00:00\n')
    filename.write('#PBS -l mem=9gb\n')
    filename.write('#PBS -l nodes=1:ppn=2\n')
    filename.write('#PBS -q gpu\n')
    filename.write('\n')
    filename.write('cd $PBS_O_WORKDIR\n')
    filename.write('setenv NUM $NCPUS\n')
    filename.write('echo "$NUM cores requested in PBS file"\n')
    filename.write('echo " "\n')
    filename.write('source /ddn/home1/r1621/.tschrc\n')
    filename.write('/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 20 \n')
    filename.write('\n')
    


    return


def runjobs(name,number):
    a = number
    os.chdir(name)
    print(a)
    os.chdir(str(a) + '/')
    os.system('qsub ' + 'runc4' + '.pbs')
    os.chdir('../')  
    return     




def Main():
    path_to_eBE = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/eBE/1Naph'
    path_to_input_geom = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/aniondipole'
    os.chdir(path_to_input_geom)
    leftoverdirect = []
    for smiles in os.listdir():
        print(smiles)
        leftoverdirect.append(smiles)
    os.chdir(path_to_eBE)
    name = path_to_eBE.split('/')
    #print(name)
    for i in name:
        if 'CNCN' in i:
            name = name[-1] + 'CNCN'
        if 'CNC2H' in i:
            name = name[-1] +'CNC2H'
        if 'C2HC2H' in i:
            name = name[-1] +'C2HC2H'

            #print(name)
    for i in leftoverdirect:
        i
        ## If you need the directories added uncomment
        os.mkdir(str(i))
        xyzcoords = grabxyz( path_to_input_geom ,str(i) )
        letxyzcoords = atom_num_to_letter(xyzcoords)
        #print(letxyzcoords)
        #print(xyzcoords)
        inputfilecfour(path_to_eBE + '/' + str(i) + '/' + 'ZMAT' ,letxyzcoords)
        pbsfile(name+str(i),path_to_eBE + '/' + str(i) + '/' + 'runc4')
   #     runjobs(path_to_eBE,i)

       





    return
Main()

