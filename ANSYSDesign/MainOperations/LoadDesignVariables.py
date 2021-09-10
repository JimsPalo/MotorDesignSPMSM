'''
Created on Jun 06, 2021

@author: Jimmy Palomino

All quantities are in mm
'''


def LoadDesignVariables(main):
    """This function is used to load the design varibles to the ANSYS environment.

    Args:
        main (Dic): Main Object
    """
    
    GeometricParameters = main['ANSYS']['DesignProperties']
    ODesign = main['ANSYS']['oDesign']

    for part, parameter in GeometricParameters.items():
        for SubparmeterName, SubparmeterValue in parameter.items():
            if SubparmeterName in ['Embrace', 'Pf', 'Iph', 'RotSpeed']:
                SubparmeterValue = str(SubparmeterValue)
            elif SubparmeterName in ['InitialPosition']:
                SubparmeterValue = str(SubparmeterValue) +'deg'
            else:
                SubparmeterValue = str(SubparmeterValue)+'mm'
            ODesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:LocalVariableTab",
                        [
                            "NAME:PropServers",
                            "LocalVariables"
                        ],
                        [
                            "NAME:NewProps",
                            [
                                "NAME:" + SubparmeterName,
                                "PropType:=", "VariableProp",
                                "UserDef:=", True,
                                "Value:=", SubparmeterValue
                            ]
                        ]
                    ]
                ]
            )
            
    return main
