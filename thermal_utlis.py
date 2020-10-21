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

data loading and basic utility functions
"""
import unittest
import numpy as np
from scipy.stats import mannwhitneyu


#a patch to your DS location
DS_DIR = 'hdthermal_dataset/'
 
#H for horses, D for donkeys
ATYPES = ['H','D']
#normal animals
INDICES = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#anomalies (donkeys)
ANOMALOUS_DONKEY_INDICES=[17,18]

#GORS
GOR_CLASSES = [{'roi_group':[1,2,3],'group_name':'Neck','short':'Neck'}
                     ,{'roi_group':[1,2,3,4,14,15],'group_name':'Frontquarter','short':'Front.'}
                     ,{'roi_group':[5,11],'group_name':'Trunk','short':'Trunk'}
                     ,{'roi_group':[6,7,8,9,10],'group_name':'Hindquarter','short':'Hind.'}
                     ,{'roi_group':[8,9],'group_name':'Rump','short':'Rump'}
                     ,{'roi_group':[3,4,5,6],'group_name':'Dorsal aspect','short':'Dors.'}
                     ,{'roi_group':[9,10,11,12,13],'group_name':'Ventral aspect','short':'Vent.'}
                     ,{'roi_group':[11],'group_name':'Abdomen','short':'Abdom.'}
                     ,{'roi_group':[10,12],'group_name':'Groins','short':'Groins'}
                     ,{'roi_group':[9,13],'group_name':'Legs','short':'Legs'}
                     ]

#global show(True) / savefig (False) switch
GLOBAL_SHOW = True


def get_animal(name):
    """
    returns data and annotation for the animal
    parameters:
        name: animal name (use get_name())
    
    returns:
        data: 2D array of thermal data
        anno: 2D array with class map 
    """
    arr = np.load("{}data/da_{}.npz".format(DS_DIR,name))
    return arr['data'],arr['gt']


def get_name(atype='H',index=1):
    """
    returns animal name
    parameters:
        atype: type of animal from ['H','D']
        index: animal index: 1..16 (1..18 for donkeys)
    
    returns:
        animal name
    """
    assert atype in ATYPES
    return '{}.{}'.format(atype,index)


def get_animal_rois(name):
    """
    returns list of ROIs for a given animal
    
    parameters: 
        name - animal name
    
    returns: 
        list of 15 ROIs
    
    """
    arr,anno = get_animal(name)
    res = []
    for c in range(1,16):
        res.append(arr[anno==c].tolist())
    return res

def mww_test(hot,cold,p=0.001,alternative='greater'):
    """
    wilcoxon test of statistical significance
    parameters:
        hot - 1st sequence
        cold - 2nd sequence
        p- required p
    """
    h = hot.copy()
    c = cold.copy()
    
    
    mm = np.min([len(h),len(c)])
    np.random.shuffle(h.copy())
    np.random.shuffle(c.copy())
    _,s_p = mannwhitneyu(h[:mm],c[:mm],alternative=alternative)
    return s_p<p

class Test(unittest.TestCase):
    def test_load(self):
        for i in INDICES:
                for atype in ATYPES:
                    aname = get_name(atype,i)
                    data,anno = get_animal(aname)
                    self.assertSequenceEqual(list(data.shape),list(anno.shape))
                    self.assertSequenceEqual(np.unique(anno).tolist(),np.arange(16).tolist())
                    rois = get_animal_rois(aname)
                    self.assertEqual(len(rois),15)
                    for roi in rois:
                        self.assertTrue(10<=np.mean(roi)<=35)
    def test_mww(self):
        o = np.random.rand(100)
        z = np.random.rand(100)*0.01
        self.assertTrue(mww_test(o,z,p=0.001))    
        self.assertFalse(mww_test(o,o,p=0.001))
        self.assertFalse(mww_test(z,o,p=0.001))                        
                    
                    
if __name__ == '__main__':
    unittest.main()
    