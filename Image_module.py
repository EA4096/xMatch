#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from astropy.io import fits

class Image:
    
    def __init__(self, fname='', hdr={}, data=[]):
        self._fname = fname
        self.hdr = hdr
        self.data = data
    
    @property
    def width(self):
        try:
            return self.data.shape[0]
        except Exception as e:
            return 0
    
    @property
    def height(self):
        try:
            return self.data.shape[1]
        except:
            return 0
    
    @property
    def fname(self):
        return self._fname
    
    def __str__(self):
        return f"<Image {self.width}x{self.height}>"
    
    __repr__ = __str__
    
    
def imread(path):
    hdr, data = {}, []
    with fits.open(path, 'readonly', ignore_missing_end=True) as f:
        hdu = f[0]
        hdr = getattr(hdu, 'header', {})
        data = getattr(hdu, 'data', [])
        
    return Image(path, hdr=hdr, data=data)


def imsave(img, path=''):
    if path:
        fits.writeto(path, img.data, img.hdr, overwrite=True)
    else:
        fits.writeto(img.fname, img.data, img.hdr, overwrite=True)