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

Histograms for ROIs
"""

import matplotlib.pyplot as plt
import numpy as np
from thermal_utlis import get_name,get_animal_rois,INDICES,ATYPES,GLOBAL_SHOW
from scipy.stats import skew, kurtosis  

def get_roi_differences(rid):
    """
    returns (and prints) differences between animals in ROI
    parameters:
        rid: ROI id
    
    returns:
        dictionary of differences i.e. 
        {diff: roi difference,H:<horse roi stats>,D:<donkey roi stats>} 
    """
    temps = {}
    rets = {}
    for atype in ATYPES:
        temps[atype]=[]
        for i in INDICES:
            name = get_name(atype,i)
            rois = get_animal_rois(name)
            temps[atype].append(rois[rid-1])
        temps[atype] = np.concatenate(temps[atype])
        rmin,rmean,rmedian,rmax = np.min(temps[atype]),np.mean(temps[atype]),np.median(temps[atype]),np.max(temps[atype])
        rets[atype] = [rmin,rmean,rmedian,rmax]
    dd = np.abs(rets['H'][1]-rets['D'][1])
    print ("{}: {:0.2f}, {}".format(rid,dd,rets))
    rets['diff'] = dd    
    return rets    
                        
def count_rois_differences():
    """
    counts average differences between no. pixels in ROIs
    """
    h =[[len(l) for l in get_animal_rois(get_name('H',i))] for i in INDICES]
    d =[[len(l) for l in get_animal_rois(get_name('D',i))] for i in INDICES]
    h = np.sum(np.asarray(h),axis=0)
    d = np.sum(np.asarray(d),axis=0)
    diff = np.abs(h-d)
    print (100*np.mean([np.median(diff/h),np.median(diff/d)]))
    print ("average difference: {:0.2f}({:0.2f})".format(100*np.mean([np.mean(diff/h),np.mean(diff/d)]),100*np.mean([np.std(diff/h),np.std(diff/d)])))


def plot_roi_histo(rid,small=False,show=GLOBAL_SHOW):
    """
    plots hhistogram of temperatures for a given ROI
    parameters:
        rid - ROI id or 0 for all
        small - True/False: wheather to generate small (half-size) histograms
        show: True/False: show or save image
    """
    assert rid>=0 and rid<16,"{}".format(rid) 
    temps = {}
    for atype in ATYPES:
        temps[atype]=[]
        for i in INDICES:
            name = get_name(atype,i)
            rois = get_animal_rois(name)
            if rid>0:
                temps[atype].append(rois[rid-1])
            else:    
                temps[atype].append(np.concatenate(rois))
        temps[atype] = np.concatenate(temps[atype])
        print ("{} ROI {}: mean: {:0.2f}, std: {:0.2f}, skew:{:0.2f}, kurtosis:{:0.2f}".format(atype,rid
                                                                                               ,np.mean(temps[atype])
                                                                                               ,np.std(temps[atype])
                                                                                               ,skew(temps[atype])
                                                                                               ,kurtosis(temps[atype])))    

    if not small:
        plt.rcParams.update({'font.size': 12})
        plt.figure(figsize=(4,3),dpi=300)
    else:    
        plt.rcParams.update({'font.size': 10})
        plt.figure(figsize=(2,1.5),dpi=300)
    nbins = int(np.max([np.sqrt(len(temps[atype])) for atype in ['H','D']]))
    
    plt.hist(temps['H'],color='#DC3220',alpha=0.7,density=True,bins=nbins,label='Horses')
    plt.hist(temps['D'],color='#005AB5',alpha=0.7,density=True,bins=nbins,label='Donkeys')
    if not small:
        plt.xlabel("Temperature")
    else:
        txt="[ROI {}] Temp.".format(rid) if rid>0 else 'Combined Temp.'
        plt.xlabel(txt)
    plt.ylabel("Density")
    if not small:
        plt.legend()        
    plt.tight_layout(0.1,0.1,0.1)
    ss = '_small' if small else ''
    if show:
        plt.show()
    else:    
        plt.savefig('fig/histo_{}{}.pdf'.format(rid,ss),bbox_inches='tight',pad_inches=0)
    plt.close()
    
import sys 
if __name__ == '__main__':
    count_rois_differences()
    plot_roi_histo(0,small=True)
    for rid in range(1,16):
        plot_roi_histo(rid,small=True)
    imin=4
    imax=7
    if True:
        diffs = [get_roi_differences(rid)['diff'] for rid in range(1,16)]
        imin = np.argmin(diffs)+1
        imax = np.argmax(diffs)+1
        print (imin,imax)
    
    plot_roi_histo(rid=imin) 
    plot_roi_histo(rid=imax) 