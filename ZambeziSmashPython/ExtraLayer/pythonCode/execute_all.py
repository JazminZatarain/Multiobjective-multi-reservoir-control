import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sn
import csv
import os
import sys
import subprocess

#### the above lines need to match the main_plots.py
title='5_res_wKGL'
build_dir = "../test/"
input_folder="../../../optimization/"+title+"/parallel/sets/"
output_folder="../for_plots/"
output_folder2="../decisions/"
output_folder3=build_dir+"storage_release/"


#copy the three lines below into the main_plots.py
#####################################
feature='500K'
#reservoirs=['itt','kgu','kgl','ka','bg','dg','cb','mn']
reservoirs=['itt','kgu','kgl','ka','cb']


#####################################
no_res=5

array_no_decisions=[196,230,264,298,332]
tot_decisions=array_no_decisions[no_res-4]
print(tot_decisions)
FILENAME='Zambezi_'+title

# print("start")
# subprocess.call(['bash', '../MOEAFramework/run_referenceset_overall.sh', str(tot_decisions), feature, FILENAME])
# print("end")

input_file=FILENAME+'.reference'#'.reference' #change filename
data= np.loadtxt(input_folder+feature+'/'+input_file, skiprows=0+1+2-1)
# print(np.shape(data))


if not os.path.exists(output_folder+feature+'/png'):
    os.makedirs(output_folder+feature+'/png')
   
if not os.path.exists(output_folder+feature+'/pdf'):
    os.makedirs(output_folder+feature+'/pdf')

if not os.path.exists(output_folder2+feature):
    os.makedirs(output_folder2+feature)
    
if not os.path.exists(output_folder3+feature):
    os.makedirs(output_folder3+feature)


os.putenv('RESERVOIRS', ' '.join(reservoirs))
hydro_index=np.argmin(data[:,tot_decisions])
env_index=np.argmin(data[:,tot_decisions+1])
irrd_index=np.argmin(data[:,tot_decisions+2])

hydro=np.argmin(data[:,tot_decisions])
app=np.argmin(data[:,tot_decisions+1])
irrd=np.argmin(data[:,tot_decisions+2])

names=['hydro', 'env', 'irr']
index=[hydro_index,env_index,irrd_index]
nobjs=len(names)
nsolns=3

a = []
for i in range(nobjs):
    row =data[index[i], tot_decisions:(tot_decisions+nsolns)]
    a.append(row)
    df = pd.DataFrame(a)

df.columns=['Hydropower','Environment','Irrigation']
df=pd.DataFrame(data[:,tot_decisions:(tot_decisions+nsolns)], columns=df.columns).append(df, ignore_index=True)
policies=['Best Hydropower','Best Environment','Best Irrigation']
df.insert(nsolns, "Name", "All Solutions") 

i=0
for i in range(len(policies)):
	df.loc[np.shape(data)[0]+i, 'Name'] = policies[i]
	i+=1

# # # #print real min and max values before normalizing
with open(output_folder+'/'+feature+'/'+'min_max.csv', mode='w') as min_max:
      min_max = csv.writer(min_max, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      min_max.writerow(df.columns)
      min_max.writerow(df.values[:,0:nobjs].max(axis=0))
      min_max.writerow(df.values[:,0:nobjs].min(axis=0))

# # # #Normalize Hydropower, Environment and Irrigation.  Where 0=worst and 1=best solutions
df.Hydropower=(np.max(df.Hydropower)-df.Hydropower)/(np.max(df.Hydropower)-np.min(df.Hydropower))
df.Environment=(np.max(df.Environment)-df.Environment)/(np.max(df.Environment)-np.min(df.Environment))
df.Irrigation=(np.max(df.Irrigation)-df.Irrigation)/(np.max(df.Irrigation)-np.min(df.Irrigation))

# #save to csv for plotting
df.to_csv(output_folder+'/'+feature+'/'+'Best_objectives.csv')

## save best decisions
for i in range(len(policies)):
 	np.savetxt(output_folder2+'/'+feature+'/'+'decisions_best_'+names[i]+'.txt', data[index[i], 0:tot_decisions])

print("start")
subprocess.call(['bash', '../bash/rows2columns.sh', str(tot_decisions), feature])
print("end")

cwd = os.getcwd() 
os.chdir(build_dir)
os.system("make clean")
os.system("make")

os.system(build_dir+'run_simulation.sh %s' % (feature))


print("generating figures")
os.chdir(cwd)
os.system('python main_plots.py')
print("finished generating figures")