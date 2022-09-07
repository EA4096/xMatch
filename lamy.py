#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy.stats import chi2
import numpy as np
import joblib

def position_test(row, conf_level):
    
    q = chi2(df = 2).ppf(conf_level)
    
    a1 = np.array((row['RA1'], row['DE1']),dtype = float)
    a2 = np.array((row['RA2'], row['DE2']),dtype = float)
    
    d = row['sep']/3600

    Vm1 = np.array(([(float(row['e_RA1'])/3600)**2, 0],
                  [0, (float(row['e_DE1'])/3600)**2]))
    
    Vm2 = np.array(([(float(row['e_RA2'])/3600)**2, 0],
                  [0, (float(row['e_DE2'])/3600)**2]))
    
    if a2[0] - a1[0] < 0:
        theta = np.pi + np.arctan((a2[1] - a1[1])/(a2[0] - a1[0]))
        
    else:
        theta = np.arctan((a2[1] - a1[1])/(a2[0] - a1[0]))
    
    R = np.array(([np.cos(theta), np.sin(theta)],
                  [-np.sin(theta), np.cos(theta)]))
    
    R_inv = np.array(([np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]))
    
    Vm1_n = R@Vm1@R_inv
    Vm2_n = R@Vm2@R_inv
    Vc = Vm1_n + Vm2_n
    
    rho_c = Vc[0][1]/np.sqrt(Vc[0][0]*Vc[1][1])
    statistic = d/(np.sqrt(Vc[0][0]*(1 - rho_c**2)))
    
    return statistic < np.sqrt(q)


def photometry_test(row, obs_name):
    
    loaded_model = joblib.load(obs_name + '.save')
    
    try:
        res = bool(loaded_model.predict(np.array(row[['r1', 'e_r1', 'r2', 'e_r2']].astype(float)).reshape(1, -1))[0])
        
    except ValueError:
        res = np.nan
        
    return res


def separation(row):
    
    ra1 = np.deg2rad(float(row['RA1']))
    dec1 = np.deg2rad(float(row['DE1']))
    ra2 = np.deg2rad(float(row['RA2']))
    dec2 = np.deg2rad(float(row['DE2']))

    a = np.sin(np.abs(dec1 - dec2)/2)**2
    b = np.cos(dec1)*np.cos(dec2)*np.sin(np.abs(ra1 - ra2)/2)**2
    
    angle = 2*np.arcsin(np.sqrt(a + b))
    
    return np.degrees(angle)*3600



