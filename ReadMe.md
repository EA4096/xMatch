# <center> <b>Cross-matching methods in the problem of search and identification of transient objects </b>

Data on observed astronomical objects is usually stored in so-called astronomical catalogs. These catalogs can be imagined as very big tables, containing millions of rows, where each row represents a patricular source. Columns of such a table define parameters of observed source: coordinates, positional errors, proper motion, time of observation, results of photometry and other properties of an object. Very often, studing a particular source through the first catalog, we may want to find this object in another catalog, for instance, to trace it's evolution in time. In order to do this, we will launch a cross-matching procedure, which, in general, involves searching second catalogue for a counterpart for each object from the first catalogue. It's obviuos that counterparts must be located closely and have similar parameters of brighness, but even this task have it's own caveats and it results in rich diversity of cross-matching methods, used in astronomy and astrophysics. This problem becomes even more complicated if we look for a short-living (transient) object (for example, an optical afterglow of a gamma ray burst), which appears in the sky for a short time and soon fade away. Of course, such event won't be recorded in catalogs, created in previous observations, so it must find it's counterpart NOT, when proceeding xmatch with other catalogs. This project is designed as a possible solution for the problem of identification of transients in astronomical images via xmatch with external catalogs.

# <u>Formulation of the problem</u>
Using the given catalog C1 as input, perform its cross-matching with already existing catalogs C2, C3, ..., Cn based on all the available parameters and return the list of candidate transients. For this problem cross-matching methods <u>must be implemented</u> and then used in our routine processing of the astronomical images. Altough, the on-sky separation cross-matching method is provided here for example.

## <u>Requirements</u>
* A catalog C1 will be passed in as an Sqlite database where objects listed in the 'objects' table and their standardized fields (i.e. they are always presented) are following:
    * id -- an object's id based on sorted right ascension
    * x -- the centroid position in the image
    * x_xerr
    * y
    * y_yerr
    * ra -- the centroid position in the sky (both in the form of HH MM SS.SSS for RA and DD MM SS for dec and degrees)
    * ra_err
    * dec
    * dec_err
    * ra_deg
    * dec_deg
    * inst_mag -- an instrumental magnitude
    * inst_mag_err
    * mag -- an apparent magnitude
    * mag_err
    * fwhm_x -- an FWHM in both directions
    * fwhm_x_err
    * fwhm_y
    * fwhm_y_err
    * catalog -- the catalog name
    * catid -- the catalog ID
* For a start use astroquery to find available catalogs, but in the future APEX catalog readers should be used (??)
* Use this predefined list of catalogs:
    * PanSTARRS PS1/2
    * USNO-B1.0
    * GAIA DR2/EDR3
    * SDSS DR9 -- DR16
    * GALEX
    * Skymapper
    * Tycho2
    * Hipparcos
    * Minor Planet Center (possibly, but it seems very relevant)
* Return a list of transient canidates in the form of a table or a list of catalog objects (like in APEX)
* Additionally, there is also must be a possibility for cross-matching the two catalogs, obtained from processing of two images in order to:
    * Find the objects that are absent in one of the two images, but are presented in the other one
    * Or detect the significantly brightened objects that are presented in both images

Database of astronomical papers <a href="https://adsabs.harvard.edu">ADS</a>  may be used to find necessery information about cross-matching methods. Be cautious that all these catalogs mentioned earlier might have a different set of fields (e.g. GAIA has some unique fields which are not present in the other catalogs), so take it into account to boost performance of the appropriate cross-matching methods. Note, that before the field identification and further cross-matching <i>one can not compute the apparent magnitudes, using the differetial photometry</i>.

# <b>GOOD LUCK =)</b>

## Files

<u>catalogs.db</u> - database, containing two tables and simulating a big local database, which provides acess to astronomical catalogs appropriate for xmatch. This one contains two small slices of 6x6 squared degrees fields of PS1 and SDSS DR12 catalogs.

<u>test.db</u> - database, containing objects, extracted from test.fits astronomical image using APEX software

<u>image_module.py</u> - module, designed for convenient fits-image preprocessing

<u>lamy.py</u> has three functions: <b>separation</b> calculates angular distance between two objects on celestial sphere,
<b>position_test</b> tests a hypothesis that two compared objects, located within the limits of their measurement errors are actually the same one (<a href="https://doi.org/10.1051/0004-6361/201015141">Details</a>, 3.1.1) and <b>photometry_test</b>, which loads trained in <u>model.ipynb</u> classificator (<u>Maidanak.save</u> - for now for Maidanak observatory R filter only)

<u>Final_comments.ipynb</u> represents an advanced and commented copy of ready-for-work <u>Final.ipynb</u> 

<u>Draft_comparison.ipynb</u> is unkommented and written for efficiency comparison of various xmatch methods (NN, , <a href=https://www.aanda.org/articles/aa/full_html/2017/11/aa30965-17/aa30965-17.html > ErrorEllipses</a>, <a href="https://arxiv.org/abs/1503.01184"> MatchEX</a>) in terms of precision and recall of xmatch procedure, which are also described in MatchEx paper 
 
<u>Draft_griz_best_model.ipynb</u> is also unkommented and was written for choosing the best match classificator when comparing objects with data avaliable on several photometric filters (g, r, i, z bands for PS1 and SDSS DR12 astronomical catalogs)
