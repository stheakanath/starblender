starblender
===========

starblender consists of multiple programs used in the study of NGC 4449 (case study done here: http://sonytheakanath.com/downloads/Dwarf-Dwarf_Cannibalism_SONY.pdf). We have used Keck/DEIMOS to conduct the first detailed spectroscopic study of the recently discovered stellar stream in the Large Magellanic Cloud analog NGC 4449. Martinez- Delgado et al. (2012), using the tip of the red giant branch (TRGB), found that both objects, the stream and NGC 4449, are at the same distance, which suggests that this stream is the remnant of the first ongoing dwarf-dwarf cannibalism event known so far. Information about the orbital properties of this event is a powerful tool to constrain the physical conditions involved in dwarf- dwarf merger events. The low surface-brightness of this structure makes it impossible to obtain integrated light spectroscopic measurements, and its distance (3.8 Mpc) is too large to observe stars individually. 

This is where starblender comes in. I designed a a novel method that extends star spectroscopy to farther distances. This program collection won Intel STS and Siemens Science Competitions. 

Why Open Source?
---------------

I want future astrophysicists to use this program, make it more efficient and use it for their own research, because research is a team oriented activity. 

How to Use
---------------

You'll need to have IDL in order to do the server side work, in addition to your SLIT Z-SPEC files, for program analysis. 

Main Program Details
---------------

- __ColorMagnitude_ZQualities.py__ Prints the Z-Qualities from -2 to 4 on a graph for analysis. See Siemens paper above. 
- __Distance_Velocity.py__ Runs a simulation of the Distance vs Velocity over time. 
- __FITStablesheadersreader.py__ Converts the FITS raw file for analysis. 
- __coaddition.pro__ Coadds the starts for larger star magnitude (Key algorithm invented). 
- __coaddition.py__ Python version of above program.

Other programs are used for FITS and Z-SPEC file handling/setup for coaddition and star blending. 
