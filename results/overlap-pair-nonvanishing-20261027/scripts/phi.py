"""Handwritten rational evaluator, copied verbatim from the independent review.
Returns L**5 * Phi, not Phi itself. No sparse-polynomial table is read.
"""
from fractions import Fraction

def phi_direct(L,A,t):
 # Independent rational, factored evaluation; no use of sparse terms.
 R=Fraction(A,L); Z=t+2*R+1
 mu=2*L**2+L*(-8*R-5*Z+5)+6*R**2-7*R*Z-8*R+2*Z**2-4*Z-18
 eta=2*R*(R+2)+Z**2*(R-4)-Z*(R+4)*(2*R+1)
 Q=2*L**3+L**2*(-16*R-3*Z-9)+L*(38*R**2+4*R*Z+29*R-3*Z**2+36*Z-53)-24*R**3+32*R**2*Z-8*R**2-14*R*Z**2+40*R*Z+144*R+2*Z**3-18*Z**2+10*Z+126
 n2=-10*R*(R+2)**2-2*Z**2*(R**2-11*R-20)+5*Z*(R+2)*(R+4)*(2*R+1)
 n1=15*R*(R+2)**2*(5*R+4)-15*Z**3*(R**2+2*R-4)+Z**2*(43*R**3+52*R**2-80*R-180)-5*Z*(R+2)*(15*R**3+85*R**2+101*R+24)
 n0=-20*R**2*(R+2)**2*(7*R+12)+3*R*Z**4*(R+4)+R*Z**3*(23*R**2-88*R-304)-R*Z**2*(128*R**3+467*R**2+170*R-672)+10*R*Z*(R+2)*(14*R**3+98*R**2+171*R+50)
 return L**5*((L-4*R)*(5*R+10)*eta*Q+(L**2*n2+L*n1+n0)*mu)
