from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import scipy
#from scipy.integrate import simps
import xraylib

density_dict = {'H2O': 0.992,
             'Al': 2.7,
             'SiO2': 2.32,
             'CaF2': 3.18,
             'V2A' : 7.8,            # V2A  0.05% C, 18% Cr, 10% Ni, 71.95% Fe
             'Cu' : 8.96,
             'Mo' : 10.22,
             'Be' : 1.85,
             'Polycarbonate' : 1.20,  # Polycarbonate 5.5% H, 75.5 % C, 20% O
             'Si' : 2.329,
             'Adipose' : 0.95,          # Adipose Tissue nist gov 0.95
             'Formaldehyde':0.8153,
             'Au': 19.3
             }

def calculate_quantum_efficiency(spectrum_energies, filter, sensor_thickness):
    '''
    Calculate the quantum efficiency weighted of the spectrum
    Filter is a String like 'Si'
    sensor thickness is in mm
    energy in keV
    '''
    energy, mu_rho = loadtxt(BASEPATH+filter+'_XMuDat.dat', unpack=True, usecols=[0,1])
    mu = mu_rho*density_dict[filter]
    interpolated_mu = interpolate.InterpolatedUnivariateSpline(energy,mu)
    new_mu = interpolated_mu(spectrum_energies)
    return 1 - np.exp(-new_mu*sensor_thickness*.1)

# energy, mu_rho = loadtxt('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/Mo_XMuDat_2.dat',unpack=True, usecols=[0,1])
#
# plt.figure()
# plt.title('Att H2O')
# plt.plot(energy, np.log(mu_rho) )
# plt.xlabel('energy in keV')
# plt.ylabel('mass attenuation coefficient')
# plt.show()
#
# save_data = np.array([energy, mu_rho])
# np.save('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_Mo.npy', save_data)
test = np.load('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_H2O.npy')
#data = loadtxt('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/W50kVpSiemens.dat')

energy = np.zeros(np.array(len(data)))
intensity = np.zeros(np.array(len(data)))
for i in range(len(data)):
    energy[i] = data[i, 0]
    intensity[i] = data[i, 1]

save_data = np.array([energy, intensity])
np.save('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/W_50kVp.npy', save_data)

test = np.load('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/W_140kVp.npy')

# Begin exercise
base_path = '/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/' ### Ubuntu
base_path = 'C:/Users/Lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/' ### Windows
name = 'W_140kVp'
energy, intensity = np.load(base_path + name + '.npy')

name = 'W_120kVp'
energy_120, intensity_120 = np.load(base_path + name + '.npy')

name = 'W_100kVp'
energy_100, intensity_100 = np.load(base_path + name + '.npy')

name = 'W_90kVp'
energy_90, intensity_90 = np.load(base_path + name + '.npy')

name = 'W_80kVp'
energy_80, intensity_80 = np.load(base_path + name + '.npy')

name = 'Mo_40kVp'
energy_40, intensity_40 = np.load(base_path + name + '.npy')

plt.figure()
plt.title('Tungsten up to 140 kVp')
plt.plot(energy, intensity, energy_80, intensity_80, energy_100, intensity_100, energy_120, intensity_120)
plt.xlabel('energy in keV')
plt.ylabel('intensity')
plt.show()

plt.figure()
plt.title('CT vs Mammography, both unfiltered')
plt.plot(energy_40, intensity_40, energy_120, intensity_120)
plt.xlabel('energy in keV')
plt.ylabel('intensity')
plt.show()

# Which part of spectrum is dominated by which effect? PE Compton equality?

#Z = 13 # Mo:42, W: 74, Al: 13, Cu: 29
filter_thickness = 20 # in cm
#energy,mu= np.load('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_H2O.npy') 
energy,mu= np.load('C:/Users/Lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_H2O.npy') ### Windows
mu *= density_dict["H2O"]
interpolated_mu = interpolate.InterpolatedUnivariateSpline(energy,mu)
new_mu_h2o = interpolated_mu(energy_120)
# plt.figure()
# plt.title('Att H2O')
# plt.plot(energy_120, np.log(new_mu) )
# plt.xlabel('energy in keV')
# plt.ylabel('mass attenuation coefficient')
# plt.show()
filtered_spectrum_h2o = intensity_120*(np.exp(-new_mu_h2o*filter_thickness))

# Filtration
# One common filtration is one mm Al (Z = 13). Apply this to the 120 kVp W spectrum.
# What percentage of the spectrum is left?
ratio = np.sum(filtered_spectrum_h2o)/np.sum(intensity_120)
print(ratio)

filter_thickness_al = 1 # in cm
#energy,mu= np.load('/home/lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_Al.npy')
energy,mu= np.load('C:/Users/Lorenz/Dropbox/Aktuelles/XrayCTexercises/spectrum/mu_rho_Al.npy')
mu *= density_dict["Al"]
interpolated_mu = interpolate.InterpolatedUnivariateSpline(energy,mu)
mu_al = interpolated_mu(energy_120)
filtered_spectrum = intensity_120*(np.exp(-mu_al*filter_thickness))
filtered_spectrum_al_h2o = filtered_spectrum_h2o * (np.exp(-mu_al*filter_thickness_al))
ratio = np.sum(filtered_spectrum)/np.sum(intensity_120)
print(ratio)



plt.figure()
plt.title('CT raw and Al ')
plt.plot(energy_120, intensity_120, label='120 kVp raw')
plt.plot(energy_120, filtered_spectrum, label='120 kVp + Al')
plt.plot(energy_120, filtered_spectrum_h2o, label='120 kVp + 20cm H2o')
plt.plot(energy_120, filtered_spectrum_h2o, label='120 kVp + 20cm H2o + Al')
plt.xlabel('energy in keV')
plt.ylabel('intensity')
plt.legend()
plt.show()


plt.figure()
plt.title('CT raw and Al ')
plt.plot(energy_120, intensity_120/np.max(intensity_120), label='120 kVp raw')
plt.plot(energy_120, filtered_spectrum/np.max(filtered_spectrum), label='120 kVp + Al')
plt.plot(energy_120, filtered_spectrum_h2o/np.max(filtered_spectrum_h2o), label='120 kVp + 20cm H2o')
plt.plot(energy_120, filtered_spectrum_al_h2o/np.max(filtered_spectrum_al_h2o), label='120 kVp + 20cm H2o + Al')
plt.xlabel('energy in keV')
plt.ylabel('intensity')
plt.legend()
plt.show()




plt.figure()
plt.title('CT native and with 1mm Al')
plt.plot(energy_120, intensity_120)
plt.xlabel('energy in keV')
plt.ylabel('intensity')
plt.show()

# Filter additionally the Mo with 1 mm Rh (Z = 45) or 1 mm Mo (Z = 42)

# Compare a raw spectrum of 40 kVp Mo and the 1 mm Mo filtered 40 kVp Mo spectrum of 20 cm water.




