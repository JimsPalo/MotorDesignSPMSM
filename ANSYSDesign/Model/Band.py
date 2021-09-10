'''
Created on Apr 23, 2021

@author: Jimmy Palomino
'''


def Band(main):
    """This function creates the region and set the boundaries to the
     machine analysis by FEM.

    Args:
        main (Dic): Main Dictionary than contain the necessary information.

    Returns:
        Dic: unmodified main dictionary.
    """

    oEditor = main['ANSYS']['oEditor']
    oDesign = main['ANSYS']['oDesign']

    # Drawing the Band
    oEditor.CreateCircle(
        [
            "NAME:CircleParameters",
            "IsCovered:="		, True,
            "XCenter:="		, "0mm",
            "YCenter:="		, "0mm",
            "ZCenter:="		, "0mm",
            "Radius:="		, "DiaGap/2+g/2",
            "WhichAxis:="		, "Z",
            "NumSegments:="		, "0"
        ],
        [
            "NAME:Attributes",
            "Name:="		, 'Band',
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0.75,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ]
    )

    # Drawing the Inner Band
    oEditor.CreateCircle(
        [
            "NAME:CircleParameters",
            "IsCovered:="		, True,
            "XCenter:="		, "0mm",
            "YCenter:="		, "0mm",
            "ZCenter:="		, "0mm",
            "Radius:="		, "DiaGap/2",
            "WhichAxis:="		, "Z",
            "NumSegments:="		, "0"
        ],
        [
            "NAME:Attributes",
            "Name:="		, 'InnerBand',
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0.75,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"vacuum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, True,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ]
    )

    # Band assignation
    oModule = oDesign.GetModule("ModelSetup")
    oModule.AssignBand(
        [
            "NAME:Data",
            "Move Type:="		, "Rotate",
            "Coordinate System:="	, "Global",
            "Axis:="		, "Z",
            "Is Positive:="		, True,
            "InitPos:="		, "InitialPosition",
            "HasRotateLimit:="	, False,
            "NonCylindrical:="	, False,
            "Consider Mechanical Transient:=", False,
            "Angular Velocity:="	, "RotSpeed*1rpm",
            "Objects:="		, ["Band"]
        ]
    )

    return main
