'''
Created on Apr 21, 2021

@author: Jimmy Palomino
'''
import numpy as np


def WindingDesign(main):
    """Funtion used to place each coil in the machinery

    Returns:
        Dic: Main boject upload the coil names.
    """
    oEditor = main['ANSYS']['oEditor']

    # Slots number
    Slots = main['ANSYS']['FixedVariables']['Slots']

    # SlotType
    SlotType = main['ANSYS']['FixedVariables']['SlotType']

    # Geimetric parameters
    g = main['ANSYS']['DesignProperties']['Stator']['g']

    Hs0 = main['ANSYS']['DesignProperties']['Slot']['Hs0']
    Hs1 = main['ANSYS']['DesignProperties']['Slot']['Hs1']
    Hs2 = main['ANSYS']['DesignProperties']['Slot']['Hs2']
    Bs1 = main['ANSYS']['DesignProperties']['Slot']['Bs1']
    Bs2 = main['ANSYS']['DesignProperties']['Slot']['Bs2']

    DiaGap = main['ANSYS']['DesignProperties']['Rotor']['DiaGap']

    # Coils Arrange ABC
    PhasesABC = main['ANSYS']['Winding']['ABC']

    # Color used for phases
    Color = main['ANSYS']['Winding']['Color']

    oEditor.CreateUserDefinedPart(
        [
            "NAME:UserDefinedPrimitiveParameters",
            "DllName:="		, "RMxprt/LapCoil.dll",
            "Version:="		, "16.0",
            "NoOfParameters:="	, 22,
            "Library:="		, "syslib",
            [
                "NAME:ParamVector",
                [
                    "NAME:Pair",
                    "Name:="		, "DiaGap",
                    "Value:="		, "DiaGap+g*2"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "DiaYoke",
                    "Value:="		, "DiaYoke"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Length",
                    "Value:="		, "0mm"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Skew",
                    "Value:="		, "0deg"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Slots",
                    "Value:="		, str(int(Slots))
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "SlotType",
                    "Value:="		, str(int(SlotType))
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Hs0",
                    "Value:="		, "Hs0"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Hs1",
                    "Value:="		, "Hs1"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Hs2",
                    "Value:="		, "Hs2"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Bs0",
                    "Value:="		, "Bs0"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Bs1",
                    "Value:="		, "Bs1"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Bs2",
                    "Value:="		, "Bs2"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Rs",
                    "Value:="		, "Rs"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "FilletType",
                    "Value:="		, "0"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "Layers",
                    "Value:="		, "2"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "CoilPitch",
                    "Value:="		, "1"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "EndExt",
                    "Value:="		, "5mm"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "SpanExt",
                    "Value:="		, "25mm"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "BendAngle",
                    "Value:="		, "0deg"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "SegAngle",
                    "Value:="		, "10deg"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "LenRegion",
                    "Value:="		, "200mm"
                ],
                [
                    "NAME:Pair",
                    "Name:="		, "InfoCoil",
                    "Value:="		, "0"
                ]
            ]
        ],
        [
            "NAME:Attributes",
            "Name:="		, "LapCoil1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"copper\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ]
    )

    # Body Separation
    oEditor.SeparateBody(
        [
            "NAME:Selections",
            "Selections:="		, "LapCoil1",
            "NewPartsModelFlag:="	, "Model"
        ],
        [
            "CreateGroupsForNewObjects:=", False
        ]
    )

    # Average Slot Width
    AverWidth = (Bs2 + Bs1)/2

    # Average Radius
    AverRadius = DiaGap/2 + g + Hs0 + Hs1 + Hs2*0.75

    # Angle to shift and find the kth tooth
    ShiftSlot = 1/Slots*np.pi

    # Angle to fond the corrent layer
    ShiftLayer = np.arctan(AverWidth/4/AverRadius)

    # List to save the coils sides names
    WindingNames = [[], [], []]

    # Phases name to employed
    PhaseNames = ['A', 'B', 'C']

    for phase, row in enumerate(PhasesABC):

        PhaseName = [[], []]

        for coil, slot in enumerate(row):

            SlotAngle = np.abs(slot)/Slots*2*np.pi - ShiftSlot

            if coil % 2 == 1:
                SlotAngle = SlotAngle - ShiftLayer

            else:
                SlotAngle = SlotAngle + ShiftLayer

            x = np.cos(SlotAngle)*AverRadius
            y = np.sin(SlotAngle)*AverRadius

            Name0 = oEditor.GetBodyNamesByPosition(
                [
                    "NAME:Parameters",
                    "XPosition:=", str(x)+"mm",
                    "YPosition:=", str(y)+"mm",
                    "ZPosition:=", "0mm"
                ]
            )

            C = Color[phase]

            if np.sign(slot) == 1:

                CoilSideName = PhaseNames[phase]+"In"+str(np.abs(coil))

                PhaseName[0] += [CoilSideName]

                oEditor.ChangeProperty(
                    [
                        "NAME:AllTabs",
                        [
                            "NAME:Geometry3DAttributeTab",
                            [
                                "NAME:PropServers",
                                Name0[0]
                            ],
                            [
                                "NAME:ChangedProps",
                                [
                                    "NAME:Name",
                                    "Value:="		,
                                    CoilSideName
                                ],
                                [
                                    "NAME:Color",
                                    "R:="			, C[0],
                                    "G:="			, C[1],
                                    "B:="			, C[2]
                                ],

                            ]
                        ]
                    ]
                )
            else:

                CoilSideName = PhaseNames[phase]+"Out"+str(np.abs(coil))

                PhaseName[1] += [CoilSideName]

                oEditor.ChangeProperty(
                    [
                        "NAME:AllTabs",
                        [
                            "NAME:Geometry3DAttributeTab",
                            [
                                "NAME:PropServers",
                                Name0[0]
                            ],
                            [
                                "NAME:ChangedProps",
                                [
                                    "NAME:Name",
                                    "Value:="		,
                                    CoilSideName
                                ],
                                [
                                    "NAME:Color",
                                    "R:="			, C[0],
                                    "G:="			, C[1],
                                    "B:="			, C[2],
                                ],

                            ]
                        ]
                    ]
                )

        WindingNames[phase] += PhaseName

    main['ANSYS']['Winding']['CoilNames'] = WindingNames

    return main
