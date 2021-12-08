import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd
import os



def mef_plots(input_folder,output_folder,label_policy,delta_release_balance,feature, policies, n_years,n_months,delta_target,colors, months, title, mef_folder):
	left=0.18; bottom=0.1; right=0.96; top=0.92; wspace=0.2; hspace=0.2
	font_size=22
	font_sizey=22
	font_size_title=25
	fig = plt.figure()
	for p in range(len(policies)):
		#actual release for mef_
		data=np.loadtxt(input_folder+feature+'/rDelta_'+policies[p]+'.txt')
		#target mef
		rMEF=np.reshape(data,(n_years,n_months))
		mean_mef=np.mean(rMEF,0)
		min_mef=np.min(rMEF,0)
		max_mef=np.max(rMEF,0)

		plt.fill_between(range(n_months),max_mef,min_mef, alpha=0.5,color=colors[p])
		plt.plot(mean_mef, linewidth=5,color=colors[p], label=label_policy[p])
		
		plt.title('Delta releases-'+title+delta_release_balance, fontsize=font_size_title)
		plt.ylabel('Average environmental flows bounded\nby min and max values [m'r'$^3$/sec]', fontsize=font_sizey, labelpad=20)
		plt.xticks(np.arange(n_months),months, rotation=30, fontsize=font_size)
		plt.yticks(fontsize=font_size)
		plt.xlim([0,11])
		
	plt.plot(delta_target, color='k', linestyle=':', linewidth=6, label='MEF Delta target')
	plt.legend(fontsize=font_size)
	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
	fig.set_size_inches(12,10)
	return plt.savefig(output_folder+feature+'/png/rMEF.png')



