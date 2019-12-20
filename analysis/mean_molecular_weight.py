import numpy as np


def get_mu( dens, HI_dens, HII_dens, HeI_dens, HeII_dens, HeIII_dens   ):
  mu =  dens / ( HI_dens + 2*HII_dens + ( HeI_dens + 2*HeII_dens + 3*HeIII_dens) / 4 )
  return mu
  
h_frac = 0.75984
he_frac = 1 - h_frac

dens = 1
#Neutral gas
HI_dens = h_frac * dens
HII_dens = 0
HeI_dens = he_frac * dens
HeII_dens = 0
HeIII_dens = 0
mu_neutral = get_mu( dens, HI_dens, HII_dens, HeI_dens, HeII_dens, HeIII_dens,   )

# 
# #Ionized gas
# HI_dens = 0
# HII_dens = h_frac * dens
# HeI_dens = 0
# HeII_dens = 0
# HeIII_dens = he_frac * dens
# mu_ionized = get_mu( dens, HI_dens, HII_dens, HeI_dens, HeII_dens, HeIII_dens,   )
# 


n_h = 1.
n_he = 0.1
# n_he = 0.08232
mu = ( n_h + 4*n_he ) / ( n_h + n_he )
X = n_h / ( n_h + 4*n_he )
Y = 1 - X
mu_0 = 1/( X + Y/4)

# n_he = he_frac / 4
# HeI_dens_1 = 4 * n_he
# HI_dens_1= dens - HeI_dens_1


# mu = get_mu( dens, HI_dens_1, HII_dens, HeI_dens_1, HeII_dens, HeIII_dens,   )


# mu = n_h + 4*n_he / ( n_h + n_he )  