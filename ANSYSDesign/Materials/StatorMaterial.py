'''
Created on Apr 24, 2021

@author: Jimmy Palomino
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def StatorMaterial(main):
    """This function adds the stator material

    Args:
        main (Dic): Main dictionary used to upload the information

    Returns:
        Dic: Same unmodified main dictionary.
    """

    # oDefinitionManager
    oDefinitionManager = main['ANSYS']['Materials']['oDefinitionManager']

    # Material Name
    StatorMaterialName = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialBHCurve.csv',
                                    dtype='str', skiprows=2, usecols=1, unpack=True, delimiter=',', max_rows=1)
    # BH curve
    H, B = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialBHCurve.csv',
                      skiprows=5, unpack=True, delimiter=',')

    # Core Losses Curves
    # frequencies
    frequencies = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialCoreLosses.csv',
                             dtype='str', skiprows=7, unpack=True, delimiter=',', max_rows=1)
    frequencies = frequencies[1:]

    # Curves
    CoreLoss = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialCoreLosses.csv',
                          skiprows=9, unpack=True, delimiter=',')

    # Units
    Units = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialCoreLosses.csv',
                       dtype='str', skiprows=4, usecols=1, unpack=True, delimiter=',', max_rows=1)
    Units = str(Units).split('/')

    # Mass density in kg/m^3
    MassDensity = np.loadtxt('ANSYSDesign\\Materials\\StatorMaterialCoreLosses.csv',
                             skiprows=5, usecols=1, unpack=True, delimiter=',', max_rows=1)

    # Generation the argument for the Corelosses
    InitialCurve = ["NAME:AllCurves"]
    for freq in frequencies:

        points = ["NAME:Points"]
        for i, k in enumerate(CoreLoss[0, :]):
            points.append(k),
            points.append(CoreLoss[1, i])

        ForFreq = [
            "NAME:OneCurve",
            "Frequency:=", freq+"Hz",
            [
                "NAME:Coordinates",
                [
                    "NAME:DimUnits",
                    "",
                    ""
                ],
                points
            ]
        ]
        InitialCurve.append(ForFreq)

    # Generation of the data for the BH curve
    InitialCurveBH = ["NAME:BHCoordinates", ["NAME:DimUnits",  "", ""]]
    for i, h in enumerate(H):
        InitialCurveBH.append(["NAME:Point", h, B[i]])

    # Uploading in Ansoft
    oDefinitionManager.AddMaterial(
        [
            "NAME:"+str(StatorMaterialName),
            "CoordinateSystemType:=", "Cartesian",
            "BulkOrSurfaceType:=", 1,
            [
                "NAME:PhysicsTypes",
                "set:=", ["Electromagnetic"]
            ],
            [
                "NAME:AttachedData",
                [
                    "NAME:CoreLossMultiCurveData",
                    "property_data:=", "coreloss_multi_curve_data",
                    "coreloss_unit:=", Units[0]+"_per_"+Units[1],
                    InitialCurve
                ]
            ],
            [
                "NAME:permeability",
                "property_type:=", "nonlinear",
                "BTypeForSingleCurve:=", "normal",
                "HUnit:=", "A_per_meter",
                "BUnit:=", "tesla",
                "IsTemperatureDependent:=", False,
                InitialCurveBH,
                [
                    "NAME:Temperatures"
                ]
            ],
            [
                "NAME:magnetic_coercivity",
                "property_type:=", "VectorProperty",
                "Magnitude:=", "0A_per_meter",
                "DirComp1:=", "1",
                "DirComp2:=", "0",
                "DirComp3:=", "0"
            ],
            [
                "NAME:core_loss_type",
                "property_type:=", "ChoiceProperty",
                "Choice:=", "Electrical Steel"
            ],
            "core_loss_kh:=", "184.233670546732",
            "core_loss_kc:=", "0.386260592696451",
            "core_loss_ke:=", "0.270231418332487",
            "core_loss_kdc:=", "0",
            "mass_density:=", str(MassDensity),
            "core_loss_equiv_cut_depth:=", "0.001meter"
        ]
    )

    # B-H Curve Interpolation----------------------------------------------------------------
    # Transforming en kA/m
    H = H/1000

    # Redefining useful range
    # Here considerer as maximum a slop of 10 degrees
    BHslop = (B[1:]-B[:-1])/((H[1:]-H[:-1]))-np.tan(np.pi*2.5/180)

    HUseful = H[:-1][BHslop > 0.]
    BUseful = B[:-1][BHslop > 0.]

    # Interpolation using cubic spline
    p = interp1d(HUseful, BUseful, kind='cubic')
    p2 = interp1d(BUseful, HUseful, kind='cubic')

    # Supersamplig the BH curve
    Hnew = np.linspace(min(HUseful), max(HUseful), 10000)
    Bnew = p(Hnew)

    # Knee point finding
    slop = (Bnew[1:]-Bnew[:-1])/((Hnew[1:]-Hnew[:-1]))-np.tan(45/180*np.pi)
    HKnee = np.mean(Hnew[:-1][np.abs(slop) < 0.01])

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(Hnew, Bnew, 'k', label='B-H Curve interp.')
    ax.plot(HKnee, p(HKnee), 'x', label='Knee point')
    ax.scatter(H, B, label='Data Points')

    # Figure labeling
    ax.legend(loc='lower right')
    ax.set_xlim(min(HUseful), max(HUseful))
    ax.set_ylim(min(BUseful), max(BUseful))
    ax.set_ylabel(r'$B [T]$', fontsize=18)
    ax.set_xlabel(r'$H [kA/m]$', fontsize=18)
    # plt.show()

    # Saving in main object
    StatorMaterial = {}
    StatorMaterial['StatorMaterialName'] = StatorMaterialName
    # Saving the BH Curve ans HB Curve
    StatorMaterial['BHCurve'] = [p, p2]
    StatorMaterial['KneePoint'] = [HKnee, p(HKnee)]
    StatorMaterial['MassDensity'] = MassDensity

    main['ANSYS']['Materials']['Stator'] = StatorMaterial

    return main
