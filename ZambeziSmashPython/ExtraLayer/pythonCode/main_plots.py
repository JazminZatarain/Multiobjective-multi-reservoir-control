def plot_quantities():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import seaborn as sns
    import pandas as pd
    import os
    from irrigation_plots import irr_plots
    from mef_plots import mef_plots
    #from mass_balance_plots import mass_balance_plots
    from summary_fig import summary_plot
    #from parallel_categorical import parallel_plots
    #from scatter_3d import *
    #import execute_all

    plt.rcParams["font.family"] = "Myriad Pro"
    sns.set_style("whitegrid")

    input_folder= '../storage_release/'
    input_folder_objs='../for_plots/'
    target_input_folder='../../data/'
    output_folder='../plots/'
    delta_target=np.loadtxt(target_input_folder+'MEF_delta.txt')
    n_objs=3

    #copy here..
    #####################################
    feature='new_feature'
    #reservoirs=['itt','kgu','kgl','ka','bg','dg','cb','mn']
    reservoirs=['itt','kgu','kgl','ka','cb']
    title='5_res_wKGL'
    input_file='Zambezi_'+title+'.reference'  #'.reference'change filename


    # data= np.loadtxt('../parallel/sets/'+feature+'/'+input_file, skiprows=0+1+2-1)
    delta_release_balance='\n('r'$r_{CB}+Q_{Shire}-r_{Irrd7}-r_{Irrd8}-r_{Irrd9}$)'
    #res_names=['Itezhitezhi','Kafue G. Upper','Kafue G. Lower','Kariba','Batoka Gorge','Devil\'s Gorge','Cahora Bassa', 'Mphanda Nkuwa']
    res_names=['Itezhitezhi','Kafue G. Upper','Kafue G. Lower','Kariba','Cahora Bassa']
    #####copy the segment above#########



    policies=['best_hydro', 'best_env', 'best_irr']
    irr_index=['2','3','4','5','6','7','8','9']
    irr_d=['Irrigation District 2', 'Irrigation District 3', 'Irrigation District 4', 'Irrigation District 5','Irrigation District 6','Irrigation District 7','Irrigation District 8', 'Irrigation District 9']
    label_policy=['Best Hydropower', 'Best Environment', 'Best Irrigation', 'Target Demand']
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    n_months=12
    n_years=20
    purple='#7a0177';yellow='#fdaa09';blue='#1d91c0' #green='#41ab5d'
    colors=[purple,yellow,blue]
    variables_names=[r'$q_t$',r'$h_t$',r'$s_t$',r'$s_{t+1}$',r'$r_{t+1}$',r'$r^{delay}_{t+1}$']
    variables=['q','h_t','s_t','s_t+1','r_t+1','r_d_t+1']


    image_format=['png']
    for im in range(len(image_format)):
        for policy in range(len(policies)):
            if not os.path.exists(output_folder+'/'+feature+'/'+image_format[im]+'/'+policies[policy]):
                    os.makedirs(output_folder+'/'+feature+'/'+image_format[im]+'/'+policies[policy])
    #this generates 8 plots one for each irrigation district:
    for ir in range(len(irr_d)):
        irr_plots(input_folder,target_input_folder,output_folder,feature,ir,irr_d,irr_index,policies,months,label_policy,n_months,n_years,colors)

    # this a summary of the delta releases:
    mef_plots(input_folder,output_folder,label_policy,delta_release_balance,feature, policies, n_years,n_months,delta_target,colors, months, title,target_input_folder)

    #mass balance, prints all variables:
    # for p in range(len(policies)):
    # 	for r in range(1,len(reservoirs)):
    # 		for v in range(len(variables)-1):
    # 			mass_balance_plots(r,p,v,variables_names,variables,input_folder,output_folder,feature,reservoirs,res_names,policies,n_months,months,n_years,colors)

    #this is only for itt to print the delay:
    # for p in range(len(policies)):
    # 	for v in range(len(variables)):
    # 		mass_balance_plots(0,p,v,variables_names,variables,input_folder,output_folder,feature,reservoirs,res_names,policies,n_months,months,n_years,colors)

    v=4 # to print only releases across all reservoirs:
    #for v in range(len(variables)-1): to print all summary figures:
    for p in range(len(policies)):
        fig= plt.figure()
        for r in range(len(reservoirs)):
            summary_plot(v,p,r,fig,input_folder,output_folder,feature,policies,variables,label_policy,reservoirs, res_names,months,n_years,n_months)

    #parallel_plots(input_folder_objs,output_folder,feature,title)


    #x,y,z,n =prepare_data(data, n_objs)


    #scatter_3d(feature,title,n,x,y,z)
