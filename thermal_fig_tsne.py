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

T-SNE data visualisation
"""

import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import get_name,get_animal_rois,ATYPES,INDICES,GLOBAL_SHOW
from scipy.stats import skew, kurtosis  
from sklearn.manifold import TSNE


def plot_groups(stat=np.mean,normalise=False,show=GLOBAL_SHOW):
    """
    Compare ROI features with t-SNE (expecting observable structure in data)
    warning: t-SNE is a nondeterministic algorithm
    paramters:
        stat: feature extraction statistics
        normalise: normalise features by removing the global average
        show: True/False: show or save image   
    """
    
    data = []
    y = []
    for atype in ATYPES:
        for a in INDICES:
            rois = get_animal_rois(get_name(atype=atype,index=a))
            if rois != None:
                y.append(0 if atype =='H' else 1)
                if normalise:
                    gv = np.mean(np.concatenate(rois))
                    rois = [v-gv for v in rois]
                temp = [stat(v) for v in rois]
                data.append(temp) 
    
    plt.rcParams.update({'font.size': 12})
    
    X = np.array(data)
    y=np.array(y)
    tsne = TSNE(perplexity=5)
    X = tsne.fit_transform(X)
    where = y==0
    plt.scatter(X[where,0],X[where,1],color = '#DC3220', label='Horses')
    where = y==1
    plt.scatter(X[where,0],X[where,1],color = '#005AB5', label='Donkeys')
    plt.legend()
    nstr = '_norm' if normalise else ''
    if show:
        plt.show()
    else:
        plt.savefig('fig/tsne_{}{}.pdf'.format(stat.__name__,nstr),bbox_inches='tight',pad_inches=0)
    plt.close()    
    

if __name__ == '__main__':
    for stat in [np.mean,np.std,skew, kurtosis]:
        plot_groups(stat)
    plot_groups(np.mean,True)