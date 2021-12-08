from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(style='whitegrid')

def norm_var(x):
	norm=(np.max(x)-x)/(np.max(x)-np.min(x))
	return(norm)

def prepare_data(data, n_objs):
	x=data[:,np.shape(data)[1]-n_objs]
	y=data[:,np.shape(data)[1]-n_objs+1]
	z=data[:,np.shape(data)[1]-n_objs+2]
	n=np.shape(data)[0]
	return x,y,z,n

def count_zeros(number):
    return str(number).count('0')

def scatter_3d(feature,fig_name,n,x,y,z):
	fig = plt.figure()
	c = np.abs(x)
	scale=100000
	cmap = plt.cm.get_cmap("YlGnBu_r")
	units=['[TWh/year]','[cms]'+r'$^2$','Normalized']
	labelx=r'$\leftarrow$'+'Hydropower Deficit \n'+units[0]
	labelx2=r'$\leftarrow$'+'Hydropower Deficit [TWh/year]' 
	labely=r'$\leftarrow$'+'Environmental Deficit\n'+units[1]
	labely2='Environmental Deficit [cms]'+r'$^2$ :'
	labelz=r'$\leftarrow$'+'Irrigation Deficit\n'+units[2]
	title=fig_name
	y_norm=norm_var(y)
	markersize=(1-norm_var(y))*450
	edgecolors='gray'
	exp=count_zeros(scale)
	ax = fig.add_subplot(111, projection='3d')
	left=0.0; bottom=0.1; right=0.98; top=0.92; wspace=0.2; hspace=0.2
	font_size=18;font_sizey=25;font_size_title=35;labelpad=30
	minx=np.min(x)
	maxx=np.max(x)
	miny=np.min(y)
	maxy=np.max(y)
	minz=np.min(z)
	miny_marker=np.min(y/scale)
	maxy_marker=np.max(y/scale)
	y=y/scale
	im= ax.scatter(x, y, z, c=c, cmap= cmap, s=markersize, edgecolors=edgecolors)
	ax.scatter(minx, miny/scale, minz, c='gray', s=800, marker='*',edgecolors=edgecolors)
	ax.text(minx, miny/scale-5, minz+.1,  'Preferred \nsolution', size=20, zorder=1, color='k', bbox=dict(facecolor='gray', alpha=0.2))
	ax.set_xlabel(labelx, fontsize=font_sizey, labelpad=labelpad)
	ax.set_ylabel(labely+' ('+r'$10^{}$'.format(exp)+')', fontsize=font_sizey, labelpad=labelpad+10, rotation=40)
	ax.set_zlabel(labelz, fontsize=font_sizey, labelpad=labelpad)
	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
	plt.xticks(fontsize=font_sizey)
	plt.yticks(fontsize=font_sizey)
	plt.title(title, fontsize=font_size_title, pad=40)
	cbaxes = fig.add_axes([0.2, .04, 0.65, .03]) 
	cbar= fig.colorbar(im, ax=ax, ticks=[np.min(minx),np.max(maxx)],cax = cbaxes,orientation='horizontal',format='%.0f')

	cbar.ax.tick_params(labelsize=font_sizey)
	cbar.set_label(labelx2, labelpad=-28, fontsize=font_sizey)
	im.set_clim(np.min(x), np.max(x))
	for t in ax.zaxis.get_major_ticks(): t.label.set_fontsize(font_sizey)
	ax.view_init(elev=47, azim=-20)
	print('ax.azim {}'.format(ax.azim))
	print('ax.elev {}'.format(ax.elev))
	marker_size=[miny_marker, maxy_marker]
	labels=[str(np.ceil(miny_marker*scale)), str(np.ceil(maxy_marker*scale))]
	for i in range(len(marker_size)):
			ax.scatter([], [], c='k', alpha=0.3, s=marker_size[i]*20, label=labels[i])
    	h, l = ax.get_legend_handles_labels() # Extracting handles and labels
	ph = [plt.plot([],marker="", ls="")[0]] # Canvas
	handles = ph + h
	labels = [labely2] + l  # Merging labels
	legend=plt.legend(handles, labels, scatterpoints=1, frameon=False, fontsize=font_sizey, loc='upper right', 
           fancybox=True, shadow=True,ncol=3, bbox_to_anchor=(1.1,-1))

	fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
	fig.set_size_inches(15,15)
	return(fig.savefig('../plots/'+feature+'/pdf/'+fig_name+'_pf.pdf',bbox_inches='tight',transparent=True), fig.savefig('../plots/'+feature+'/png/'+fig_name+'_pf.png',bbox_inches='tight',transparent=True))


def scatter_3d_two_sets(x1,x2,y1,y2,z1,z2,labelx,labely,labelz,label1, label2, cmap1,cmap2, markersize,edgecolors):
	fig = plt.figure()
	c = np.abs(x1)
	c2 = np.abs(x2)
	ax = fig.add_subplot(111, projection='3d')
	n = np.shape(data1)[0]
	ax.scatter(x1, y1, z1, c=c, cmap= cmap1, label=label1, s=markersize, edgecolors=edgecolors)
	ax.scatter(x2, y2, z2, c=c2, cmap=cmap2, label=label2, s=markersize, edgecolors=edgecolors)
	ax.set_xlabel(labelx)
	ax.set_ylabel(labely)
	ax.set_zlabel(labelz)
	plt.legend()
	return(plt.show())

# x2,y2,z2, =prepare_data(data2, n_objs)
# title='4res'
# scatter_3d_single_set(data2,'../figures/',title,x2,y2,z2)


#scatter_3d_two_sets(x1,x2,y1,y2,z1,z2,'Hydropower','Environment','Irrigation', 'Fede\'s reference set \n 10 seeds, 1 MNFE', 'Without split irrigation \n Single seed 500K', cmap1,cmap2,20,'k')
