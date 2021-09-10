'''
Created on Apr 21, 2021

@author: Jimmy Palomino

Definiton of the main object - The Heart of the program
'''

main = {
    'ANSYS':
        {
            # Application object and desktop
            'oAnsoftApp': [],
            'oDesktop': [],

            # Project object
            'ProjectName': 'MachineDesign',
            'oProject': [],

            # Materials definition
            'Materials': {
                'oDefinitionManager': [],

                # Stator&Rotor material
                'Stator': {
                    'StatorMaterialName': [],
                    # BH curve in T vs kA/m and HB Curve [BH, HB]
                    'BHCurve': [],
                    # Knee point Hknee and Bknee
                    'KneePoint': [],
                    # MasDensity in kg/m3
                    'MassDensity': []
                },

                # Magnet material
                'PM': {
                    # The name consist in a arrange of two
                    'PMName': 'SmCo24_MachineDesign',
                    # Relative permeability
                    'Permeability': 1.06314,
                    # Conductivity en sims/m
                    'conductivity': 1111110,
                    # Coercivity Magnitucde Vector in A*m
                    'CoercivityMagnitude': -920000,
                    # Mass Density in kg/m3
                    'MassDensity': 8300
                }
            },

            # Specifications
            'Specifications': {
                'Qs': [],
                'Poles': [],
                'DiaYoke': [],
                'Length': [],
                'RatedPower': [],
                'Speed': [],
                'VDC': [],
                'J': []
            },

            # Design Object
            'oDesign': [],
            'oEditor': [],
            'DesignName': 'DynamicAnalysis',

            # Geometric Parameters Definition
            'DesignProperties': {
                'Stator': {
                    'g': [],
                    'DiaYoke': [],
                    'lenght': [],
                },
                'Slot': {
                    'Hs0': [],
                    'Hs1': [],
                    'Hs2': [],
                    'Bs0': [],
                    'Bs1': [],
                    'Bs2': [],
                    'Rs': 5
                },
                'Rotor': {
                    'DiaGap': [],
                    'DiaYokeR': [],
                    'Embrace': [],
                    'ThickMag': [],
                    'Speed': [],
                },
                'Electric': {
                    'Iph': [],
                    'Pf': [],
                    'InitialPosition': [],
                }
            },

            # Fixes Variables
            'FixedVariables': {
                'Slots': [],
                # Two possibilities 3 or 4
                'SlotType': 3,
                # Poles number
                'Poles': [],
                # Total turns
                'Nph': [],
                # Rated Current
                'Iph': [],
                # Turns in one coil
                'CoilTurns': [],
                # Branch number
                'Branches': 1,
            },

            # Winding Design
            'Winding': {
                # Coil Names
                'CoilNames': [],
                # Slots for every phase
                'ABC': [],
                # Winding factor
                'kw': [],
                # Phases color definition (ABC)
                'Color': [
                    [255, 133, 0],
                    [50, 0, 158],
                    [21, 228, 109]
                ]
            },

            # Stator Data
            'Stator': {
                'Name': 'Stator',
                'Color': (143, 159, 175)
            },

            # Rotor and Magnets Data
            'Rotor&Magnets': {
                'Name': ['Rotor', 'Magnets'],
                'Color': [(0, 255, 0), (255, 0, 0)],
                'PMNames': []
            },

            'Region': {
                'RegionName': 'Region',
                'OffsetPercent': 10
            },

            'Mesh': {
                'Rotor': {
                    # Mesh lenght based (mm)
                    'NumMaxElem': 1000,
                    'MaxLength': 5
                },
                'Magnets': {
                    # Mesh lenght based (mm)
                    'NumMaxElem': 1000,
                    'MaxLength': 5
                },
                'Stator': {
                    # Meah surface based (deg)
                    'NormalDev': 15,
                    'AspectRatio': 5
                },
                'Winding': {
                    # Mesh lenght based (mm)
                    'NumMaxElem': 1000,
                    'MaxLength': 4
                },
            },

            # Setting the No-load Solution
            'AnalysisSetup': {
                'Multiplier': 1,
                'oModule': [],
                'Name': 'DynamicAnalysis',
                'PercentError': 0.1,
                'RefinementPerPass': 15,  # percent
                'NonLinearResidual': 0.0001
            },
            'Report': {
                'oModule': [],
                'FluxDensity': {
                    'Name': 'StaticAnalysisBPlot'
                }
            },
            'Design2': {
                'Design_Name': 'LoadAnalysis',
                'oDesign': [],
                'oEditor': [],
                'Winding': {
                    # Coil Names
                    'CoilNames': [],
                    # Slots for every phase
                    'ABC': [],
                    # Winding factor
                    'kw': [],
                    # Phases color definition (ABC)
                    'Color': [
                        [255, 133, 0],
                        [50, 0, 158],
                        [21, 228, 109]]
                }
            },

            # Dynamic Analysis
            'Design3': {
                'Design_Name': 'DynamicAnalysis',
                'oDesign': [],
                'oEditor': [],
                'Winding': {
                    # Coil Names
                    'CoilNames': [],
                    # Slots for every phase
                    'ABC': [],
                    # Winding factor
                    'kw': [],
                    # Phases color definition (ABC)
                    'Color': [
                        [255, 133, 0],
                        [50, 0, 158],
                        [21, 228, 109]]
                }
            }
        }
}
