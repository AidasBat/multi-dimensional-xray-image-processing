import sys
sys.path.append('/users/Berthe/01_Scripts/RotatingAnode/PCDSimulationtool/')
import numpy as np
from tube_source import *
from detector import *
import os

#sampling of the spectrum
e_sampling = 1.0
#define which kVp should be simulated
minSimEnergy = 15
maxSimEnergy = 150
#where should it be saved
savePath = "/users/Berthe/01_Scripts/RotatingAnode/PCDSimulationtool/xraySpectra/"

#generate array with all kVp
simulationEnergies = np.arange(minSimEnergy, maxSimEnergy+1)

#generate txt file with all spectra
for E in simulationEnergies:
    #generate spectrum (with W target)
    spectrum = t = tubeSource(anode_material='W', kVp=E, beam_filter_material='Al', beam_filter_thickness=0.0, mAs=100., spectral_sampling=e_sampling)
    #extract spectrum from function
    energies = np.arange(0, E+1, e_sampling)
    intensity = t.get_spectrum().astype(np.float32)
    data = np.array([energies, intensity])
    #save as txt 
    np.save(savePath + str("W_") + str(E) + str("kVp"), data, allow_pickle = False)

#used by the students to load all spectra 
def generate_Spectrum(kVp):
   if os.path.exists(savePath + str("W_") + str(kVp) + str("kVp.npy")):
       spectrum = np.load(savePath + str("W_") + str(kVp) + str("kVp.npy"), allow_pickle = True)
       return spectrum
   else: print("Spectrum doesnt exist under the path" + savePath + str("W_") + str(kVp) + str("kVp.npy"))


