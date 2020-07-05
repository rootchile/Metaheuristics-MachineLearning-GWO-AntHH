__author__ = 'INVESTIGACION'
import random as rn
from . import matrixUtility as mU
from . import heuristic as he
from . import timeUtility as tU

def getNewItem(lSolution, matrix, lHeuristic, row):
    # Preguntemos: Dado un valor de la heuristica. Esta en lSolution?
    estado = -1
    i = 0
    while estado == -1 :
        if lHeuristic[i] in  lSolution:
            estado = -1
        else:
            estado = i
        i = i + 1
    # Ya identificamos el que no esta, filtremos todos los que estan en una misma condicion
    seleccion = lHeuristic[lHeuristic[:,1]==lHeuristic[i,1],:] # Me da la lista, luego hacemos un random para seleccionar sobre todos
    estado = -1
    while estado == -1 :
        item = seleccion[rn.randint(0, len(seleccion))]
        if  item in lSolution:
            estado = -1
        else:
            estado = 0
            lSolution.add(item)
    return lSolution

def getNewColumn(pColumns):
    rnd = rn.randint(0, 10)
    #print 'El largo', len(pColumns)
    if rnd == 0:
        column = pColumns[rn.randint(0, len(pColumns)-1)]
    else:
        column = pColumns[0]
    return column

def getNewRow(pRows):
    # La eleccion es de los mas grandes a los mas pequenos
    #Primero obtenemos las filas que no estan cubiertas
    rnd = rn.randint(0, 10)
    #print 'El largo', len(pColumns)
    if rnd == 0:
        row = pRows[rn.randint(0, len(pRows)-1)]
    else:
        row = pRows[0]
    return row

def obtienenNuevoElemento(lSolucion, matrix, pesos, rHeuristic,dictcHeuristics,dict,cHeuristic):
    #Obtenemos las filas no cuviertas
    uRows = mU.getRows(matrix,lSolucion)
    #print 'Largo Filas', len(uRows)
    if len(uRows) > 0:
        #---------------------------------------------------------------------------------------------------------
        #La seleccion ed la heuristica
        #---------------------------------------------------------------------------------------------------------
        #column = he.SeleccionaColumna(matrix,lSolucion,cHeuristic)
        #column = he.SeleccionaColumna1(lSolucion,cHeuristic)
        column = he.SeleccionaColumna6(pesos,matrix,uRows,lSolucion)
        #---------------------------------------------------------------------------------------------------------
        #pColumns = he.getProposedColumnsDict(uColumns,dictcHeuristics,lparam=2)
        #column = getNewColumn(pColumns)

        lSolucion.append(int(column))
        estado = 0
    else:
        estado = 1
    return lSolucion, estado

def obtienenNuevoElemento1(lSolucion, matrix, pesos, rHeuristic,dictcHeuristics,dict,cHeuristic):

    #Obtenemos las filas no cuviertas
    uRows = mU.getRows(matrix,lSolucion)
    uColumns = []

    if len(uRows) > 0:

        pRows = he.getProposedRows(uRows,rHeuristic,lparam = 10 )

        #uColumns =  dict[uRows[0]]
        for i in range(0,len(pRows)):
            uColumns =  list(set(uColumns + dict[pRows[i]]))
        #print 'Las columnas', len(uColumns)
        pColumns = he.getProposedColumns(uColumns,cHeuristic,lparam=10)
        #pColumns = he.getProposedColumnsNew(uColumns,dictcHeuristics,lparam=50)


        #---------------------------------------------------------------------------------------------------------
        #La seleccion ed la heuristica
        #---------------------------------------------------------------------------------------------------------
        #column = he.SeleccionaColumnaNueva(pesos,matrix,pRows,pColumns)
        column = getNewColumn(pColumns)

        #---------------------------------------------------------------------------------------------------------

        lSolucion.append(int(column))
        estado = 0
    else:
        estado = 1
    return lSolucion, estado

def obtieneElemento(lSolucion, matrix, pesos, rHeuristic,dictcHeuristics,dict,cHeuristic):
    uRows = mU.getRows(matrix,lSolucion)
    if len(uRows) > 0:
        pRows = he.getProposedRows(uRows,rHeuristic,lparam = 10 )

        column = he.SeleccionaColumna6(pesos,matrix,pRows,lSolucion)
        lSolucion.append(int(column))
        estado = 0
    else:
        estado = 1
    return lSolucion, estado

def obtieneElemento2(lSolucion,matrix,pesos,rHeuristic,dictcHeuristics,dict,cHeuristic,dictCols):
#    tIni = tU.obtieneTime()
    uRows = mU.getRows(matrix,lSolucion)
    uColumns = []
    if len(uRows) > 0:
        pRows = he.getProposedRows(uRows,rHeuristic,lparam = 10 )
        #print ('pRows',pRows)
        for i in range(0,len(pRows)):
            uColumns =  list(set(uColumns + dict[pRows[i]]))
            #print ('uColumns',uColumns,dict)
            #print 'El numero de columnas', len(uColumns), pRows[i],dict[int(pRows[i])]

        #-----------------------------------------------------------------------------------------------
        # LAs Heuristicas
        #-----------------------------------------------------------------------------------------------
        #column = he.SeleccionaColumna6(pesos,matrix,pRows,lSolucion)

        #-----------------------------------------------------------------------------------------------
        # Muy Bien con Scheduling
        #-----------------------------------------------------------------------------------------------
        #column = he.SeleccionaColumnaNueva(pesos, matrix, pRows,uColumns)

        column = he.heuristByCols(pesos,uRows,uColumns,dictCols)

        lSolucion.append(int(column))
        estado = 0
    else:
        estado = 1
#    tFin = tU.obtieneTime()
    #print 'EL obtieneLEmento2', tIni, tFin
    return lSolucion, estado

def generaSolucion(lSolution,matrix,pesos,rHeuristic,dictcHeuristics,dict,cHeuristic,dictCol):
#    print(f'lSolution {type(lSolution)},matrix {type(matrix)},pesos {type(pesos)},rHeuristic {type(rHeuristic)},dictcHeuristics {type(dictcHeuristics)},dict {type(dict)},cHeuristic {type(cHeuristic)},dictCol {type(dictCol)}')
#    exit()
#    lSolution = list(lSolution)
    estado = 0
    contReparaciones = 0
#    tInicio = tU.obtieneTime()
    while estado == 0:
        #lSolution, estado = obtienenNuevoElemento1(lSolution,matrix,pesos,rHeuristic,dictcHeuristics,dict, cHeuristic)
        #lSolution, estado = obtienenNuevoElemento(lSolution,matrix,pesos,rHeuristic,dictcHeuristics,dict, cHeuristic)
        #lSolution, estado = obtieneElemento(lSolution,matrix,pesos,rHeuristic,dictcHeuristics,dict, cHeuristic)
        lSolution, estado = obtieneElemento2(lSolution,matrix,pesos,rHeuristic,dictcHeuristics,dict,cHeuristic,dictCol)
        contReparaciones += 1

#    tFin = tU.obtieneTime()
    #print tInicio, tFin

    #tFin = tU.obtieneTime()
    #print 'Solucion nueva', tInicio,tFin

    return lSolution, contReparaciones