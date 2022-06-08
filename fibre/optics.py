import numpy as np
#import numpy.ma as ma
#from scipy.special import eval_legendre

def is_even(x):
    """check if value is even"""
    return x % 2 != 0


def manhatten_dist(i, j):
    return np.abs(i) + np.abs(j)

def chebyshev_dist(i, j):
    return np.max((np.abs(i), np.abs(j)))

def fresnel_t_s(n1, theta1, n2, theta2):
    """
    Calculate the complex amplitude transmission coefficient at a planar
    interface for s polarization.

    Parameters
    ----------
    n1: complex
        refractive index on incident side
    theta1: float
        incident angle in degrees
    n2: complex
        refractive index on outgoing side
    theta1: float
        outgoing angle in degrees
    """
    denom = n2*np.cos(theta2) + n1*np.cos(theta1)
    return 2*n1*np.cos(theta1)/denom

def fresnel_t_p(n1, theta1, n2, theta2):
    """
    Calculate the complex amplitude transmission coefficient at a planar
    interface for p polarization.

    Parameters
    ----------
    n1: complex
        refractive index on incident side
    theta1: float
        incident angle in degrees
    n2: complex
        refractive index on outgoing side
    theta1: float
        outgoing angle in degrees
    """
    denom = n2*np.cos(theta1) + n1*np.cos(theta2)
    return 2*n1*np.cos(theta1)/denom

def fresnel_r_s(n1, theta1, n2, theta2):
    """
    Calculate the complex amplitude reflection coefficient at a planar
    interface for s polarization.

    Parameters
    ----------
    n1: complex
        refractive index on incident side
    theta1: float
        incident angle in degrees
    n2: complex
        refractive index on non incident side
    """
    #theta2 = theta1 #law of reflection
    num =   n1*np.cos(theta1) - n2*np.cos(theta2)
    denom = n1*np.cos(theta1) + n2*np.cos(theta2)
    return num/denom

def fresnel_r_p(n1, theta1, n2, theta2):
    """
    Calculate the complex amplitude reflection coefficient at a planar
    interface for p polarization.

    Parameters
    ----------
    n1: complex
        refractive index on incident side
    theta1: float
        incident angle in degrees
    n2: complex
        refractive index on non incident side
    """
    #theta2 = theta1 #law of reflection
    num =   n2*np.cos(theta1) - n1*np.cos(theta2)
    denom = n2*np.cos(theta1) + n1*np.cos(theta2)
    return num/denom

def R(n1, theta1, n2):
    theta2 = snell(n1, theta1, n2)
    rs = fresnel_r_s(n1, theta1, n2, theta2)
    rp = fresnel_r_p(n1, theta1, n2, theta2)
    return 0.5*(np.abs(rs)**2 + np.abs(rp)**2)

def T(n1, theta1, n2):
    theta2 = snell(n1, theta1, n2)
    ts = fresnel_t_s(n1, theta1, n2, theta2)
    tp = fresnel_t_p(n1, theta1, n2, theta2)
    t =  0.5*(np.abs(ts)**2 + np.abs(tp)**2)
    t *= np.real(n2*np.cos(theta2)/(n1*np.cos(theta1)))
    return t

def snell(n1, theta1, n2):
    """
    Calculate the propagation angle in region 2 at a material interface

    Parameters
    ----------
    n1: complex
        refractive index on incident side
    theta1: float
        incident angle in degrees
    n2: complex
        refractive index on non incident side
    """
    return np.arcsin(np.clip((n1/n2)*np.sin(theta1), -1., 1.))
