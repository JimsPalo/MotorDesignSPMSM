'''
Created on Apr 23, 2021

@author: Jimmy Palomino
'''


def Region(main):
    """This function creates the region and set the boundaries to the
     machine analysis by FEM.

    Args:
        main (Dic): Main Dictionary than contain the necessary information.

    Returns:
        Dic: unmodified main dictionary.
    """

    oEditor = main['ANSYS']['oEditor']

    oDesign = main['ANSYS']['oDesign']

    RegionName = main['ANSYS']['Region']['RegionName']

    oModule = oDesign.GetModule("BoundarySetup")

    OffsetPercent = main['ANSYS']['Region']['OffsetPercent']

    # Drawing the Region
    oEditor.CreateCircle(
        [
            "NAME:CircleParameters",
            "IsCovered:="		, True,
            "XCenter:="		, "0mm",
            "YCenter:="		, "0mm",
            "ZCenter:="		, "0mm",
            "Radius:="		, "DiaYoke/2"+'*'+str(1+OffsetPercent/100),
            "WhichAxis:="		, "Z",
            "NumSegments:="		, "0"
        ],
        [
            "NAME:Attributes",
            "Name:="		, RegionName,
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

    # Boundaries setting
    Edges = oEditor.GetEdgeIDsFromObject(RegionName)

    oModule.AssignVectorPotential(
        [
            "NAME:VectorPotential1",
            "Edges:="		, [int(Edges[0])],
            "Value:="		, "0",
            "CoordinateSystem:="	, ""
        ]
    )

    oEditor.FitAll()

    return main
