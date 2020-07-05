#  Author: Diego Tapia R.
#  E-mail: root.chile@gmail.com - diego.tapia.r@mail.pucv.cl
import numpy as np

#Gracias Mauricio Y Lemus!
from .repair import ReparaStrategy as repara
from Discretization import DiscretizationScheme as DS


#action : esquema de discretizacion DS
def SCP(solucion,costos,cobertura,ds):

    repair = repara.ReparaStrategy(cobertura, costos, cobertura.shape[0],cobertura.shape[1])

    ds = ds.split(",")
    ds = DS.DiscretizationScheme(solucion,ds[0],ds[1])

    solucion = ds.binariza()

    if repair.cumple(solucion):
        return solucion, np.sum(costos*solucion)

    solucion, num_rep = repair.repara_one(solucion)

    return solucion, np.sum(costos*solucion)


