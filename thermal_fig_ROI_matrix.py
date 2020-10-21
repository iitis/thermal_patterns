# -*- coding: utf-8 -*-
"""
************************************************************************
Copyright 2020 Institute of Theoretical and Applied Informatics, 
Polish Academy of Sciences (ITAI PAS) https://www.iitis.pl
author: M. Romaszewszki, mromaszewski@iitis.pl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
************************************************************************

Code for experiments in the paper by  
M. Domino, M. Romaszewski,  T. Jasinski,  M. Masko
`Comparison of surface thermal patterns of horses and donkeys in IRT images'
preprint: http://arxiv.org/abs/2010.09302

Thermal pattern matrices 
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from thermal_utlis import get_name,get_animal_rois,GOR_CLASSES,mww_test,INDICES,ATYPES,GLOBAL_SHOW
from matplotlib.colors import ListedColormap
 

def get_roi_group_a(atype='H',roi_group=[8,9],a_indices=INDICES):
    """
    returns ROI groups for every animal of a given species as a concatenated vector
    
    parameters:
        atype = animal type [H,D]
        roi_group -  list of rois to include
        a_indices - animal indices
    
    return:
        a dictinary indexed by animals with individual roi vectors
        a concatenated roi vector
    """
    animals = {}
    for a in a_indices:
        animals[a]=[]
        
    for a in a_indices:
        name=get_name(atype,a)
        rois = get_animal_rois(name)
        for r in roi_group: 
            animals[a].append(rois[r-1])
    for a in a_indices:
        animals[a]=np.concatenate(animals[a])
    
    data = np.concatenate([animals[a] for a in animals])
    
    return animals,data
    

def prepare_pattern_matrices(atype='H',p=0.001):
    """
    prepares a thermal pattern matrix
    
    parameters:
        atype: animal type [H,D]
        p: required p value for the MWW test

    """    
    N = len(GOR_CLASSES)
    rgs = []
    for rg in GOR_CLASSES:
        animals,data = get_roi_group_a(atype=atype,roi_group=rg['roi_group'])
        rgs.append({'animals':animals,'data':data})
    
    deltas = np.zeros((N,N))    
    s_global = np.zeros((N,N),dtype=np.int32)
    s_local = np.zeros((N,N,len(INDICES)),dtype=np.int32)
    for r in range(N):
        for c in range(N):
            deltas[r,c]=np.mean(rgs[r]['data'])-np.mean(rgs[c]['data'])
            alternative = 'greater' if deltas[r,c]>0 else 'less'  
            s_global[r,c] = mww_test(rgs[r]['data'],rgs[c]['data'],p=p,alternative=alternative)
            for a in INDICES:
                s_local[r,c,a-1] = mww_test(rgs[r]['animals'][a],rgs[c]['animals'][a],p=p,alternative=alternative)
    np.savez_compressed('pattern_matrices_{}.npz'.format(atype),deltas=deltas,s_global=s_global,s_local=s_local)            
                
            
def plot_pattern_matrix_global(atype='H',show=GLOBAL_SHOW):
    """
    Plots the global thermal pattern matrix
    
    parameters:
        atype: animal type [H,D]
        show: True/False: show or save image   
    """      

    pm = np.load('pattern_matrices_{}.npz'.format(atype))
    cmap = 'RdBu_r'

    plt.rcParams.update({'font.size': 10})
    labels = [v['short'] for v in GOR_CLASSES]
    
    sns.heatmap(data=pm['deltas'],cmap=cmap,annot=True,linewidths=.5,fmt=".2f",mask = np.logical_or(pm['s_global'],pm['deltas']==0),cbar=False
                ,xticklabels=labels, yticklabels=labels)
    res= sns.heatmap(data=pm['deltas'],cmap=cmap,annot=True,linewidths=.5,fmt=".2f",mask = pm['s_global']==0,annot_kws={"style": "italic", "weight": "bold",'fontsize':'10'}
                     ,xticklabels=labels, yticklabels=labels)
    
    for _, spine in res.spines.items():
        spine.set_visible(True)
    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:    
        plt.savefig('fig/m_deltas_{}.pdf'.format(atype),bbox_inches='tight',pad_inches=0)
    plt.close()
        
def plot_pattern_matrix_local(atype='H',show=GLOBAL_SHOW):
    """
    Plots the local thermal pattern matrix
    
    parameters:
        atype: animal type [H,D]
        show: True/False: show or save image   
    """      
    
    pm = np.load('pattern_matrices_{}.npz'.format(atype))
    loc = pm['s_local']
    loc = np.sum(loc,axis=2)
    labels = [v['short'] for v in GOR_CLASSES]

    cmap = 'YlGn'
    plt.rcParams.update({'font.size': 10})
    res = sns.heatmap(loc,cmap=cmap,annot=True,linewidths=.5,annot_kws={'fontsize':'10'}
                      ,xticklabels=labels, yticklabels=labels,mask=np.eye(loc.shape[0]),vmin=0,vmax=16)
     
    for _, spine in res.spines.items():
        spine.set_visible(True)
    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:
        plt.savefig('fig/m_ss_{}.pdf'.format(atype),bbox_inches='tight',pad_inches=0)    
    plt.close()

                
def plot_pattern_matrix_global_combined(show=GLOBAL_SHOW):
    """
    plots the comparison of both the global and the local pattern matrices
    parameters:
        show: True/False: show or save image   
    """

    pmhd = [np.load('pattern_matrices_{}.npz'.format('H')),np.load('pattern_matrices_{}.npz'.format('D'))]
    plt.rcParams.update({'font.size': 10})
    
    labels = [v['short'] for v in GOR_CLASSES]
    
    ddhd = [v['deltas'] for v in pmhd]
    for i in range(2):
        ddhd[i][ddhd[i]<0]=-1
        ddhd[i][ddhd[i]>0]=1
    
    sshd = [v['s_global'] for v in pmhd]
    combined = np.zeros_like(ddhd[0],dtype=np.int32)-10 #sanity check
    
    #1: same and significant
    mask =  np.logical_and( ddhd[0]==ddhd[1] , (sshd[0]+sshd[1])==2 )
    combined[mask]=1

    #2: same but insignificant
    mask =  np.logical_and( ddhd[0]==ddhd[1] , (sshd[0]+sshd[1])!=2 )
    combined[mask]=2

    #3: H warmer, significant
    mask =  np.logical_and( ddhd[0]>ddhd[1] , (sshd[0]+sshd[1])==2 )
    combined[mask]=3

    #4: H warmer, insifnificant
    mask =  np.logical_and( ddhd[0]>ddhd[1] , (sshd[0]+sshd[1])!=2 )
    combined[mask]=4


    #5: H warmer, significant
    mask =  np.logical_and( ddhd[0]<ddhd[1] , (sshd[0]+sshd[1])==2 )
    combined[mask]=5

    #6: H warmer, insifnificant
    mask =  np.logical_and( ddhd[0]<ddhd[1] , (sshd[0]+sshd[1])!=2 )
    combined[mask]=6
    
    np.fill_diagonal(combined,0)
    
    colors = ['white','#117733','#44AA99', '#882255','#CC6677','#0072B2','#56B4E9']
    cmap = ListedColormap(colors, name='colors')

    res = sns.heatmap(data=combined,cmap=cmap,annot=False,linewidths=.5,fmt=".2f",cbar=True,xticklabels=labels, yticklabels=labels,mask=combined==0,vmin=0,vmax=6)
    for _, spine in res.spines.items():
        spine.set_visible(True)
    cbar = res.collections[0].colorbar    
    cbar.set_ticks([1,2,3,4,5,6,7])
    cbar.set_ticklabels(['SPS','SP','HWS','HW','HCS','HC'])

    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:
        plt.savefig('fig/m_comp.pdf',bbox_inches='tight',pad_inches=0)
    plt.close()

    #the second table - local summary

    lpmmhd = [np.load('pattern_matrices_{}.npz'.format('H')),np.load('pattern_matrices_{}.npz'.format('D'))]
    
    lddhd = np.dstack([np.sum(v['s_local'],axis=2) for v in lpmmhd])
    lddhd = np.min(lddhd,axis=2)
    
    #only show statistically significant classes 
    for i in [2,4,6]:
        lddhd[combined==i]=0
    
    labels = [v['short'] for v in GOR_CLASSES]
    
    cmap = 'YlGn'
    plt.rcParams.update({'font.size': 10})
    res = sns.heatmap(lddhd,cmap=cmap,annot=True,linewidths=.5,annot_kws={'fontsize':'10'}
                      ,xticklabels=labels, yticklabels=labels,mask=lddhd==0,vmin=0,vmax=16)
     
    for _, spine in res.spines.items():
        spine.set_visible(True)
    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:
        plt.savefig('fig/m_comp_local.pdf',bbox_inches='tight',pad_inches=0)
    plt.close()
    
if __name__ == '__main__':
    for a in ATYPES:
        prepare_pattern_matrices(a)
    for a in ATYPES:
        plot_pattern_matrix_global(a)
        plot_pattern_matrix_local(a)
    plot_pattern_matrix_global_combined()
