'''
Created on Apr 29, 2021

@author: Jimmy Palomino
'''


def MeshMachine(main):
    """Function used to setting up the meshes for the each elements of the machine. 

    Args:
        main (Dic): The main object used to upload the necessary information.

    Returns:
        Dic: The same main dictionary.
    """

    # oDesign definition
    oDesign = main['ANSYS']['oDesign']

    # Data for the rotor mesh
    RotorName = main['ANSYS']['Rotor&Magnets']['Name'][0]
    RotorNumMaxElem = main['ANSYS']['Mesh']['Rotor']['NumMaxElem']
    RotorMaxLength = main['ANSYS']['Mesh']['Rotor']['MaxLength']

    # Data for the magnets mesh
    PMNames = main['ANSYS']['Rotor&Magnets']['PMNames']
    PMNumMaxElem = main['ANSYS']['Mesh']['Magnets']['NumMaxElem']
    PMMaxLength = main['ANSYS']['Mesh']['Magnets']['MaxLength']

    # Data for the Stator mesh
    StatorName = main['ANSYS']['Stator']['Name']
    StatorNormalDev = main['ANSYS']['Mesh']['Stator']['NormalDev']
    StatorAspectRatio = main['ANSYS']['Mesh']['Stator']['AspectRatio']

    # Data for the Stator mesh
    CoilNames = main['ANSYS']['Winding']['CoilNames']
    WindingNumMaxElem = main['ANSYS']['Mesh']['Winding']['NumMaxElem']
    WindingMaxLength = main['ANSYS']['Mesh']['Winding']['MaxLength']

    WindingName = []
    for phase in CoilNames:
        for direction in phase:
            WindingName += direction

    # Creating meshes
    oModule = oDesign.GetModule("MeshSetup")

    # Rotor meshes
    oModule.AssignLengthOp(
        [
            "NAME:Rotor",
            "RefineInside:=", True,
            "Enabled:=", True,
            "Objects:=", [RotorName],
            "RestrictElem:=", False,
            "NumMaxElem:=", str(RotorNumMaxElem),
            "RestrictLength:=", True,
            "MaxLength:=", str(RotorMaxLength)+"mm"
        ]
    )
    # Magnet meshes
    oModule.AssignLengthOp(
        [
            "NAME:Magnets",
            "RefineInside:=", True,
            "Enabled:=", True,
            "Objects:=", PMNames,
            "RestrictElem:=", False,
            "NumMaxElem:=", str(PMNumMaxElem),
            "RestrictLength:=", True,
            "MaxLength:=", str(PMMaxLength)+"mm"
        ]
    )
    # Stator meshes
    oModule.AssignTrueSurfOp(
        [
            "NAME:Stator",
            "Objects:=", [StatorName],
            "CurvedSurfaceApproxChoice:=", "ManualSettings",
            "SurfDevChoice:=", 0,
            "NormalDevChoice:=", 2,
            "NormalDev:=", str(StatorNormalDev) + "deg",
            "AspectRatioChoice:=", 2,
            "AspectRatio:=", str(StatorAspectRatio)
        ]
    )

    # Coil meshes
    oModule.AssignLengthOp(
        [
            "NAME:Coils",
            "RefineInside:="	, True,
            "Enabled:="		, True,
            "Objects:="		, WindingName,
            "RestrictElem:="	, False,
            "NumMaxElem:="		, str(WindingNumMaxElem),
            "RestrictLength:="	, True,
            "MaxLength:="		, str(WindingMaxLength) +"mm"
        ]
    )

    return main
