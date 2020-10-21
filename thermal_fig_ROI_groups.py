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

Histograms for GORs
"""

import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import get_name,get_animal_rois,GOR_CLASSES,INDICES,GLOBAL_SHOW
from scipy.stats import mannwhitneyu


   
def get_roi_group_a(atype='H',roi_group=[8,9]):
    """
    returns a GOR of all animals of a given species as a vector
    
    parameters:
        atype = animal type [H,D]
        roi_group -  list of rois to include (GOR)
    
    return:
        vector of temperature values of all animals in GOR
    """
    data = []
    for i in INDICES:
        name=get_name(atype,i)
        rois = get_animal_rois(name)
        for r in roi_group: 
            data.append(rois[r-1])
    return np.concatenate(data)


def stats_species_gors(roi_group=[8,9],group_name='rump',p=0.001,short=None):
    """
    wilcoxon test of statistical significance for temp. difference
    between H/D GORs
    
    parameters:
        roi_group -  list of rois to include
        group_name - name of the group (savefile name)
        p - required p value
        short: short name (optional)
    return:
        test result (True/False)
 
    """
    
    H = get_roi_group_a(atype='H',roi_group=roi_group)
    D = get_roi_group_a(atype='D',roi_group=roi_group)

    mm = np.min([len(H),len(D)])
    np.random.shuffle(H)
    np.random.shuffle(D)
    s,s_p = mannwhitneyu(H[:mm],D[:mm],alternative='greater')
    print ("{}: {}/{:0.4f}, {}".format(group_name,s,s_p,s_p<p))
    return (s_p<p)
    


def plot_species_gor_histo(roi_group=[8,9],group_name='rump',short=None,show=GLOBAL_SHOW):
    """
    plots species (H/D) temperature histogram for a given GOR 
    
    parameters:
        roi_group -  list of rois to include (GOR)
        group_name - name of the group (savefile name)
        short: short name (optional)
        show: True/False: show or save image
    """
    assert len(roi_group)>0 and np.min(roi_group)>0 and np.max(roi_group)<16

    plt.rcParams.update({'font.size': 10})
    plt.figure(figsize=(2,1.5),dpi=300)
    
    for atype in ['H','D']:
        data = get_roi_group_a(atype=atype,roi_group=roi_group)
        cc = '#DC3220' if atype == 'H' else '#005AB5'
        ll = 'H' if atype == 'H' else 'D'
        plt.hist(data,bins=100,color=cc,alpha=0.7,label=ll,density=True)
    plt.xlabel("Temperature")
    plt.ylabel("Density")

    plt.tight_layout(0.1,0.1,0.1)
    if show:
        plt.show()
    else:    
        plt.savefig('fig/rgc_{}.pdf'.format(group_name[:4]),bbox_inches='tight',pad_inches=0)
    plt.close()

if __name__ == '__main__':
    for r in GOR_CLASSES:
        stats_species_gors(**r)
        plot_species_gor_histo(**r)