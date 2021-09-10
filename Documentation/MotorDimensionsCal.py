'''
Created on Jul 07, 2021

@author: Jimmy Palomino
'''

import numpy as np
from scipy.optimize import fsolve as fs



def MotorDimensionsCal(LoopSignal):
    """Calculate the motor Dimensions

    Args:
        LoopSignal (Dic): Problem data

    Returns:
        Dic: Motor Dimensions
    """
    # Variable defintion 
    BAirgap = LoopSignal['BAirgap']
    L = LoopSignal['L']
    D = LoopSignal['D']
    hm = LoopSignal['hm']
    J = LoopSignal['J']
    g = LoopSignal['g']
    Np = LoopSignal['Np']
    Nm = LoopSignal['Nm']
    f = LoopSignal['f']
    m = LoopSignal['m']
    Vt = LoopSignal['Vt']
    TAngle = LoopSignal['TAngle']
    MuPM = LoopSignal['MuPM']
    OpeTemp = LoopSignal['OpeTemp']
    Bknee = LoopSignal['Bknee']
    kw = LoopSignal['kw']
    Hs0 = LoopSignal['Hs0']
    Rs = LoopSignal['Rs']
    Kfill = LoopSignal['Kfill']
    Ks = LoopSignal['Ks']
    alphaPM = LoopSignal['alphaPM']
    Bs0 = LoopSignal['Bs0']
    Pmec = LoopSignal['Pmec']

    # vaccum permeability
    Mu0 = np.pi*4e-7

    # Slots per phase per pole
    q = Nm/m/Np

    # flux per pole
    PhiPole = BAirgap *\
        np.pi*L*D/Np*1e-6

    SWidth = PhiPole/(2*Bknee*Ks*L)*1e6

    RWidth = PhiPole/(2*Bknee*Ks*L)*1e6

    Kds = 1/(1-Bs0*Nm/D/np.pi)

    # width of tooth per pole
    ToothPerPole = PhiPole*Kds/Bknee/Ks/L*1e6

    # width of the tooth
    Tw = ToothPerPole/(Nm/Np)

    # Magnet Diameter
    DPM = D-2*g

    # Inner rotor diameter
    DInRot = DPM - 2*(hm-RWidth)

    TeethPitch = D*np.pi/Nm - Bs0

    BsR = TeethPitch - Tw

    # Hs1 defintion
    Hs1 = 0.5*BsR*np.tan(TAngle/180*np.pi)

    # Bs1 Definiton
    Bs1 = ((D/2 + Hs0 + Hs1)*np.tan(np.pi/Nm) -
            Tw/2/np.cos(np.pi/Nm))*2

    # Slot pitch
    TauSlot = np.pi*D/Nm

    # Pole pitch
    TauPole = np.pi*D/Np

    # Function definiton
    # Carter coefficient
    def Carter(Bs0, TauSlot, geq): return \
        (1-2*Bs0/np.pi/TauSlot*(
            np.arctan(Bs0/2/geq) -
            geq/Bs0*np.log(1+1/4*(Bs0/geq)**2)
        ))**-1

    # Inductance definition
    def Inductance(Hs2, Nph):
        """Funtion used to calculate the machine synchronous inductancae

        Args:
            Hs2 (float): slot height
            Nph (int): turns number 

        Returns:
            float: synchronous inductance
        """
        # Airgap inductance
        Lsg = 3/np.pi*(kw*Nph/(Np/2)) ** 2*Mu0 /\
            (g + hm/MuPM)/Carter(Bs0, TauSlot, g + hm/MuPM) *\
            D*L*1e-3
        # Uppeer Slot width
        Bs2 = ((D/2 + Hs2 + Hs1 + Hs0)*np.tan(np.pi/Nm) -
                Tw/2/np.cos(np.pi/Nm))*2

        # Slot Inductance
        GammaSL = (2/3*Hs2/(Bs1 + Bs2) +
                    2*Hs1/(Bs0 + Bs1) +
                    Hs0/Bs0) *\
            ((1 + 3*(TauSlot/TauPole))/4)

        Lsl = 2*Mu0*L*1e-3*(Nph)**2/(Np*q)*GammaSL

        # Slot area
        Aslot = (Bs1 + Bs2)/2*Hs2 +\
            (Bs2 - 2*Rs)*Rs +\
            np.pi*Rs**2/2

        # End Winding Inductance
        Lew = Mu0*TauSlot*Nph**2/16 *\
            np.log(np.pi*TauSlot**2 /
                    4/Aslot)*1e-3
        
        return Lsg + Lsl + Lew

    # Resistance function definition
    def Resistance(Hs2, Nph, Iph):
        """Calculate the Machine resistance

        Args:
            Hs2 (float): slot height
            Nph (int): turns number in series
            Iph (float): Machine current

        Returns:
            int: Calculate resistance
        """
        # function to calculate the resistance

        # Average length of the end-winding
        lend = np.pi*(D + (Hs0 + Hs1 + Hs2))/Nm

        # Effective winding length by phase
        lw = 2*Nph*(L + lend)

        # Cross Wire Area
        Awire = Iph/J

        # Cupper resistivity Ohms/mm
        RhoCu = 1.68e-11

        # Winding Resistance
        Rph = RhoCu*lw/Awire

        return Rph

    # Slot Height And Turns funtion
    def HeightAndTurns(Hs2Nph):
        """function used to calculate the slot height and the turns number

        Args:
            Hs2Nph (array): two dimension array

        Returns:
            Errors: Erros between the calculated and the hoped quantities
        """
        # positive condition
        Hs2 = np.abs(Hs2Nph[0])
        Nph = np.abs(Hs2Nph[1])

        #Hs2 = 2*Tw

        EMF = 2*np.pi*f/np.sqrt(2) *\
            Nph*kw *\
            2/np.pi*BAirgap *\
            2*D*L/Np*1e-6

        Iph = Pmec/3/EMF

        # Inductance
        Lph = Inductance(Hs2, Nph)

        # Resistance
        Rph = Resistance(Hs2, Nph, Iph)
        
        # Erro EMF Calculation
        ErrorEMF = (EMF+Rph*Iph)**2 +\
            (2*np.pi*f*(Lph)*Iph)**2 -\
            Vt**2

        # Wire Diameter
        Dwire = 2*np.sqrt(Iph/J/np.pi)

        # AWG gauge
        AWG = np.round(np.log(Dwire/8.251463)/np.log(0.8905257))

        DAWG = 8.251463*(0.8905257)*AWG

        Awire = np.pi*DAWG**2/4

        Acu = Awire*Np /\
            (q*Np/2)

        # Required slot area
        Aslot = Acu/Kfill

        Bs2 = ((D/2 + Hs0 + Hs1 + Hs2)*np.tan(np.pi/Nm) -
            Tw/2/np.cos(np.pi/Nm))*2

        Bs1 = ((D/2 + Hs0 + Hs1)*np.tan(np.pi/Nm) -
            Tw/2/np.cos(np.pi/Nm))*2

        # Calculated slot area without physic limitation
        Aslot0 = (Bs1+Bs2)/2*Hs2 +\
            (Bs2-2*Rs)*Rs +\
            np.pi*Rs**2/2
        # Taking account additional elements
        SlotLiner = 0.001

        Wedgethick = 0.001

        LayIns = 0.001

        # Calculated slot Area
        ASlotWire = Aslot0 -\
            Hs2*LayIns -\
            Bs2*LayIns -\
            (2*Bs1+Bs2+2*Hs2/np.cos(np.pi/Nm))*SlotLiner -\
            Bs1*Wedgethick

        # ErrorSlot calculation
        ErrorSlot = ASlotWire - Aslot

        return ErrorEMF, ErrorSlot

    Hs2, Nph = fs(HeightAndTurns, [2*Tw, 80])

    Hs2 = np.abs(Hs2)

    Ncoilside = int((m*Nph*2)/(Nm*2))

    Nph = Ncoilside*2*Nm/2/m

    Bs2 = ((D/2 + Hs0 + Hs1 + Hs2)*np.tan(np.pi/Nm) -
            Tw/2/np.cos(np.pi/Nm))*2

    Dimensions = {
        'Hs0': Hs0,
        'Hs1': Hs1,
        'Hs2': Hs2,
        'Bs0':Bs0,
        'Bs1':Bs1,
        'Bs2':Bs2,
        'DInRot': DInRot,
        'SWidth': SWidth,
        'RWidth': RWidth,
    }

    return Dimensions