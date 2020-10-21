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

Heatmap plots for horses/donkeys
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from thermal_utlis import get_animal,get_name
from thermal_utlis import INDICES,ATYPES,GLOBAL_SHOW


def print_global_temperatures():
    """
    prints global temperature stats for animals
    """
    temps = {}
    for atype in ATYPES:
        temps[atype]=[]
        for i in INDICES:
            arr, anno = get_animal(get_name(atype,i))
            temps[atype].append(arr[anno!=0])
        temps[atype] = np.concatenate(temps[atype])
        print (atype,'min: {:0.2f},mean:{:0.2f}({:0.2f}), median:{:0.2f},  max: {:0.2f}'.format(np.min(temps[atype])
                                                                                              ,np.mean(temps[atype])
                                                                                              ,np.std(temps[atype])
                                                                                              ,np.median(temps[atype])
                                                                                              ,np.max(temps[atype])))         

def plot_animal_heatmap(name,gmin=8.80,gmax=30.65,cutb=None,is_bg=False,show=GLOBAL_SHOW,custom_name=None):
    """
    plots heatmaps for a given animal
    parameters:
        
        name: animal name
        gmin: min temperature for colormap scaling, if None
            local temperature range is used
        gmax: max temperature for colormap  scaling
        cutb: None or cut box for the image [cutb[0]:cutb[1],cutb[2]:cutb[3]]
        is_bg: True for masked background, False otherwise
    
    """
    assert (gmin is None and gmax is None) or (gmin>0 and gmax>gmin)
    
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(4,3),dpi=300)
    arr, anno = get_animal(name)
    if not is_bg:
        arr[anno==0]=0
    
    
    if cutb is not None:
        arr = arr[cutb[0]:cutb[1],cutb[2]:cutb[3]]
        anno = anno[cutb[0]:cutb[1],cutb[2]:cutb[3]]
    
    vmin = np.min(arr[anno>0]) if gmin is None else gmin
    vmax = np.max(arr[anno>0]) if gmax is None else gmax
    ax=plt.subplot(111)
    im = plt.imshow(arr,cmap='nipy_spectral',vmin=vmin,vmax=vmax)
    if cutb is None:
        plt.text(20,220,s=name, fontsize=18,color='white')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    
    plt.tight_layout()
    indstr = '_relative' if gmin is None else ''
    if show:
        plt.show()
    else:
        name = '{}.pdf'.format(custom_name) if custom_name is not None else 'fig/{}{}.pdf'.format(name,indstr)
        plt.savefig(name,bbox_inches='tight',pad_inches=0)
    plt.close()    


if __name__ == '__main__':
    plot_animal_heatmap(name='D.3',gmin=8.80,gmax=30.65,cutb=[20,201,52,300],is_bg=False,custom_name='fig/heat')
    plot_animal_heatmap(name='D.3',gmin=8.80,gmax=30.65,cutb=[20,201,52,300],is_bg=True,custom_name='fig/heat_all')
    print_global_temperatures()
    plot_animal_heatmap('D.17',gmin=8.80,gmax=30.65)
    plot_animal_heatmap('D.18',gmin=8.80,gmax=30.65)
    plot_animal_heatmap('D.12',gmin=None,gmax=None)
    plot_animal_heatmap('H.11',gmin=None,gmax=None)
    if True:
        for atype in ATYPES:
            for i in INDICES:
                plot_animal_heatmap(get_name(atype,i))
            
   
  