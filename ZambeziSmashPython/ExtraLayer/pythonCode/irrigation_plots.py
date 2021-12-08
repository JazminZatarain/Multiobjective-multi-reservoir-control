import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd


def irr_plots(input_folder,t_irr_folder,output_folder,feature,ir,irr_d,irr_index,policies,months,label_policy,n_months,n_years, colors):
	left=0.05; bottom=0.17; right=0.98; top=0.89; wspace=0.2; hspace=0.2
	font_size=22
	font_sizey=22
	font_size_title=25

	#for ir in range(len(irr_d)):
	fig = plt.figure()
	for p in range(len(policies)):
	#actual release for irrigation:	
		data=np.loadtxt(input_folder+feature+'/irr_'+policies[p]+'.txt')
	#irrigation target demand:
		data2=np.loadtxt(t_irr_folder+'IrrDemand'+irr_index[ir]+'.txt')
		irrigation=np.reshape(data[:,ir],(n_years,n_months))

		mean_irr=np.mean(irrigation,0)
		min_irr=np.min(irrigation,0)
		max_irr=np.max(irrigation,0)

		plt.fill_between(range(n_months),max_irr,min_irr, alpha=0.5,color=colors[p])
		plt.plot(mean_irr, linewidth=5,color=colors[p], label=label_policy[p])
	
		plt.title(irr_d[ir], fontsize=font_size_title)
		plt.ylabel('Average diversion bounded \nby min and max values [m'r'$^3$/sec]', fontsize=font_sizey, labelpad=20)
		plt.xticks(np.arange(n_months),months, rotation=30, fontsize=font_size)
		plt.yticks(fontsize=font_size)
		plt.xlim([0,11])
	
	plt.plot(data2, color='k', linestyle=':', linewidth=5, label='Target Demand')
	plt.legend(fontsize=font_size)
	fig.set_size_inches(12,10)
	return plt.savefig('../plots/'+feature+'/png/irr_d_'+irr_index[ir]+'.png')



