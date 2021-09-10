'''
Created on Jun 06, 2021

@author: Jimmy Palomino

All quantities are in mm
'''
import numpy as np
from scipy.optimize import fsolve as fs

def GeometricParameters(main):
    HBCurve = main['ANSYS']['Materials']['Stator']['BHCurve'][1]
    mum = main['ANSYS']['Materials']['PM']['Permeability']
    Hc = main['ANSYS']['Materials']['PM']['CoercivityMagnitude']
    KneePoint = main['ANSYS']['Materials']['Stator']['KneePoint'][1]

    # Specifications Parameters predefined
    Qs = main['ANSYS']['Specifications']['Qs']
    Poles = main['ANSYS']['Specifications']['Poles']
    DiaYoke = main['ANSYS']['Specifications']['DiaYoke']
    Length = main['ANSYS']['Specifications']['Length']
    RatedPower = main['ANSYS']['Specifications']['RatedPower']
    speed = main['ANSYS']['Specifications']['Speed']
    kw = main['ANSYS']['Winding']['kw']
    VDC = main['ANSYS']['Specifications']['VDC']
    J = main['ANSYS']['Specifications']['J']

    # Constructional asuumptions
    print(mum)
    print(Hc)
    print(KneePoint)
    print(kw)

    # Filling factor
    kfill = 0.5

    # Phase Number
    m = 3

    # Assuming a voltage drop in the inverter of 2%
    InvVoltDrop = 0.02

    # Staking factor
    Ks = 0.95

    # tooth opening
    Bs0 = 2

    # Magnet width optimimum 0.83
    Embrace = 0.83

    # Tooth tip
    Hs0 = 1.5

    # Tooth wedge
    Hs1 = 2.5

    # Thickness Rotor Sleeve (mm)
    RotorSleeve = 2

    # Efective length discounting the end coils as 5%
    LengthEfective = Length*(1-0.05)

    # Aspect Ratio Inside Diameter to Outside Diameter
    AspectRatio = 0.5

    # Funtion used to fitting a*log(b*x)+c


    def p(x, a, b, c): return a * np.log(b * x) + c


    # Airgap flux densities based on recommentdations
    abc = [0.10711606, 1.24582401, 0.53210381]
    Bg = p(Poles, *abc)
    print(Bg)
    # Airgap height
    if Poles == 2:
        g = 0.1 + 0.02*(RatedPower)**(1/3) + RotorSleeve
    else:
        g = 0.1 + 0.012*(RatedPower)**(1/3) + RotorSleeve

    # Airgap Diameter
    DiaGap = DiaYoke*AspectRatio

    # Airgap area under one pole
    Ag = (DiaGap+g)*np.pi*LengthEfective/Poles*1e-6

    # Airgap flux
    AirgapFlux = Bg*Ag

    # Stator back iron thickness
    SYoke = AirgapFlux/(2*KneePoint*LengthEfective*Ks)*1e6

    # Rotor back iron thickness
    RYoke = AirgapFlux/(2*KneePoint*LengthEfective*Ks)*1e6

    # Concentration factor
    kds = (np.pi*DiaGap/Qs)/(np.pi*DiaGap/Qs-Bs0)

    Tw = AirgapFlux*kds/(KneePoint*LengthEfective*Ks)*1e6

    # mechanical speed
    Wm = speed/60*2*np.pi

    # vacuum permeability
    mu0 = np.pi*4e-7

    # Upper slot width
    Bs1 = np.pi*(DiaGap+2*(g + Hs0 + Hs1))/Qs-Tw

    # Initial variables
    # voltage follower
    Vbuffer = 0.95

    # Phase voltage in machine (peak)
    Vt = VDC*(1-InvVoltDrop)/np.sqrt(3)/np.sqrt(2)

    # Inducced fem hoped (peak)
    EMF = Vt*Vbuffer

    # Intial Value for Number of Turns in series (hoped)
    Nph = int(EMF/(Wm*kw*AirgapFlux/2)*np.sqrt(2))

    print()

    # Initial Value for slor height Hs2
    Hs2 = Tw*2

    # Magnet height (hm)
    hm = 3.06*g

    # Funtion to find Nph and Hs2


    def StatorSizing(A):

        Nph, Hs2 = A[0], A[1]
        # EMF induced in one phase
        EMF = Wm/2/np.sqrt(2)*kw*Nph*AirgapFlux

        # Current definition
        Iph = RatedPower/3/EMF

        # Equivalent Airgap
        # Airgap equivalent height
        geq = g + hm/mum

        # Airgap taking account the slotinig effect (Carter coefficient)
        LamdaCarter = 4/np.pi*(Bs0/2/geq*np.arctan(Bs0/2/geq)-np.log(1+(Bs0/2/geq)**2))

        # tooth pitch
        taoS = np.pi*DiaGap/Qs

        # Carter coefficient
        CarterCoeff = taoS/(taoS-LamdaCarter*geq)

        # Equivalent airgap height
        geq = g*CarterCoeff

        # Slot Airgap Inductance
        Lsg = 3/np.pi*(kw*Nph/(Poles/2))**2*mu0 * \
            (DiaGap+2*g)*LengthEfective/geq/1000

        # Lower slot width
        Bs2 = np.pi*(DiaGap+2*(g+Hs0+Hs1+Hs2))/Qs-Tw

        # Upper slot width
        Bs1 = np.pi*(DiaGap+2*(g + Hs0 + Hs1))/Qs-Tw

        # Ration of slot pitch to pole pitch
        B = Poles/Qs

        # Slots per pole per phase
        q = Qs/m/Poles

        # Slot Leakage Inductance
        LambdaSl = ((2/3)*Hs2/(Bs2 + Bs1) +
                    2*Hs1/(Bs0 + Bs1) +
                    Hs0/Bs0) *\
            (1+3*B)/4

        Lsl = 2*mu0*LengthEfective*Nph**2*LambdaSl/Poles/q/1000

        # lenght of the end winding pitch
        tauc = np.pi*(DiaGap+2*(g+Hs0+Hs1+Hs2/2))/Qs

        # Mean slot width
        Bsm = (Bs1 + Bs2)/2

        # End Winding Inductance
        Lew = mu0*tauc*Nph**2/16*np.log(np.pi*tauc**2/(4*Hs2*Bsm))/1000

        # Total inductance
        L = Lew + Lsl + Lsg

        # Average length of the end-winding
        lend = np.pi*((DiaGap + 2*g) + (Hs0 + Hs1 + Hs2))/Qs

        # Effective winding length by phase
        lw = 2*Nph*(LengthEfective + lend)

        # Cross Wire Area
        Awire = Iph/J

        # Cupper resistivity Ohms/mm
        RhoCu = 1.68e-11

        # Winding Resistance
        Rph = RhoCu*lw/Awire

        # Voltage error with parameters Nph and Hs2
        VoltError = (EMF + Rph*Iph)**2 + (2*np.pi*L*Iph)**2 - (Vt)**2

        # Conductor Diameter
        # Dw = np.sqrt(4*Awire/np.pi)

        # Copper Area
        Acu = Awire*Nph/Poles/q

        # Slot Area
        Aslot = (Bs1 + Bs2)/2*Hs2

        # Slot Area error
        ASlotError = Aslot - Acu/kfill

        return VoltError, ASlotError


    Nph, Hs2 = fs(StatorSizing, [Nph, Hs2])


    # Definition of Bs2
    Bs2 = np.pi*(DiaGap+2*(g+Hs0+Hs1+Hs2))/Qs-Tw

    # Loop to calculate Hs2
    Errorhm, count = 100, 0

    AirgapFlux  = AirgapFlux/2

    while (Errorhm >0.01) and (count<100):
        # Airgap equivalent height
        geq = g + hm/mum

        # Airgap taking account the slotinig effect (Carter coefficient)
        LamdaCarter = 4/np.pi*(Bs0/2/geq*np.arctan(Bs0/2/geq)-np.log(1+(Bs0/2/geq)**2))

        # tooth pitch
        taoS = np.pi*DiaGap/Qs

        # Carter coefficient
        CarterCoeff = taoS/(taoS-LamdaCarter*geq)

        # Equivalent airgap height
        gCarter = g*CarterCoeff

        # Pole Pitch
        taoP = DiaGap*2*np.pi/Poles

        # Airgap Reluctance

        RAirgap = gCarter/(mu0*taoP*LengthEfective)*1e3

        # Magnet Pitch
        taoPM = taoP*Embrace

        # PM Reluctance
        RPM = hm/(mu0*mum*taoPM*LengthEfective)*1e3

        # Distance between to magnets
        taoNotPM = taoP*(1-Embrace)

        # Leakage Reluctance
        RLeakage = taoNotPM/(mu0*(hm +g)*LengthEfective)*1e3

        # Efective longitudes
        LengthYokeStator = (DiaYoke - SYoke)*np.pi/Poles
        LengthYokeRotor = (DiaGap - 2*hm - RYoke)*np.pi/Poles
        LengthTooth = Hs0 + Hs1 + Hs2 + SYoke/2

        # Stator Tooth FMM
        BTooth = AirgapFlux/2/(Tw*LengthEfective*Qs/Poles/2*1e-6)
        HTooth = HBCurve(BTooth)
        FMMTooth = HTooth*LengthTooth

        # Stator Yoke FMM
        BStatorYoke = AirgapFlux/2/(SYoke*LengthEfective*1e-6)
        HSTator = HBCurve(BStatorYoke)
        FMMStator = HSTator*LengthYokeStator

        # FMM Stator
        FMMStator = FMMStator + 2*FMMTooth + AirgapFlux*4*RAirgap

        # Leakage Flux
        LeakageFLux = FMMStator/RLeakage

        # Rotor Flux
        RotorFlux = AirgapFlux + LeakageFLux 

        # Rotor Reluctance
        BRotorYoke = RotorFlux/2/(RYoke*LengthEfective*1e-6)
        HRotor = HBCurve(BRotorYoke)
        FMMRotor = HRotor*LengthYokeRotor

        # Magnet EMMFPM
        EMMFPM = FMMRotor + FMMStator

        # Magnet branch flux
        ParallelPMFlux = EMMFPM/(4*RPM)

        # Magnet Flux
        PMFlux = RotorFlux + ParallelPMFlux

        Bmagnet = PMFlux/(taoPM*LengthEfective*1e-6)

        Hmagnet = Bmagnet/mum/mu0 + Hc

        hm0 = -EMMFPM/(Hmagnet)*1000

        Errorhm = np.abs(hm0-hm)
        hm = hm0
        count += 1

    AirgapFlux  = AirgapFlux*2

    # EMF induced in one phase
    EMF = Wm/2/np.sqrt(2)*kw*Nph*AirgapFlux
    
    # Rated current definition (rms)
    Iph = RatedPower/3/EMF


    GeometricParameters = {
        'Stator': {
            'g': g,
            'DiaYoke': DiaYoke,
            'Lenght': LengthEfective,
        },
        'Slot': {
            'Hs0': Hs0,
            'Hs1': Hs1,
            'Hs2': Hs2,
            'Bs0': Bs0,
            'Bs1': Bs1,
            'Bs2': Bs2,
            'Rs': 5
        },
        'Rotor': {
            'DiaGap': DiaGap,
            'DiaYokeR': DiaGap - 2*(RYoke + hm + g),
            'Embrace': Embrace,
            'ThickMag': hm,
            'RotSpeed': speed,
        },
        'Electric': {
                    'Iph': Iph,
                    'Pf': np.pi/180*20,
                    'InitialPosition': 15,
                }
    }

    main['ANSYS']['DesignProperties'] = GeometricParameters

    main['ANSYS']['FixedVariables']['Nph'] = Nph
    main['ANSYS']['FixedVariables']['Iph'] = Iph
    main['ANSYS']['FixedVariables']['Poles'] = Poles
    main['ANSYS']['FixedVariables']['Slots'] = Qs



    return main

    

