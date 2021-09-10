'''
Created on Apr 21, 2021

@author: Jimmy Palomino
'''


def RotorAndMagnetsDesign(main):
    """Definition of the rotor and magnets design on ANSYS.

    Args:
        main (Dic): Contains the parameters of the rotor and magnets design.

    Returns:
        Dic: The same input dont modified only is readed by the following lines.
    """

    # oEditor definition
    oEditor = main['ANSYS']['oEditor']

    # Stator and PM Names
    Names = main['ANSYS']['Rotor&Magnets']['Name']

    # Stator and rotor names
    Colors = main['ANSYS']['Rotor&Magnets']['Color']

    # Rotor material definition
    RotorMaterial = main['ANSYS']['Materials']['Stator']['StatorMaterialName']

    # Arrange material names
    material = [RotorMaterial, 'vacuum']

    # Poles
    Poles = main['ANSYS']['FixedVariables']['Poles']

    for k in range(2):
        # Part definition
        oEditor.CreateUserDefinedPart(
            [
                "NAME:UserDefinedPrimitiveParameters",
                "DllName:=", "RMxprt/PMCore.dll",
                "Version:=", "12.0",
                "NoOfParameters:=", 13,
                "Library:=", "syslib",
                [
                    "NAME:ParamVector",
                    [
                        "NAME:Pair",
                        "Name:=", "DiaGap",
                        "Value:=", "DiaGap"
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "DiaYoke",
                        "Value:=", 'DiaYokeR'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Length",
                        "Value:=", "0mm"
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Poles",
                        "Value:=", str(int(Poles))
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "PoleType",
                        "Value:=", '1'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Embrace",
                        "Value:=", 'Embrace'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "ThickMag",
                        "Value:=", 'ThickMag'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "WidthMag",
                        "Value:=", '45mm'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Offset",
                        "Value:=", '0deg'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Bridge",
                        "Value:=", '2mm'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "Rib",
                        "Value:=", '3mm'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "LenRegion",
                        "Value:=",  '200'
                    ],
                    [
                        "NAME:Pair",
                        "Name:=", "InfoCore",
                        "Value:=", str([0, 1][k])
                    ]
                ]
            ],
            [
                "NAME:Attributes",
                "Name:=", str(Names[k]),
                "Flags:=", "",
                "Color:=", str(Colors[k]).replace(',', ' '),
                "Transparency:=", 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:=", "",
                "MaterialValue:=", "\"vacuum\"".replace(
                    'vacuum', str(material[k])),
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "ShellElement:=", False,
                "ShellElementThickness:=", "0mm",
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:=", False
            ]
        )

    return main
