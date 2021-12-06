import os
import pandas as pd 


def radicalener(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    totener2 = []
    for x in data:
        if 'Normal termination' in x or 'Move to dipole moment step' in x:
            iterenergy = []
            for num2 in data:
                #print(num)
                if 'SCF Done' in num2:
                    #print(num)
                    iterenergy.append(num2)

            totener2.append(float(iterenergy[-1][24:41])*627.509)
   # print(totener2)



    return totener2

def anionener(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    totener = []
    for x in data:
        if 'Normal termination' in x or 'Move to dipole moment step' in x:
            iterenergy = []
            for num2 in data:
                #print(num)
                if 'SCF Done' in num2:
                    #print(num)
                    iterenergy.append(num2)

            totener.append(float(iterenergy[-1][24:41])*627.509)

    return totener

def eBEgatherer(num,path):
    filename = open(path +'/' + str(num) + '/' + 'output.dat')
    data = filename.readlines()
    value = []
    for i in data:
        if 'Converged eigenvalue' in i:
            i = i.replace('Converged eigenvalue:','')
            i = i.replace('a.u.','')
           # print((num,i))
            value.append(float(i))

          #  print(i)
  #  print(value)
    value = sorted(value,reverse=False)

    
   # print(value)
    #print(value[0])

    return value[0] * 27.2114

def exciteDBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    state21 = []
    for x in data:
     #   state = []
        if '2.1' in x and 'spectrum data (repeated)' in x:
            #print(x)
            state21.append(x[13:25])
        

    return float(state21[0])



def orbitalsDBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    data_2 = filename.readlines()
    start = []
    #end = []
    for num,x in enumerate(data):
        if 'Results for state  2.1:' in x :
            #print(num)
            start.append(num+3)
     #   if 'Contribution of reference' in x:
     #
     #        end.append(num)
    print((start[-1],'Line number of where the loop begins 1st_DBS'))
   # print(data[start[-1]])
    orbitals = []
    for num in range(30):
        if data[start[-1]+num]=='\n':
            break
        else: 
            orbitals.append(data[start[-1]+num])
    #print(orbitals)
    coefficients = []
    excitations = []
    for i in orbitals:
        if abs(float(i[0:15])) > 0.3: 
            coefficients.append(float(i[0:15]))
            excitations.append(i[15:].replace('\n','').replace(' ',''))
        #print(i)
    #d = {'Coefficients': coefficients,'Excitation': excitations}
    #df = pd.DataFrame(data=d)
    #print(df)


    return coefficients,excitations

def excite2ndDBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    state31 = []
    for x in data:
     #   state = []
        if '3.1' in x and 'spectrum data (repeated)' in x:
            #print(x)
            state31.append(x[13:25])
        

    return float(state31[0])

def orbitals2ndDBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    data_2 = filename.readlines()
    start = []
    #end = []
    for num,x in enumerate(data):
        if 'Results for state  3.1:' in x :
            #print(num)
            start.append(num+3)
     #   if 'Contribution of reference' in x:
     #
     #        end.append(num)
    print((start[-1],'Line number of where the loop begins 2nd_DBS'))
   # print(data[start[-1]])
    orbitals = []
    for num in range(30):
        if data[start[-1]+num]=='\n':
            break
        else: 
            orbitals.append(data[start[-1]+num])
    #print(orbitals)
    coefficients = []
    excitations = []
    for i in orbitals:
        if abs(float(i[0:15])) > 0.3: 
            coefficients.append(float(i[0:15]))
            excitations.append(i[15:].replace('\n','').replace(' ',''))
        #print(i)
    d = {'Coefficients': coefficients,'Excitation': excitations}
    df = pd.DataFrame(data=d)
    print(df)



    return  coefficients,excitations 



def exciteVBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    state12 = []
    for x in data:
     #   state = []
        if '1.2' in x and 'spectrum data (repeated)' in x:
            #print(x)
            state12.append(x[13:25])
        

    return float(state12[0])

def orbitalsVBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    data_2 = filename.readlines()
    start = []
    #end = []
    for num,x in enumerate(data):
        if 'Results for state  1.2:' in x :
            #print(num)
            start.append(num+3)
     #   if 'Contribution of reference' in x:
     #
     #        end.append(num)
    print((start[-1],'Line number of where the loop begins_VBS'))
   # print(data[start[-1]])
    orbitals = []
    for num in range(30):
        if data[start[-1]+num]=='\n':
            break
        else: 
            orbitals.append(data[start[-1]+num])
    #print(orbitals)
    coefficients = []
    excitations = []
    for i in orbitals:
        if abs(float(i[0:15])) > 0.3: 
            coefficients.append(float(i[0:15]))
            excitations.append(i[15:].replace('\n','').replace(' ',''))
        #print(i)
   # d = {'Coefficients': coefficients,'Excitation': excitations}
   # df = pd.DataFrame(data=d)
   # print(df)


    return coefficients,excitations

def excite2ndVBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    state22 = []
    for x in data:
     #   state = []
        if '2.2' in x and 'spectrum data (repeated)' in x:
            #print(x)
            state22.append(x[13:25])
        

    return float(state22[0])


def orbitals2ndVBS(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')

    data = filename.readlines()
    data_2 = filename.readlines()
    start = []
    #end = []
    for num,x in enumerate(data):
        if 'Results for state  2.2:' in x :
            #print(num)
            start.append(num+3)
     #   if 'Contribution of reference' in x:
     #
     #        end.append(num)
    print((start[-1],'Line number of where the loop begins_VBS'))
   # print(data[start[-1]])
    orbitals = []
    for num in range(30):
        if data[start[-1]+num]=='\n':
            break
        else: 
            orbitals.append(data[start[-1]+num])
    #print(orbitals)
    coefficients = []
    excitations = []
    for i in orbitals:
        if abs(float(i[0:15])) > 0.3: 
            coefficients.append(float(i[0:15]))
            excitations.append(i[15:].replace('\n','').replace(' ',''))
        #print(i)
   # d = {'Coefficients': coefficients,'Excitation': excitations}
   # df = pd.DataFrame(data=d)
   # print(df)


    return coefficients,excitations

def dipoletable(num,path):
    filename = open(path + '/' + str(num) + '/' + str(num) + '.out','r')
    data = filename.readlines()
    for num,i in enumerate(data):
        if 'Dipole' in i:
            for x in data[num+1:num+3]:
                if 'X=' in x:
                    xx = float(x[10:26])
                    yy = float(x[37:55])
                    zz = float(x[60:80])
                    tt = float(x[85:105])

                
                 #   print(x[60:])

  #  filename2 = open(path2 + '/' +'Dipinfo.tex','a+')
  #  filename2.write(str(numb) + ' & '+ str(xx) + " & " + str(yy) + ' & ' + str(zz) + ' & ' + str(tt)  + " \\\\ " + '\n' )
   # print(tt)


    return tt

def quadtable(name,path,path2,numb):
    filename = open(path,'r')
    data = filename.readlines()
    for num,i in enumerate(data):
        if 'Traceless' in i:
            for x in data[num+1:num+3]:
                if 'XX=' in x:
                    xx = float(x[10:26])
                    yy = float(x[37:55])
                    zz = float(x[60:])
                
                 #   print(x[60:])
                if 'XY=' in x:
                    xy = float(x[10:26])
                    xz = float(x[37:55])
                    yz = float(x[60:])
    filename2 = open(path2 + '/' +'quadinfo.tex','a+')
    filename2.write(str(numb) + ' & '+ str(xx) + " & " + str(yy) + ' & ' + str(zz) + ' & ' + str(xy) + ' & '+ str(xz) + ' & ' + str(yz) + " \\\\ " + '\n' )

    


 
   # os.remove('quad.out')
    

    return 




def main():

    path_to_src = '/Users/tsantaloci/Desktop/PAHcode/src'
    path_to_quad = '/Users/tsantaloci/Desktop/PAHcode/CNCN/EOM/aniondipole/2Naph'
    path_to_dipole = '/Users/tsantaloci/Desktop/PAHcode/CNCN/EOM/aniondipole/2Naph'
    path_to_dipole = path_to_quad
    path_to_anion_ener = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/2Naph'
    path_to_radical_ener = '/Users/tsantaloci/Desktop/PAHcode/CNCN/radicals/apVDZ/2Naph'
    path_to_eBE = '/Users/tsantaloci/Desktop/PAHcode/CNCN/EOM/eBE/2Naph'
    path_to_exc = '/Users/tsantaloci/Desktop/PAHcode/CNCN/EOM/apvdz+8s6p2d/2Naph'
    name = 'CNCNNaph'
    #radicalener(path_to_radical_ener)

   # os.chdir(path_to_radical_ener)

   ### CNCN  ### #### 24 is not done and 32 has a bug but is done ####
   ### 1Naph CNCN w/o 24 and 32###
  #  isomer = ['0','1','2','3','4','25','26','27','28','29','30','31','33','34','35','36','38','40']
   # isomer = ['8','26']
   # isomer = ['26']
   # isomer = ['8']
   ### 2Naph CNCN 7 did not print orbitals excitations###
    isomer =   ['8','9','25','26','27','32','34','35']
   # isomer = ['25']



    a = []
    r = []
    dipole = []
    eBE = []
    DBS = []
    DBSorbs_c = []
    DBSorbs_e = []
    DBS2ndorbs_c = []
    DBS2ndorbs_e = []
    DBS2nd = []
    VBS = []
    VBSorbs_c = []
    VBSorbs_e = []
    VBS2nd = []
    VBS2ndorbs_c = []
    VBS2ndorbs_e = []
   # for i in os.listdir():
    for i in isomer:
        print(i,'Isomer number')
        
        os.chdir(path_to_radical_ener)
        r.append(str(radicalener(i,path_to_radical_ener)).replace('[','').replace(']','').replace("'",''))
        os.chdir(path_to_anion_ener)
        a.append(str(anionener(i,path_to_anion_ener)).replace('[','').replace(']','').replace("'",''))
        dipole.append(dipoletable(i,path_to_dipole))
        eBE.append(eBEgatherer(i,path_to_eBE))
        DBS.append(exciteDBS(i,path_to_exc))
        c = orbitalsDBS(i,path_to_exc)
        
        DBSorbs_c.append(c[0])
        DBSorbs_e.append(c[1])
        
        DBS2nd.append(excite2ndDBS(i,path_to_exc))
        c_2 = orbitals2ndDBS(i,path_to_exc)
        DBS2ndorbs_c.append(c_2[0])
        DBS2ndorbs_e.append(c_2[1])
        
        VBS.append(exciteVBS(i,path_to_exc))
        c_3 = orbitalsVBS(i,path_to_exc)
        VBSorbs_c.append(c_3[0])
        VBSorbs_e.append(c_3[1])
        
        VBS2nd.append(excite2ndVBS(i,path_to_exc))
        c_4 = orbitals2ndVBS(i,path_to_exc)
        VBS2ndorbs_c.append(c_4[0])
        VBS2ndorbs_e.append(c_4[1])
        
    a2 = []
    r2 = []
    for i in a:
        i = float(i)
        a2.append(i)   
    for i in r:
        i = float(i)
        r2.append(i)
    
###### Relative Energies and Dipole moment Table #####

    Isomer = '1-Dicyanonaph.'
    d = {'filename': isomer, 'Anion': a2,'Radical': r2}
    df = pd.DataFrame(data=d)
    d2 = {Isomer:isomer,'Anion':df['Anion']-df['Anion'].min(),'Radical':df['Radical']-df['Radical'].min(),'Dipole':dipole}
    df2 = pd.DataFrame(data=d2)
    os.chdir(path_to_src)
    df2.to_csv('relenerg.csv',index=False) 
   # print(df2.to_latex(index=False))
####### Excitation energies with eBE #########
    e = {Isomer: isomer,"VBS":VBS, "2nd VBS": VBS2nd , "DBS":DBS,"coefficients":DBSorbs_c,"Excitation":DBSorbs_e, "2nd DBS":DBS2nd, 'eBE': eBE} 

    ef = pd.DataFrame(data=e) 
    os.chdir(path_to_src)
    ef.to_csv('excitation.csv',index=False)

####### Orbitals and what the excitations are going #######
    DBSorbs_1 = {Isomer: isomer, "DBS":DBS,"coefficients":DBSorbs_c,"Excitation":DBSorbs_e, 'eBE': eBE,'Dipole':dipole}
    DBSorbs_2 = {Isomer: isomer, "2nd_DBS":DBS2nd,"coefficients":DBS2ndorbs_c,"Excitation":DBS2ndorbs_e, 'eBE': eBE,'Dipole':dipole}
    VBSorbs_1 = {Isomer: isomer, "VBS":VBS,"coefficients":VBSorbs_c,"Excitation":VBSorbs_e, 'eBE': eBE,'Dipole':dipole}
    VBSorbs_2 = {Isomer: isomer, "2nd_VBS":VBS2nd,"coefficients":VBS2ndorbs_c,"Excitation":VBS2ndorbs_e, 'eBE': eBE,'Dipole':dipole}


    DBSorb_1 = pd.DataFrame(data=DBSorbs_1)
    os.chdir(path_to_src)
    DBSorb_1.to_csv('DBS_1.csv',index=False) 

    DBSorb_2 = pd.DataFrame(data=DBSorbs_2)
    os.chdir(path_to_src)
    DBSorb_2.to_csv('DBS_2.csv',index=False) 

    VBSorb_1 = pd.DataFrame(data=VBSorbs_1)
    os.chdir(path_to_src)
    VBSorb_1.to_csv('VBS_1.csv',index=False)

    VBSorb_2 = pd.DataFrame(data=VBSorbs_2)
    os.chdir(path_to_src)
    VBSorb_2.to_csv('VBS_2.csv',index=False) 

    total = {Isomer:isomer,'Anion':df['Anion']-df['Anion'].min(),'Radical':df['Radical']-df['Radical'].min(),'Dipole':dipole,"VBS":VBS,"VBScoefficients":VBSorbs_c,"VBSExcitation":VBSorbs_e,"2nd_VBS":VBS2nd,"VBS_2coefficients":VBS2ndorbs_c,"VBS_2Excitation":VBS2ndorbs_e,"DBS":DBS,"DBScoefficients":DBSorbs_c,"DBSExcitation":DBSorbs_e,"2nd_DBS":DBS2nd,"DBS_2coefficients":DBS2ndorbs_c,"DBS_2Excitation":DBS2ndorbs_e, 'eBE': eBE}

    total = pd.DataFrame(data=total)
    os.chdir(path_to_src)
    total.to_csv('total.csv',index=False)
    
   # print(ef)
   # print(ef.to_latex(index=False))
    #df2.to_csv('optener.csv',index=False) 
    #ef.to_csv('exc.csv',index=False)

      #  c.append[i[0]]
     #   e.append[i[1]]
    #print(c)
    #print(e)
    
    
    
  





    '''
    os.chdir(path_to_eBE)
    numlist = []
    for i in os.listdir():
        eBEgatherer(i,path_to_eBE)
        numlist.append(i)
      #  excitetable(i,path_to_eBE,eBEgatherer(i,path_to_eBE),numlist,path_to_src)



    os.chdir(path_to_quad)
    

    
    # When quadtables == yes will make the quadrapole moments tables
    
    quadtables = 'yes'
    quadtables = ''
    # makes the dipoletables == yes will make dipole moment tables 
    dipoletables = 'yes'
    dipoletables = ''

    directory = []
    if quadtables == 'yes' and dipoletables == 'yes':
        print('Only one of them needs to not be commented')
        

    if quadtables == 'yes' and dipoletables == '':
        filename2 = open(path_to_src + '/' +'quadinfo.tex','w')
        filename2.write("\\begin{table}")
        filename2.write('\n')
        filename2.write("\\tiny")
        filename2.write('\n')
        filename2.write("\centering")
        filename2.write('\n')
        filename2.write("   \\begin{tabular}{ccccccc}")
        filename2.write('\n')
        filename2.write("    \hline")
        filename2.write('\n')
        # filename2.write("  B   & \multicolumn{2}{c}{Oscillator Strengths}  \\" + "\\")
        filename2.write(name +' & '+ "XX" + " & " + 'YY' + ' & ' + 'ZZ' + ' & ' + 'XY ' + '& '+ ' XZ' + ' & ' + 'YZ' + " \\\\")
        filename2.write('\n')
        filename2.write("\hline")
        filename2.write('\n')
        filename2.close()
        for i in os.listdir():
            i = int(i)
            directory.append(i)
        
        for i in sorted(directory):
            i = str(i)
            print(i)
            quadtable(name,path_to_quad + '/' + i +'/' + i + '.out',path_to_src,str(i))
        filename2.close()
        filename2 = open(path_to_src + '/' +'quadinfo.tex','a')
        filename2.write('\hline \n')
        filename2.write('\n')
        filename2.write('  \end{tabular}\n')
        filename2.write('\end{table}\n')
    if dipoletables == 'yes' and quadtables == '':
        filename2 = open(path_to_src + '/' +'dipinfo.tex','w')
        filename2.write("\\begin{table}")
        filename2.write('\n')
        filename2.write("\\tiny")
        filename2.write('\n')
        filename2.write("\centering")
        filename2.write('\n')
        filename2.write("   \\begin{tabular}{ccccccc}")
        filename2.write('\n')
        filename2.write("    \hline")
        filename2.write('\n')
        # filename2.write("  B   & \multicolumn{2}{c}{Oscillator Strengths}  \\" + "\\")
        filename2.write(name +' & '+ "X" + " & " + 'Y' + ' & ' + 'Z' + ' & ' + 'Tot ' +  " \\\\")
        filename2.write('\n')
        filename2.write("\hline")
        filename2.write('\n')
        filename2.close()
        for i in os.listdir():
            i = int(i)
            directory.append(i)
        
        for i in sorted(directory):
            i = str(i)
            print(i)
            dipoletable(name,path_to_quad + '/' + i +'/' + i + '.out',path_to_src,str(i))
        filename2.close()
        filename2 = open(path_to_src + '/' +'dipinfo.tex','a')
        filename2.write('\hline \n')
        filename2.write('\n')
        filename2.write('  \end{tabular}\n')
        filename2.write('\end{table}\n')
    '''
    


    return
main()
