import numpy as np
import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set()

def parallel_plots(input_folder,output_folder,feature,title):
    file_name='Best_objectives'

    names=['Hydropower','Environment','Irrigation']
    data = pd.read_csv(input_folder+feature+'/'+file_name+'.csv', usecols=['Hydropower','Environment','Irrigation','Name'])
    mn_mx= pd.read_csv(input_folder+feature+'/min_max.csv', usecols=names)
    units=['TWh/year','Deficit (cm/sec)'+r'$^2$','Normalized Deficit']

    mx=[]
    mn=[]
    for i in range(len(names)):
    	mini=str(round(mn_mx[names[i]][1],1))
    	maxi=str(round(mn_mx[names[i]][0],1))
    	mx.append(maxi)
    	mn.append(mini)


    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    gray='#bdbdbd'
    purple='#7a0177'
    green='#41ab5d'
    blue='#1d91c0'
    yellow='#fdaa09'
    pink='#c51b7d'


    parallel_coordinates(data,'Name', color= [gray,purple,yellow,blue], linewidth=7, alpha=.8)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=1.5, fontsize=18) 

    i=0
    ax1.set_xticks(np.arange(3))
    ax1.set_xticklabels([mx[i]+'\n'+'\n'+names[i]+'\n'+units[i], mx[i+1]+'\n'+'\n'+names[i+1]+'\n'+units[i+1],mx[i+2]+'\n'+'\n'+names[i+2]+'\n'+units[i+2]], fontsize=18)
    ax2 = ax1.twiny()
    ax2.set_xticks(np.arange(3))
    ax2.set_xticklabels([mn[i], mn[i+1],mn[i+2]], fontsize=18)
    ax1.get_yaxis().set_visible([])
    plt.text(1.02, 0.5, 'Direction of Preference $\\rightarrow$', {'color': '#636363', 'fontsize': 20},
             horizontalalignment='left',
             verticalalignment='center',
             rotation=90,
             clip_on=False,
             transform=plt.gca().transAxes)

    fig.set_size_inches(17.5, 9)
    return(plt.savefig(output_folder+feature+'/pdf/'+title+'res_tradeoffs.pdf', bbox_inches="tight"), plt.savefig(output_folder+feature+'/png/'+title+'res_tradeoffs.png', bbox_inches="tight"))


