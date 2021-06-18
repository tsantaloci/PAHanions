import os

# dipole moment for dummy atom
# insert dummy atom into the xyz coords
# generate input file
# generate pbs file
# runscript



path_to_exc_calcs = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/apvDZ+8s6p2d/1Naph'

def dipolemomentgrabber(filename,num):
    dipolecoords = []
    with open(filename +'/' + str(num) + '/' + str(num) + '.out','r') as file:
        data =file.readlines()
        for num,i in enumerate(data):
            if 'Dipole moment' in i:
               # print(data[num+1])
                xdipole = float(data[num+1][6:28])
                ydipole = float(data[num+1][32:56])
                zdipole = float(data[num+1][58:80])
                totdipole = float(data[num+1][85:105])
                dipolecoords.append('He     ' + str(xdipole) + '            ' + str(ydipole) + '      ' + str(zdipole) + '\n')
                #print(tot)


    return dipolecoords
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

def inputcreator(dipole,xyz,filename,num):
    #print(filename)
    filename = open(filename + '/' + str(num) + '/' + str(num) + '.com','w+')
    filename.write('***, PES for several lowest states of hydrogen fluoride\n')
    filename.write('memory,1200,m\n')
    filename.write('basis={default=avdz\n')
    filename.write('s,He,0.0252600,0.0062100,0.0015267,0.0003753,0.0000901,0.0000216,0.0000052,0.0000012;\n')
    filename.write('p,He,0.1020000,0.0268000,0.0070416,0.0018502,0.0004861,0.0001277;\n')
    filename.write('d,He,0.2470000,0.0577000;\n}')
    filename.write('gthresh,compress=1.d-9\n')
    filename.write('geomtyp=xyz                      \n')
    filename.write('\geometry={\n')
    for i in dipole:
        #print(i)

        filename.write(str(i))
    for i in xyz:
       
       # print(i)
        filename.write(str(i))
    filename.write('}\n')
    filename.write('\n')
    filename.write('dummy,He\n')
    filename.write('hf,orbprint,75,maxit=100;wf,charge=-1,spin=0;accu,20\n')
    filename.write('orbital,ignore_error;\n')
    filename.write('{ccsd,NOCHECK\n')
    filename.write('orbital,IGNORE_ERROR\n')
    filename.write('dm,5600.2 \n')
    filename.write('expec,qm \n')
    filename.write('eom,2.1,1.2,trans=1} \n')
    filename.write('\n')
    

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



def Main():
    path_to_exc_calcs = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/apvDZ+8s6p2d/1Naph'
    path_to_anion_dipole_moments = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/aniondipole/1Naph'
    os.chdir(path_to_anion_dipole_moments)
    leftoverdirect = []
    for smiles in os.listdir():
        #print(smiles)
        leftoverdirect.append(smiles)
    os.chdir(path_to_exc_calcs)
    name = path_to_exc_calcs.split('/')
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
        #os.mkdir(str(i))
        pbsfilecreator('seq',path_to_exc_calcs,str(i))
        xyzcoords = grabxyz(path_to_anion_dipole_moments,str(i) )
        letxyzcoords = atom_num_to_letter(xyzcoords)
        dipole = dipolemomentgrabber(path_to_anion_dipole_moments,str(i))
        inputcreator(dipole,letxyzcoords,path_to_exc_calcs,str(i))



    return
Main()


