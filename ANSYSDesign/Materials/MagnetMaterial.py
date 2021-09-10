'''
Created on Apr 24, 2021

@author: Jimmy Palomino
'''


def MagnetMaterial(main):
    """ Function to load the information about the PM material to ANSYS.

    Args:
        main (Dic): main object used to upload the information.

    Returns:
        Dic: The same initial dictionary
    """
    MaterialsPM = main['ANSYS']['Materials']['PM']

    # oDefiniitonManager
    oDefinitionManager = main['ANSYS']['Materials']['oDefinitionManager']

    # Magnet variables
    PMName = MaterialsPM['PMName']
    Permeability = MaterialsPM['Permeability']
    CoercivityMagnitude = MaterialsPM['CoercivityMagnitude']
    conductivity = MaterialsPM['conductivity']
    MassDensity = MaterialsPM['MassDensity']

    # Adding material for magnets with Out flux

    oDefinitionManager.AddMaterial(
        [
            "NAME:"+PMName+'Out',
            "CoordinateSystemType:=", 'Cylindrical',
            "BulkOrSurfaceType:=", 1,
            [
                "NAME:PhysicsTypes",
                "set:=", ["Electromagnetic"]
            ],
            "permeability:=", str(Permeability),
            'conductivity:=', str(conductivity),
            [
                "NAME:magnetic_coercivity",
                "property_type:=", "VectorProperty",
                "Magnitude:=", str(CoercivityMagnitude)+"A_per_meter",
                "DirComp1:=", '1',
                "DirComp2:=", '0',
                "DirComp3:=", '0',
                'mass_density:=', str(MassDensity)
            ]
        ]
    )

    # Adding mateial with In flux
    oDefinitionManager.AddMaterial(
        [
            "NAME:"+PMName+'In',
            "CoordinateSystemType:=", 'Cylindrical',
            "BulkOrSurfaceType:=", 1,
            [
                "NAME:PhysicsTypes",
                "set:=", ["Electromagnetic"]
            ],
            "permeability:=", str(Permeability),
            'conductivity:=', str(conductivity),
            [
                "NAME:magnetic_coercivity",
                "property_type:=", "VectorProperty",
                "Magnitude:=", str(CoercivityMagnitude)+"A_per_meter",
                "DirComp1:=", '-1',
                "DirComp2:=", '0',
                "DirComp3:=", '0',
                'mass_density:=', str(MassDensity)
            ]
        ]
    )

    # saving magnetic materials
    main['ANSYS']['Materials']['PM']['PMName'] = [PMName+'In', PMName+'Out']

    return main
