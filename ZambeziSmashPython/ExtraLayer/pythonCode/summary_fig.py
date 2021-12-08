import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib as mpl
import os
sns.set()

def summary_plot(v,p,r,fig,input_folder,output_folder,feature,policies,variables,label_policy,reservoirs, res_names, months,n_years,n_months):
	colorsr=['#b2182b','#d6604d','#fc8d59','#f4a582','#92c5de','#6baed6','#4393c3','#2166ac']
	left=0.13; bottom=0.12; right=0.75; top=0.95; wspace=0.2; hspace=0.2
	font_size=18
	font_sizey=20
	font_size_title=25
	y_label=['Inflow [m'r'$^3$/sec]','Level (t) [m]','Storage (t) [m'r'$^3$]','Storage (t+1) [m'r'$^3$]','Average Release (t+1) [m'r'$^3$/sec]', 'Average Release (t+2) [m'r'$^3$/sec]']
	locs, labels = plt.xticks()
	data=np.loadtxt(input_folder+feature+'/'+reservoirs[r]+'_'+policies[p]+'.txt')
	data=np.reshape(data[:,v],(n_years,n_months))
	avg=np.mean(data,0)
	plt.plot(avg,color=colorsr[r],linewidth=7,linestyle=':',label=res_names[r])
	plt.xticks(np.arange(n_months),months, rotation=30, fontsize=font_size)
	plt.ylabel(y_label[v], fontsize=font_size_title,labelpad=30)
	plt.yticks(fontsize=font_sizey)
	plt.title(label_policy[p],fontsize=font_size_title)
	plt.xlim([0,11])
	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
	fig.set_size_inches(14,10)
	plt.legend(fontsize=font_sizey,labelspacing=3, loc=6, bbox_to_anchor=(1, 0.5)) #bbox_to_anchor=(0., 1.02, 1., .102), loc=3,fontsize=font_sizey, ncol=4, mode="expand")

	return plt.savefig(output_folder+feature+'/png/'+variables[v]+'_all_reservoirs_'+policies[p]+'.png')

