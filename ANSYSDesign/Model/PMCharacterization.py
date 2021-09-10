'''
Created on Apr 23, 2021

@author: Jimmy Palomino
'''


def PMCharacterization(main):
    """Function to name each magnet as PMx.

    Args:
        main (Dic): The main Dictionary.

    Returns:
        Dic: The same initial unmodified dictionary.
    """

    MagnetName = main['ANSYS']['Rotor&Magnets']['Name'][1]

    oEditor = main['ANSYS']['oEditor']

    PMMaterialName = main['ANSYS']['Materials']['PM']['PMName']

    # definitions of the PM characterization
    oEditor.SeparateBody(
        [
            "NAME:Selections",
            "Selections:=", MagnetName,
            "NewPartsModelFlag:=", "Model"
        ],
        [
            "CreateGroupsForNewObjects:=", False
        ]
    )

    # Getting the magnets names
    MagnetsNames = oEditor.GetMatchedObjectName(MagnetName+'*')

    # Naming as PMx
    PMNames = []
    for i, magnet in enumerate(MagnetsNames):
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        magnet
                    ],
                    [
                        "NAME:ChangedProps",
                        [

                            "NAME:Name",
                            "Value:=", "PM"+str(i+1)
                        ],
                        [
                            "NAME:Color",
                            "R:="			, 255,
                            "G:="			, 0,
                            "B:="			, 0
                        ]
                    ]
                ]
            ]
        )
        PMNames += ["PM"+str(i+1)]

    # Magnet material definion with 'in flux'
    for i in range(int(len(PMNames)/2)):

        oEditor.AssignMaterial(
            [
                "NAME:Selections",
                "AllowRegionDependentPartSelectionForPMLCreation:=", True,
                "AllowRegionSelectionForPMLCreation:=", True,
                "Selections:=", "PM"+str(i+1)
            ],
            [
                "NAME:Attributes",
                "MaterialValue:=", "\"replace\"".replace(
                    'replace', PMMaterialName[0]),
                "SolveInside:=", True,
                "ShellElement:=", False,
                "ShellElementThickness:=", "nan ",
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:=", False
            ]
        )

    # Magnets material definiton with 'out flux'
    for i in range(int(len(PMNames)/2), int(len(PMNames))):
        oEditor.AssignMaterial(
            [
                "NAME:Selections",
                "AllowRegionDependentPartSelectionForPMLCreation:=", True,
                "AllowRegionSelectionForPMLCreation:=", True,
                "Selections:=", "PM"+str(i+1)
            ],
            [
                "NAME:Attributes",
                "MaterialValue:=", "\"replace\"".replace(
                    'replace', PMMaterialName[1]),
                "SolveInside:=", True,
                "ShellElement:=", False,
                "ShellElementThickness:=", "nan ",
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:=", False
            ]
        )

    # Saving the magnets names
    main['ANSYS']['Rotor&Magnets']['PMNames'] = PMNames

    return main
