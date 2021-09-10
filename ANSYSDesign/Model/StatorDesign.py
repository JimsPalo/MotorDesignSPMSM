'''
Created on Apr 21, 2021

@author: Jimmy Palomino
'''


def StatorDesign(main):
    """Stator design in ANSYS Electronics
    Input:
        main (Dic): Main dictionary used to upload the design information.

    Returns:
        Dic: The same unmodified main object.
    """

    # oEditor definition
    oEditor = main['ANSYS']['oEditor']

    # Stator dictionary definition
    Stator = main['ANSYS']['Stator']

    # Stator material Name
    StatorMaterialName = main['ANSYS']['Materials']['Stator']['StatorMaterialName']

    # Slots number
    Slots = main['ANSYS']['FixedVariables']['Slots']

    #SlotType
    SlotType = main['ANSYS']['FixedVariables']['SlotType']

    # Part definition
    oEditor.CreateUserDefinedPart(
        [
            "NAME:UserDefinedPrimitiveParameters",
            "DllName:=", "RMxprt/SlotCore.dll",
            "Version:=", "12.1",
            "NoOfParameters:=", 19,
            "Library:=", "syslib",
            [
                "NAME:ParamVector",
                [
                    "NAME:Pair",
                    "Name:=", "DiaGap",
                    "Value:=", "DiaGap + g*2"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "DiaYoke",
                    "Value:=", "DiaYoke"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Length",
                    "Value:=", "0mm"  # Doesn't matter in 2D
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Skew",
                    "Value:=", "0deg"  # Doesn't matter in 2D
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Slots",
                    "Value:=", str(int(Slots))
                ],
                [
                    "NAME:Pair",
                    "Name:=", "SlotType",
                    "Value:=", str(int(SlotType))
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Hs0",
                    "Value:=", "Hs0"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Hs01",
                    "Value:=", "0mm"  # Do not defined
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Hs1",
                    "Value:=", "Hs1"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Hs2",
                    "Value:=", "Hs2"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Bs0",
                    "Value:=", "Bs0"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Bs1",
                    "Value:=", "Bs1"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Bs2",
                    "Value:=", "Bs2"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "Rs",
                    "Value:=", "Rs"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "FilletType",
                    "Value:=", '0'
                ],
                [
                    "NAME:Pair",
                    "Name:=", "HalfSlot",
                    "Value:=", "0"  # Symmetry slot
                ],
                [
                    "NAME:Pair",
                    "Name:=", "SegAngle",
                    "Value:=", "15deg"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "LenRegion",
                    "Value:=",  "200mm"
                ],
                [
                    "NAME:Pair",
                    "Name:=", "InfoCore",
                    "Value:=", "0"  # Considering a core
                ]
            ]
        ],
        [
            "NAME:Attributes",
            "Name:=", Stator['Name'],
            "Flags:=", "",
            "Color:=", str(Stator['Color']).replace(',', ' '),
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:=", "",
            "MaterialValue:=",  "\"vacuum\"".replace(
                'vacuum', str(StatorMaterialName)),
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:=", True,
            "ShellElement:=", False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:=", True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:=", False
        ])

    # Fit the main screen
    oEditor.FitAll()

    return main
