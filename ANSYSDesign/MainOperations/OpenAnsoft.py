'''
Created on Apr 21, 2021

@author: Jimmy Palomino
'''

from win32com import client


def OpenAnsoft(main):
    """Open ANSYS Electronics Application.

    Args:
        main (Dic): Contains the main information.

    Returns:
        Dic: Return the last Dictionary uploaded the main object for ANSYS managing.
    """

    # Loading variables
    ProjectName = main['ANSYS']['ProjectName']
    DesignName = main['ANSYS']['DesignName']

    # oDesktop object
    oAnsoftApp = client.Dispatch('Ansoft.ElectronicsDesktop')
    oDesktop = oAnsoftApp.GetAppDesktop()

    # Restore a minimized window
    oDesktop.RestoreWindow()

    # oProject object
    oProject = oDesktop.NewProject(ProjectName)

    # oDefinitionManager
    oDefinitionManager = oProject.GetDefinitionManager()

    # oDesign object
    oProject.InsertDesign('Maxwell 2D', DesignName, "Transient", '')
    oDesign = oProject.SetActiveDesign(DesignName)

    # Design view
    oEditor = oDesign.SetActiveEditor("3D Modeler")

    # updating variables
    main['ANSYS']['oAnsoftApp'] = oAnsoftApp
    main['ANSYS']['oDesktop'] = oDesktop
    main['ANSYS']['oProject'] = oProject
    main['ANSYS']['Materials']['oDefinitionManager'] = oDefinitionManager
    main['ANSYS']['oDesign'] = oDesign
    main['ANSYS']['oEditor'] = oEditor

    return main
