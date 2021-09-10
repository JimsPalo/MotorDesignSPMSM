'''
Created on Jun 18, 2021

@author: Jimmy Palomino

'''
import numpy as np

def WindingLayout(main):

    # Slots number
    Qs = main['ANSYS']['Specifications']['Qs']

    # Pole number
    p = main['ANSYS']['Specifications']['Poles']

    # Phase number (Fixed assumption)
    m = 3

    # Relation simplified for q = Qs/m/p = b/c
    b = int(Qs/np.gcd(Qs, p*m))
    c = int(p*3/np.gcd(Qs, p*m))

    # Sequence definition 
    sequence = np.zeros(c)

    SpanForOnes = int(c/b)

    # Location ones in the sequence
    OnePosition, CountOnes = 0, 0
    while (OnePosition<c) and (CountOnes<b):
        sequence[OnePosition]=1
        OnePosition += SpanForOnes
        CountOnes += 1

    # Array repeated Qs/b times
    sequence = list(sequence)
    SequenceComplete = []
    for k in range(int(Qs/b)):
        SequenceComplete += sequence

    # Arranges each phase
    A, B, C, slot = [], [], [], 1
    for i, k in enumerate(SequenceComplete):
        if int(k)==1:
            SlotOut = slot+1 if slot != Qs else 1
            if i%6 == 0:
                A += [slot, -SlotOut]
            elif i%6 == 1:
                C += [slot, -SlotOut]
            elif i%6 == 2:
                B += [slot, -SlotOut]
            elif i%6 == 3:
                A += [-slot, SlotOut]
            elif i%6 == 4:
                C += [-slot, SlotOut]
            elif i%6 == 5:
                B += [-slot, SlotOut]
            slot += 1

    # Fem (pu) for each coil side definition
    E = np.sign(A)*np.exp(1j*p*np.pi/Qs*np.abs(np.array(A)))

    # magnitude of Fem (pu) induced by phase
    ETotal = np.abs(np.sum(E))

    # Winding factor
    kw = ETotal/(2*Qs/m)

    main['ANSYS']['Winding']['ABC'] = [A, B, C]
    main['ANSYS']['Winding']['kw'] = kw

    return main

    



