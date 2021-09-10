'''
Created on Apr 29, 2021

@author: Jimmy Palomino
'''


def AnalysisSetup(main):
    """This function setup the configuration for the analysis.

    Args:
        main (Dic): Main dictionary used to upload the necessary information.

    Returns:
        Dic: the main dictionary uploaded the oMolude, which is used to the analysis setup.
    """

    # oDesign definition
    oDesign = main['ANSYS']['oDesign']

    # Set core losses
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.SetCoreLoss(["Stator", "Rotor"], False)

    # Defining the necessary module
    oModule = oDesign.GetModule("AnalysisSetup")

    # Multiplier
    Multiplier = main['ANSYS']['AnalysisSetup']['Multiplier']

    # Analysis name
    AnalysisName = main['ANSYS']['AnalysisSetup']['Name']

    # PercentError
    PercentError = main['ANSYS']['AnalysisSetup']['PercentError']

    # RefinementPerPass
    RefinementPerPass = main['ANSYS']['AnalysisSetup']['RefinementPerPass']

    # NonLinearResidual
    NonLinearResidual = main['ANSYS']['AnalysisSetup']['NonLinearResidual']

    # Design Settings
    oDesign.SetDesignSettings(
        [
            "NAME:Design Settings Data",
            "Perform Minimal validation:=", False,
            "EnabledObjects:="	, [],
            "PreserveTranSolnAfterDatasetEdit:=", False,
            "ComputeTransientInductance:=", False,
            "ComputeIncrementalMatrix:=", False,
            "PerfectConductorThreshold:=", 1E+30,
            "InsulatorThreshold:="	, 1,
            "ModelDepth:="		, "Lenght",
            "UseSkewModel:="	, False,
            "EnableTranTranLinkWithSimplorer:=", False,
            "BackgroundMaterialName:=", "vacuum",
            "SolveFraction:="	, False,
            "Multiplier:="		, str(Multiplier)
        ],
        [
            "NAME:Model Validation Settings",
            "EntityCheckLevel:="	, "Strict",
            "IgnoreUnclassifiedObjects:=", False,
            "SkipIntersectionChecks:=", False
        ]
    )

    # Analysis setup
    oModule.InsertSetup(
        "Transient",
        [
            "NAME:" + AnalysisName,
            "Enabled:="		, True,
            [
                "NAME:MeshLink",
                "ImportMesh:="		, False
            ],
            "NonlinearSolverResidual:=", "1e-06",
            "TimeIntegrationMethod:=", "BackwardEuler",
            "SmoothBHCurve:="	, False,
            "StopTime:="		, "20ms",
            "TimeStep:="		, "300us",
            "OutputError:="		, False,
            "UseControlProgram:="	, False,
            "ControlProgramName:="	, " ",
            "ControlProgramArg:="	, " ",
            "CallCtrlProgAfterLastStep:=", False,
            "FastReachSteadyState:=", False,
            "AutoDetectSteadyState:=", False,
            "IsGeneralTransient:="	, True,
            "IsHalfPeriodicTransient:=", False,
            "SaveFieldsType:="	, "Custom",
            [
                "NAME:SweepRanges",
                [
                    "NAME:Subrange",
                    "RangeType:="		, "LinearStep",
                    "RangeStart:="		, "0ms",
                    "RangeEnd:="		, "20ms",
                    "RangeStep:="		, "300us"
                ]
            ],
            "UseNonLinearIterNum:="	, False,
            "CacheSaveKind:="	, "Count",
            "NumberSolveSteps:="	, 1,
            "RangeStart:="		, "0s",
            "RangeEnd:="		, "0.1s",
            "UseAdaptiveTimeStep:="	, False,
            "InitialTimeStep:="	, "0.002s",
            "MinTimeStep:="		, "0.001s",
            "MaxTimeStep:="		, "0.003s",
            "TimeStepErrTolerance:=", 0.0001
        ]
    )

    main['ANSYS']['AnalysisSetup']['oModule'] = oModule

    # Developing the all analysis
    # oDesign.AnalyzeAll()

    print(oDesign.GetPostProcessingVariables())

    return main
