'''
Created on Jun 23, 2021

@author: Jimmy Palomino
'''
import numpy as np


def BundlingCoils(main):

    oDesign = main['ANSYS']['oDesign']

    # Changing the solution type
    oDesign.SetSolutionType("Transient", "XY")

    # Coil Names defintion
    CoilNames = main['ANSYS']['Winding']['CoilNames']

    # Importing oModule
    oModule = oDesign.GetModule("BoundarySetup")

    Nph = main['ANSYS']['FixedVariables']['Nph']

    # Coil number
    CoilNumber = len(CoilNames[0][0])

    # CoilTurns = int(Nph/CoilNumber)
    CoilTurns = 2

    # Branches number
    Branches = main['ANSYS']['FixedVariables']['Branches']

    # Poles number
    Poles = main['ANSYS']['FixedVariables']['Poles']

    # Input Coils Names
    InputCoils = CoilNames[0][0] + CoilNames[1][0] + CoilNames[2][1]

    # Ouput Coils Names
    OuputCoils = CoilNames[0][1] + CoilNames[1][1] + CoilNames[2][0]

    oModule.AssignCoilGroup(
        InputCoils,
        [
            "NAME:AIn7",
            "Objects:="		, InputCoils,
            "Conductor number:="	, str(CoilTurns),
            "PolarityType:="	, "Positive"
        ]
    )

    oModule.AssignCoilGroup(
        OuputCoils,
        [
            "NAME:AOut6",
            "Objects:="		, OuputCoils,
            "Conductor number:="	, str(CoilTurns),
            "PolarityType:="	, "Negative"
        ]
    )

    # Omega
    Omega = 'RotSpeed*'+str(1/60*np.pi*Poles)

    # Current definition
    PhaseA = 'Iph*sqrt(2)*sin('+Omega+'*time + Pf)'
    PhaseB = 'Iph*sqrt(2)*sin('+Omega+'*time + Pf - 2*pi/3)'
    PhaseC = 'Iph*sqrt(2)*sin('+Omega+'*time + Pf - 4*pi/3)'

    # Winding creation A
    oModule.AssignWindingGroup(
        [
            "NAME:PhaseA",
            "Type:="		, "Current",
            "IsSolid:="		, False,
            "Current:="		, PhaseA,
            "Resistance:="		, "0ohm",
            "Inductance:="		, "0nH",
            "Voltage:="		, "0mV",
            "ParallelBranchesNum:="	, Branches
        ]
    )

    # Add the coils to the winding Phase A
    oModule.AddWindingCoils("PhaseA", CoilNames[0][0] + CoilNames[0][1])

    # Winding creation B
    oModule.AssignWindingGroup(
        [
            "NAME:PhaseB",
            "Type:="		, "Current",
            "IsSolid:="		, False,
            "Current:="		, PhaseB,
            "Resistance:="		, "0ohm",
            "Inductance:="		, "0nH",
            "Voltage:="		, "0mV",
            "ParallelBranchesNum:="	, Branches
        ]
    )

    # Add the coils to the winding Phase B
    oModule.AddWindingCoils("PhaseB", CoilNames[1][0] + CoilNames[1][1])

    # Winding creation C
    oModule.AssignWindingGroup(
        [
            "NAME:PhaseC",
            "Type:="		, "Current",
            "IsSolid:="		, False,
            "Current:="		, PhaseC,
            "Resistance:="		, "0ohm",
            "Inductance:="		, "0nH",
            "Voltage:="		, "0mV",
            "ParallelBranchesNum:="	, Branches
        ]
    )

    # Add the coils to the winding Phase C
    oModule.AddWindingCoils("PhaseC", CoilNames[2][0] + CoilNames[2][1])

    main['ANSYS']['FixedVariables']['CoilTurns'] = CoilTurns

    return main
