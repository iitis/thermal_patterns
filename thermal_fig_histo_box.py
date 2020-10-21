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

Boxplots of ROI for animal types
"""

import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import get_name,get_animal_rois,INDICES,GLOBAL_SHOW

def plot_box(atype='H',show=GLOBAL_SHOW):
    """
    plots boxplot of temperatures in rois for a given animal type
    parameters:
        
        atype - animal type ['H','D']
    """
    arr = [] 
    for i in INDICES:
        name = get_name(atype,i)
        rois = get_animal_rois(name)
        arr.append(rois)
    
    rois = []
    for rid in range(15):
        rois.append(np.concatenate([v[rid] for v in arr]))
    
    plt.rcParams.update({'font.size': 10})
    plt.figure(figsize=(4,3),dpi=300)
    
    medians = [np.median(v) for v in rois]
    arg = np.argsort(medians)[::-1]
    rois=np.array(rois)
    rois=rois[arg]
    indices = np.arange(15)+1
    
    plt.boxplot(rois,widths = 0.6,flierprops={'marker':'o','markersize':1,'alpha':0.7,'markeredgecolor':'#DC3220','linestyle':'none'})

    plt.ylim(10,30)
    plt.xticks(np.arange(15)+1,indices[arg])
    plt.xlabel("ROI")
    plt.ylabel("Temperature")
    plt.tight_layout(0.2,0.2,0.2)
    if show:
        plt.show()
    else:
        plt.savefig('fig/box_{}.pdf'.format(atype),bbox_inches='tight',pad_inches=0)#
    plt.close()

if __name__ == '__main__':
    plot_box('H')
    plot_box('D') 