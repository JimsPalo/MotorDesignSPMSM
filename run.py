'''
Created on Apr 21, 2021

@author: Jimmy Palomino

Main routine
'''

import matplotlib.pyplot as plt

from Main.main import main
from ANSYSDesign.MainOperations.OpenAnsoft import OpenAnsoft
from ANSYSDesign.Materials.MagnetMaterial import MagnetMaterial

from ANSYSDesign.Materials.StatorMaterial import StatorMaterial
from PreProcessing.WindingLayout import WindingLayout
from PreProcessing.GeometricParameters import GeometricParameters
from ANSYSDesign.MainOperations.LoadDesignVariables import LoadDesignVariables
from ANSYSDesign.Model.StatorDesign import StatorDesign
from ANSYSDesign.Model.RotorAndMagnetsDesign import RotorAndMagnetsDesign
from ANSYSDesign.Model.PMCharacterization import PMCharacterization
from ANSYSDesign.Model.Region import Region

from ANSYSDesign.Model.WindingDesign import WindingDesign
from ANSYSDesign.Model.BundlingCoils import BundlingCoils

from ANSYSDesign.Model.Band import Band
from ANSYSDesign.MeshMachine.MeshMachine import MeshMachine
from ANSYSDesign.AnalysisSetup.AnalysisSetup import AnalysisSetup
 

# Specifications Parameters predefined (mm, rpm, kW)
Specifications = {
    'Qs': 16,
    'Poles': 12,
    'DiaYoke': 400,
    'Length': 300,
    'RatedPower': 60e3,
    'Speed': 2500,
    'VDC': 400,
    'J': 7.5
}

main['ANSYS']['Specifications'] = Specifications

OpenAnsoft(main) and\
    MagnetMaterial(main) and\
    StatorMaterial(main) and\
    WindingLayout(main) and\
    GeometricParameters(main) and\
    LoadDesignVariables(main) and\
    StatorDesign(main) and\
    RotorAndMagnetsDesign(main) and\
    PMCharacterization(main) and\
    WindingDesign(main) and\
    BundlingCoils(main) and\
    Region(main) and\
    Band(main) and\
    MeshMachine(main) and\
    AnalysisSetup(main)


plt.show()