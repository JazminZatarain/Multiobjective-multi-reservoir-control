import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import os

sns.set()

def mass_balance_plots(r,p,v,variables_names,variables,input_folder,output_folder,feature,reservoirs,res_names,policies,n_months,months,n_years,colors):
	
	left=0.13; bottom=0.12; right=0.98; top=0.95; wspace=0.2; hspace=0.2
	font_size=18
	font_sizey=20
	font_size_title=25

	min_max_storage=np.loadtxt('../for_plots/min_max_storage')
	min_max_level=np.loadtxt('../for_plots/min_max_level')
	turbine_capacity=np.loadtxt('../for_plots/turbine_capacity.txt')


	y_label=['Inflow [m'r'$^3$/sec]','Level (t) [m]','Storage (t) [m'r'$^3$]','Storage (t+1) [m'r'$^3$]','Actual Release (t+1) [m'r'$^3$/sec]','Actual Release (t+2) [m'r'$^3$/sec]']
	fig = plt.figure()
	locs, labels = plt.xticks()
	data=np.loadtxt(input_folder+feature+'/'+reservoirs[r]+'_'+policies[p]+'.txt')
	data=np.reshape(data[:,v],(n_years,n_months))
	avg=np.mean(data,0)
	mini=np.min(data,0)
	maxi=np.max(data,0)
	if v==1:
		plt.hlines(y=min_max_level[r][0], xmin=0, xmax=11, linewidth=5, color='k', linestyle=':')
		plt.hlines(y=min_max_level[r][1], xmin=0, xmax=11, linewidth=5, color='k', linestyle=':')
		plt.text(10, min_max_level[r][0], 'Min level', bbox=dict(facecolor='gray', alpha=1),color='white',fontsize=14)
		plt.text(10, min_max_level[r][1], 'Max level', bbox=dict(facecolor='gray', alpha=1),color='white',fontsize=14)

	if v==2 or v==3:
		plt.hlines(y=min_max_storage[r][0], xmin=0, xmax=11, linewidth=5, color='k', linestyle=':')
		plt.hlines(y=min_max_storage[r][1], xmin=0, xmax=11, linewidth=5, color='k', linestyle=':')
		plt.text(10, min_max_storage[r][0], 'Min storage', bbox=dict(facecolor='gray', alpha=1),color='white',fontsize=14)
		plt.text(10, min_max_storage[r][1], 'Max storage', bbox=dict(facecolor='gray', alpha=1),color='white',fontsize=14)


	if v==4:
		turbine_release=np.loadtxt(input_folder+feature+'/qturb_'+reservoirs[r]+'_'+policies[p]+'.txt')
		turb_rel=np.reshape(turbine_release,(n_years,n_months))
		max_turb=np.max(turb_rel,0)
		plt.hlines(y=turbine_capacity[r], xmin=0, xmax=11, linewidth=5, color='k', linestyle=':')
		plt.text(9, turbine_capacity[r], 'Turbine Capacity', bbox=dict(facecolor='gray', alpha=1),color='white', fontsize=font_size)
		plt.plot(range(n_months), max_turb,color='white', linewidth=6, alpha=.3)
		plt.plot(range(n_months), max_turb,color=colors[p], linestyle=':', linewidth=5, label='Turbined Release')
	

	plt.fill_between(range(n_months),maxi,mini, alpha=0.5,color=colors[p])
	plt.plot(avg,color=colors[p],linewidth=5)
	plt.plot(avg,color=colors[p],linewidth=5)
	plt.xticks(np.arange(n_months),months, rotation=30, fontsize=font_size)
	plt.ylabel(y_label[v], fontsize=font_size_title)
	plt.yticks(fontsize=font_sizey)
	plt.title(res_names[r]+' ('+ variables_names[v]+')', fontsize=font_size_title)
	plt.xlim([0,11])
	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

	fig.set_size_inches(11,12)
	plt.legend(fontsize=font_sizey)
	return(plt.savefig(output_folder+feature+'/pdf/'+policies[p]+'/'+reservoirs[r]+'_'+variables[v]+'_'+policies[p]+'.pdf'),plt.savefig('../plots/'+feature+'/png/'+policies[p]+'/'+reservoirs[r]+'_'+variables[v]+'_'+policies[p]+'.png', transparent=True))
