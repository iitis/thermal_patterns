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

Thermal pattern matrices for outlier cases
"""
import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import GOR_CLASSES,GLOBAL_SHOW
from matplotlib.colors import ListedColormap


from thermal_fig_ROI_matrix import mww_test,get_roi_group_a
import seaborn as sns

    
#prepare outlier cases
def prepare_pattern_matrices_spec(atype='D',p=0.001,a_index=17):
    """
    prepares a thermal pattern matrix for a specific animal
    (used for outlier cases of D.17,D.18)
    
    parameters:
        atype: animal type [H,D]
        p: required p value for the MWW test
        a_index: animal index
    
    """
    N = len(GOR_CLASSES)
    rgs = []
    for rg in GOR_CLASSES:
        animals,data = get_roi_group_a(atype=atype,roi_group=rg['roi_group'],a_indices=[a_index])
        rgs.append({'animals':animals,'data':data})
    
    deltas = np.zeros((N,N))    
    s_global = np.zeros((N,N),dtype=np.int32)
    for r in range(N):
        for c in range(N):
            deltas[r,c]=np.mean(rgs[r]['data'])-np.mean(rgs[c]['data'])
            alternative = 'greater' if deltas[r,c]>0 else 'less'  
            s_global[r,c] = mww_test(rgs[r]['data'],rgs[c]['data'],p=p,alternative=alternative)
    np.savez_compressed('pattern_matrices_{}_spec_{}.npz'.format(atype,a_index),deltas=deltas,s_global=s_global)            
            
def plot_pattern_matrix_global_spec(atype='D',a_index=18,show=GLOBAL_SHOW):
    """
    plots a thermal pattern matrix for a specific animal
    (used for outlier cases of D.17,D.18)
    
    parameters:
        atype: animal type [H,D]
        a_index: animal index
        show: True/False: show or save image    
    """    

    pm = np.load('pattern_matrices_{}_spec_{}.npz'.format(atype,a_index))
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
        plt.savefig('fig/m_deltas_{}_spec_{}.pdf'.format(atype,a_index),bbox_inches='tight',pad_inches=0)
    plt.close()


def plot_pattern_matrix_combined_spced(atype='D',a_index=17,show=GLOBAL_SHOW):
    """
    plots a a comparison of thermal pattern similarity for an animal
    (used for outlier cases of D.17,D.18)
    
    parameters:
        atype: animal type [H,D]
        a_index: animal index
        show: True/False: show or save image    

    plots the comparison of pattern similarity
    """

    pmhd = [np.load('pattern_matrices_{}_spec_{}.npz'.format(atype,a_index)),np.load('pattern_matrices_{}.npz'.format(atype))]
    plt.rcParams.update({'font.size': 10})
    
    labels = [v['short'] for v in GOR_CLASSES]
    
    ddhd = [v['deltas'] for v in pmhd]
    for i in range(2):
        ddhd[i][ddhd[i]<0]=-1
        ddhd[i][ddhd[i]>0]=1
    sshd = [v['s_global'] for v in pmhd]
    
    combined = np.zeros_like(ddhd[0],dtype=np.int32)+2 #sanity check
    
    #1: same and significant
    mask =  np.logical_and( ddhd[0]==ddhd[1] , sshd[0]==sshd[1] )
    combined[mask]=1

    np.fill_diagonal(combined,0)
    combined[sshd[1]==0]=0
    
    colors = ['white','#117733','#882255']
    cmap = ListedColormap(colors, name='colors',N=len(colors))

    res = sns.heatmap(data=combined,cmap=cmap,annot=False,linewidths=.5,fmt=".2f",cbar=True,xticklabels=labels, yticklabels=labels,mask=combined==0,vmin=0,vmax=2)
    for _, spine in res.spines.items():
        spine.set_visible(True)
    cbar = res.collections[0].colorbar    
    cbar.set_ticks([1,2])
    cbar.set_ticklabels(['S','NS'])

    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:
        plt.savefig('fig/m_comp_spec_{}.pdf'.format(a_index),bbox_inches='tight',pad_inches=0)    
    plt.close()


if __name__ == '__main__':
    prepare_pattern_matrices_spec(a_index=17)
    prepare_pattern_matrices_spec(a_index=18)
    plot_pattern_matrix_global_spec(a_index=17)
    plot_pattern_matrix_global_spec(a_index=18)
    plot_pattern_matrix_combined_spced(a_index=17)
    plot_pattern_matrix_combined_spced(a_index=18)
