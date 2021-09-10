'''
Created on Jun 06, 2021

@author: Jimmy Palomino

All quantities are in mm
'''
import numpy as np
from scipy.optimize import fsolve as fs

from MotorDimensionsCal import MotorDimensionsCal
from StatorMaterial import StatorMaterial


# Specifications

HBCurve = StatorMaterial

Pmec, speed, Vdc, Nm, Np = 60e3, 2.5e3, 400, 12, 10

# Assumptions
Vinv, m, alphaPM, Bs0, RotorSleeve = 2.31, 3, 0.83, 2, 1.5

kw, Hs0, Rs, Kfill, Ks = 0.933, 1.5, 0, 0.5, 0.95

# Magnetic properties
Br20, MuPM, alphaBr, OpeTemp, Bknee = 1.16, 1.1, -0.08, 0, 1.35

# Airgap defintion
g = 0.1 + 0.012*(Pmec)**(1/3) + RotorSleeve

# Prime Variables
D, L, hm, J = 150, 300, g*4, 7.5

# Angle for tooth wedge assumed on 30 degres
TAngle = 30

# vaccum permeability
Mu0 = np.pi*4e-7

# Magnent remanence
Br = Br20*(1+alphaBr*(OpeTemp-20)/100)

# Terminal voltage
Vt = Vdc*(1-Vinv/100)/np.sqrt(2)/np.sqrt(3)

# Slots per phase per pole
q = Nm/m/Np

# Electric frequency
f = speed*Np/120

# Calculation of teeth width and yoke thickness
FLeakage = 0.95

Bg = FLeakage*alphaPM*Br/(1+(FLeakage*g*MuPM*alphaPM/hm))

# peak flux in the airgap fundamental
BAirgap = 4/np.pi*Bg*np.sin(np.pi*alphaPM/2)

Bm = Bg/FLeakage

# flux per pole
PhiPole = BAirgap *\
    np.pi*L*D/Np*1e-6

# Dictionary defintion
LoopSignal = {
    'BAirgap': BAirgap,
    'L': L,
    'D': D,
    'hm': hm,
    'J': J,
    'g': g,
    'Np': Np,
    'Nm': Nm,
    'f': f,
    'm': m,
    'Vt': Vt,
    'TAngle': TAngle,
    'MuPM': MuPM,
    'OpeTemp': OpeTemp,
    'Bknee': Bknee,
    'kw': kw,
    'Hs0': Hs0,
    'Rs':Rs,
    'Kfill': Kfill,
    'Ks':Ks,
    'alphaPM': alphaPM,
    'Bs0':Bs0,
    'Pmec': Pmec,
}

Dimensions = MotorDimensionsCal(LoopSignal)

Hs0 = Dimensions['Hs0']
Hs1 = Dimensions['Hs1']
Hs2 = Dimensions['Hs2']
Bs0 = Dimensions['Bs0']
Bs1 = Dimensions['Bs1']
Bs2 = Dimensions['Bs2']
DInRot = Dimensions['DInRot']
SWidth = Dimensions['SWidth']
RWidth = Dimensions['RWidth']

# Rotor Reluctance Back Iron
ThetaPolar = 2*np.pi/Np

ThetaEff = ThetaPolar*(1 - alphaPM)

DEff0 = D/2 - g - hm - RWidth/2

AreaRotor  = (RWidth*L)*1e6 

BRotor = PhiPole/2/AreaRotor

HRotor = HBCurve(BRotor)

LRotor = ThetaEff*DEff0*1e-3

RRotor = HRotor*LRotor/(PhiPole/2)

# Stator Reluctance Back Iron
DEff1 = D/2 + Hs0 + Hs1 + Hs2 + SWidth/2

AreaStator = (SWidth*L)*1e6

BStator = PhiPole/2/AreaStator

HStator = HBCurve(BStator)

LStator = ThetaEff*DEff1*1e-3

RStator = HStator*LStator/(PhiPole/2)

# Tooth Reluctance
Hss = (Hs0 + Hs1 + Hs2 + SWidth/2) *1e-3





print(PhiPole, BRotor)


#print(Nph, Ncoilside)

'''# Redefinition of the number by slide
Ncoilside = int((m*Nph*2)/(Nm*2))

Nph = Ncoilside*2*Nm/2/m

EMF = 2*np.pi*f/np.sqrt(2) *\
    Nph*kw *\
        2/np.pi*BAirgap *\
            2*D*L/Np*1e-6

Iph = Pmec/3/EMF

Dwire = 2*np.sqrt(Iph/J/np.pi)

AWG = np.round(np.log(Dwire/8.251463)/np.log(0.8905257))

DAWG = 8.251463*(0.8905257)*AWG

Awire = np.pi*DAWG**2/4

Acu = Awire*Np /\
    (q*Np/2)

J0 = Iph/Awire

Aslot = Acu/Kfill


def SlotHeight(Hs02):
    Hs2 = np.abs(Hs02)
    Bs2 = ((D/2 + Hs0 + Hs1 + Hs2)*np.tan(np.pi/Nm) -
           Tw/2/np.cos(np.pi/Nm))*2

    Bs1 = ((D/2 + Hs0 + Hs1)*np.tan(np.pi/Nm) -
           Tw/2/np.cos(np.pi/Nm))*2

    Aslot0 = (Bs1+Bs2)/2*Hs2 +\
        (Bs2-2*Rs)*Rs +\
        np.pi*Rs**2/2

    SlotLiner = 0.001

    Wedgethick = 0.001

    LayIns = 0.001

    ASlotWire = Aslot0 -\
        Hs2*LayIns -\
        Bs2*LayIns -\
        (2*Bs1+Bs2+2*Hs2/np.cos(np.pi/Nm))*SlotLiner -\
        Bs1*Wedgethick

    ErrorSlot = ASlotWire - Aslot

    return ErrorSlot


Hs2 = fs(SlotHeight, [100])

print(Hs2)
print(EMF)
print(Vt)
print(Iph)'''

'''# function definition
# Carter coefficient


def Carter(Bs0, TauSlot, geq): return \
    (1-2*Bs0/np.pi/TauSlot*(
        np.arctan(Bs0/2/geq) -
        geq/Bs0*np.log(1+1/4*(Bs0/geq)**2)
    ))**-1


def Inductance(Hs2, Nph):

    # Airgap inductance
    Lsg = 3/np.pi*(kw*Nph/(Np/2)) ^ 2*Mu0 /\
        (g + hm/MuPM)/Carter(Bs0, TauSlot, g + hm/MuPM) *\
        D*L*1e-3
    # Uppeer Slot width
    Bs2 = ((D/2 + Hs2 + Hs1 + Hs0)*np.tan(np.pi/Nm) -
           Tw/2/np.cos(np.pi/Nm))*2

    # Slot Inductance
    GammaSL = (2/3*Hs2/(Bs1 + Bs2) +
               2*Hs1/(Bs0 + Bs1) +
               Hs0/Bs0) *\
        (1 + 3*(TauSlot/TauPole)/4)

    Lsl = 2*Mu0*L*(Nph) ^ 2/(Np*q)*GammaSL

    # Slot area
    Aslot = (Bs1 + Bs2)/2*Hs2 +\
        (Bs2 - 2*Rs)*Rs +\
        np.pi*Rs**2/2

    # End Winding Inductance
    Lew = Mu0*TauSlot*Nph**2/16 *\
        np.log(np.pi*TauSlot**2 /
               4/Aslot)

    return Lsg + Lsl + Lew


def Resistance(Hs2, Nph):

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

    return Rph'''


'''
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



'''

'''def turnsfinding(Nph):

    EMF = 2*np.pi*f/np.sqrt(2) *\
        Nph*kw *\
        2/np.pi*BAirgap *\
        2*D*L/Np*1e-6

    Iph = Pmec/3/EMF

    TauSlot = np.pi*D/Nm

    Car =Carter(Bs0, TauSlot, g + hm/MuPM)

    Lm = 3/np.pi*(2*Nph/Np*kw)**2*Mu0 /\
        (g + hm/MuPM)/Car *\
        D*L*1e-3

    # Temporal value to Bs2

    Bs2 = 1.5*Bs1

    Baver = (Bs1+Bs2)/2

    Hs2 = 2*Tw

    Lslot = q*Np*(Nph*3*2/Nm)**2*Mu0 *\
        (Hs2*L/Baver+Hs1*L*2/(Bs1+Bs0)+Hs0*L/Bs0)*1e-3

    Lendwin = .05*Lslot

    ErrorEMF = (EMF+0.2*Iph)**2 +\
        (2*np.pi*f*(Lm+Lslot+Lendwin)*Iph)**2 -\
        Vt**2
    return ErrorEMF'''

'''    def TurnsFinding(Hs2Nph):

    Hs2 = abs(Hs2Nph[0])
    Nph = abs(Hs2Nph[1])

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

    # Condition for 
    Ncoilside = int((m*Nph*2)/(Nm*2))

    Nph = Ncoilside*2*Nm/2/m

    EMF = 2*np.pi*f/np.sqrt(2) *\
        Nph*kw *\
            2/np.pi*BAirgap *\
                2*D*L/Np*1e-6

    Iph = Pmec/3/EMF

    Dwire = 2*np.sqrt(Iph/J/np.pi)

    AWG = np.round(np.log(Dwire/8.251463)/np.log(0.8905257))

    DAWG = 8.251463*(0.8905257)*AWG

    Awire = np.pi*DAWG**2/4

    Acu = Awire*Np /\
        (q*Np/2)

    Aslot = Acu/Kfill

    Bs2 = ((D/2 + Hs0 + Hs1 + Hs2)*np.tan(np.pi/Nm) -
           Tw/2/np.cos(np.pi/Nm))*2

    Bs1 = ((D/2 + Hs0 + Hs1)*np.tan(np.pi/Nm) -
           Tw/2/np.cos(np.pi/Nm))*2

    Aslot0 = (Bs1+Bs2)/2*Hs2 +\
        (Bs2-2*Rs)*Rs +\
        np.pi*Rs**2/2

    SlotLiner = 0.001

    Wedgethick = 0.001

    LayIns = 0.001

    ASlotWire = Aslot0 -\
        Hs2*LayIns -\
        Bs2*LayIns -\
        (2*Bs1+Bs2+2*Hs2/np.cos(np.pi/Nm))*SlotLiner -\
        Bs1*Wedgethick

    # ErrorSlot calculation
    ErrorSlot = ASlotWire - Aslot

    return ErrorEMF, ErrorSlot'''