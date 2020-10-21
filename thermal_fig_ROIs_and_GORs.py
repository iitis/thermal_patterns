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

Visualisation of ROIs and GORs
"""

import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import get_animal, GOR_CLASSES,GLOBAL_SHOW
from scipy.ndimage.measurements import center_of_mass



def plot_gors(gors,ids=[1],im_index=1,show=GLOBAL_SHOW):
    """
    plots a subset of gors in the image (GOR visualisation)
    
    parameters:
        gors: a modified dictionary of gors with ids
        ids: indices of gors to show
        im_index: index of an image (a counter)
        show: True/False: show or save image 
    """    
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(4,3),dpi=300)

    data,anno = get_animal('D.3')
    anno = anno[20:201,52:300]
    ax=plt.subplot(111)

    res = np.zeros(anno.shape)
    for i_gor in ids:
        temp=anno.copy()
        for cc in gors[i_gor]['roi_group']:
            temp[temp==cc]=-1
        temp[temp!=-1]=0        
        temp[temp==-1]=gors[i_gor]['id']
        assert np.sum(res[temp>0])==0,"{} <- {}, {}".format(np.unique(res[temp>0]),gors[i_gor]['id'],im_index)
        res[temp>0]=temp[temp>0]
    plt.imshow(res,cmap='nipy_spectral',vmax=10)
    for u in np.unique(res):
        if u!=0:
            com = center_of_mass(res==u)    #custom values :-/
            cc = 0
            cr = 0
            if u==9:
                cc+=17
            if u==5:
                cc-=10
                cr+=20
            if u==10:
                cc+=55
            
            plt.text(com[1]+cc,com[0]+cr,s='{}'.format(int(u)), fontsize=12,color='white',fontweight='bold')
    
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)        
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.savefig('fig/gors_{}.pdf'.format(im_index),bbox_inches='tight',pad_inches=0)
    plt.close()   


def plot_rois(show=GLOBAL_SHOW):
    """
    plots the rois in the image (ROI visualisation)
    """       
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(4,3),dpi=300)

    _,anno = get_animal('D.3')
    anno = anno[20:201,52:300]
    ax=plt.subplot(111)
    plt.imshow(anno,cmap='nipy_spectral',vmax=15)
    
    #custom values :-/
    cr_c = [0,0,3,5,0,0,0,0,0,0,0,5,0,0,0]
    cc_c = [-10,-5,-3,-5,0,-5,0,0,-5,-7,0,-10,-7,-10,-7]
    for i,c in enumerate(range(1,16)):
        temp=anno.copy()

        temp[temp!=c]=0
        temp[temp==c]=1
        com = center_of_mass(temp)
        plt.text(com[1]+cc_c[i],com[0]+cr_c[i],s='{}'.format(c), fontsize=12,color='white',fontweight='bold')
        
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)        
    plt.tight_layout()
    if show:
        plt.show()
    else:    
        plt.savefig('fig/rois.pdf',bbox_inches='tight',pad_inches=0)
    plt.close()   
    

if __name__ == '__main__':
    plot_rois()
    gc = GOR_CLASSES
    for i in range(len(gc)):
        gc[i]['id']=i+1
    plot_gors(gors = gc,ids=[0,2,3],im_index=1)
    plot_gors(gors = gc,ids=[1,4,7,8],im_index=2)
    plot_gors(gors = gc,ids=[5,6],im_index=3)
    plot_gors(gors = gc,ids=[9],im_index=4)
