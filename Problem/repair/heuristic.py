__author__ = 'INVESTIGACION'
import numpy as np
from copy import deepcopy
import math

def getHeuristic(matrix, pesos):
    """
    Vamos a utilizar Cj/Pj donde Pi se obtiene por el numero de filas que cubre la columna
    :param matrix:
    :param pesos:
    :return:
    """
    lHeuristic = np.zeros((len(pesos),2)) # Dos columnas. La primera para indicar la columna la segunda para la Heuristica
    for i in range(0,len(pesos)):
        lHeuristic[i,0] = int(i)
        #print i,sum(matrix[:,i]), pesos[i], float(pesos[i]/sum(matrix[:,i]))
        lHeuristic[i,1] = float(pesos[i]/sum(matrix[:,i]))

        #lHeuristic[lHeuristic[:,1].argsort()]
    return lHeuristic[lHeuristic[:,1].argsort()]

def getRowHeuristics(matrix):
    """
    Para cada fila, calculamos como es cubierta y obtenermos 1/Cubrimiento. Mientras menos cubrimiento mas importante es
    :param matrix:
    :return:
    """
    row, col = matrix.shape
    rHeuristic = np.zeros((row,2)) # Dos columnas. La primera para indicar la columna la segunda para la Heuristica
    for i in range(0,row):
        rHeuristic[i,0] = int(i)
        #print (i,sum(matrix[:,i]), pesos[i], float(pesos[i]/sum(matrix[:,i])))
        rHeuristic[i,1] = 1/sum(matrix[i,:])
    return rHeuristic[rHeuristic[:,1].argsort()]

def getRowColumn(matrix):
    #Corresponde a un diccionario que tiene las columnas asociadas a una Fila
    nrow, ncol = matrix.shape
    dict = {}
    for i in range(0,nrow):
        list = []
        for j in range(0,ncol):
            if matrix[i,j]==1:
                list.append(j)
        dict[i] = deepcopy(list)
    return dict

def getColumnRow(matrix):
    #Corresponde a un diccionario que tiene las columnas asociadas a una Fila
    nrow, ncol = matrix.shape
    dictCol = {}
    for j in range(0,ncol):
        list = []
        for i in range(0,nrow):
            if matrix[i,j]==1:
                list.append(i)
        dictCol[j] = deepcopy(list)
    return dictCol

def getProposedRows(uRows,rHeuristic,lparam):
    """
    :param uRows: Uncovered rows
    :param rHeuristic: Rows Heuristic
    :param lparam: Number of rows proposed
    :return: pRows proposed rows
    """
    pRows = []
    contador = 1
    if len(uRows) < lparam:
        pRows = uRows
    else:
        while len(pRows) < lparam:
            if  rHeuristic[len(rHeuristic)-contador,0] in uRows:
                pRows.append(rHeuristic[len(rHeuristic)-contador,0])
            contador = contador + 1
            if contador > len(rHeuristic):
                break
    return pRows

def getProposedColumns(uColumns, cHeuristic,lparam):
    """
    :param uRows: Uncovered rows
    :param rHeuristic: Rows Heuristic
    :param lparam: Number of rows proposed
    :return: pRows proposed rows
    """
    pColumns = []
    contador = 0
    #print 'Cuantas columnas propuestas', len(uColumns)

    while len(pColumns) < lparam:
        #print uColumns
        if  cHeuristic[contador,0] in uColumns:
            pColumns.append(cHeuristic[contador,0])
        if contador == len(cHeuristic)-1:
            break
        contador = contador + 1
    return pColumns

def getProposedColumnsNew(uColumns, dictcHeuristics ,lparam):
    """
    :param uRows: Uncovered rows
    :param rHeuristic: Rows Heuristic
    :param lparam: Number of rows proposed
    :return: pRows proposed rows
    """
    pColumns = []
    tColumns = np.zeros((len(uColumns),2))
    contador = 0
    #print 'Cuantas columnas propuestas', len(uColumns)

    for i in range(0,len(uColumns)):
        tColumns[i,0] = uColumns[i]
        tColumns[i,1] = dictcHeuristics[uColumns[i]]


    return  tColumns[tColumns[:,1].argsort()][0:lparam,0]

def getProposedColumnsDict(uColumns,dictcHeuristics,lparam):

    pColumns = []
    tColumns = np.zeros((len(uColumns),2))
    for i in range(0,len(uColumns)):
        tColumns[i,0] = uColumns[i]
        tColumns[i,1] = dictcHeuristics[uColumns[i]]
    tColumns = tColumns[tColumns[:,1].argsort()]
    largo = min(lparam, len(tColumns[:,0]))
    for i in range(0,largo):
        pColumns.append(tColumns[i,0])
    return pColumns

def getColumnsDict(cHeuristic):
    dictcHeuristics = {}
    for i in range(0,len(cHeuristic)):
        dictcHeuristics[cHeuristic[i,0]] = cHeuristic[i,1]
    return dictcHeuristics

def diff(A,B):
    C = set(A) -set(B)
    return list(C)

def Calcula_Measure_j(Option, Pesos,j, K_j):
    """
    :param Option:  Identify the Measure 0 Cost, 1 Normalize Cost,
    :param Pesos:   Is a variable in the measure calculus
    :param Matrix:  Column by row information
    :param j:       Column used for the calculus
    :return:        The measure
    """
    if Option==0:
        Measure = Pesos[j]

    elif Option==1:
        Measure = Pesos[j]/K_j

    elif Option==2:
        Measure =  (Pesos[j]/math.log(K_j,2))

    return Measure

def SeleccionaColumna(Matrix,S,cHeuristic):

    row, col = Matrix.shape
    columnTot = range(0,col)
    columnComplement = diff(columnTot,S)
    estado = 0
    i = 0
    while estado == 0:
        if cHeuristic[i,0] in columnComplement:
            column = cHeuristic[i,0]
            estado = 1
        i = i + 1
    return column

def SeleccionaColumna1(S,cHeuristic):
    estado = 0
    i = 0
    while estado == 0:
        if cHeuristic[i,0] not in S:
            column = cHeuristic[i,0]
            estado = 1
        i = i + 1
    return column

def SeleccionaColumna6(Pesos, Matrix, R,S):
    """
    :param Pesos:   Is a variable in the measure calculus
    :param Matrix:  Column by row information
    :param R:       Uncovered Row
    :param S:       Column in solution
    """


    NumberCalculus = 2

    T = 1 # start choice
    Option1 = np.random.randint(0,9)
    #Option = np.random.randint(2)
    Option = 1
    #Choice = np.random.randint(0,T)
    rows, cols = Matrix.shape
    compl = range(0,cols)
    columnComplement = list(set(compl)-set(S))
    Matrix_F = Matrix[R,:]

    Matrix_F = Matrix_F[:,columnComplement]

    rowF, colF = Matrix_F.shape
    #print rowF, colF
    ColumnWeight = np.zeros((colF,NumberCalculus))
    Cont = 0

    for i in range(0,colF):

        ColumnWeight[Cont,0] = columnComplement[i]
        K_i = np.sum(Matrix_F[:,i])
        if K_i > 0:
            ColumnWeight[Cont,1] = Calcula_Measure_j(Option,Pesos,columnComplement[i],K_i)
        else:
            ColumnWeight[Cont,1] = Pesos[columnComplement[i]]*100
        Cont = Cont + 1
    ColumnWeight = ColumnWeight[ColumnWeight[:,1].argsort()]

    # We need to get the S complement
    if Option1 == 0:
        #print tam, Option1, len(ColumnWeight)
        tam = min(len(ColumnWeight),10)
        #print 'El largo', len(ColumnWeight)
        if tam == 1:
            column = int(ColumnWeight[0,0])
        else:
            column = int(ColumnWeight[np.random.randint(1,tam),0])
    else:
        column = int(ColumnWeight[0,0])
        #print 'La columna', column
    return column

def SeleccionaColumnaNueva(Pesos, Matrix, pRows,pColumns):
    """
    :param Pesos:   Is a variable in the measure calculus
    :param Matrix:  Column by row information
    :param R:       Uncovered Row
    :param S:       Column in solution
    """


    NumberCalculus = 2

    T = 1 # start choice

    Option = np.random.randint(2)
    #Choice = np.random.randint(0,T)

    row, col = Matrix.shape
    #print 'El largo de las columnas antes', len(pColumns)
    columnComplement = list(set(pColumns).intersection(range(0,col)))
    #print 'El largo de las columnas ', len(columnComplement), pColumns
    Matrix_F = Matrix[pRows,:]

    Matrix_F = Matrix_F[:,columnComplement]
    rowF, colF = Matrix_F.shape


    ColumnWeight = np.zeros((colF,NumberCalculus))

    Cont = 0

    for i in range(0,colF):

        ColumnWeight[Cont,0] = columnComplement[i]
        K_i = np.sum(Matrix_F[:,i])
        if K_i > 0:
            ColumnWeight[Cont,1] = Calcula_Measure_j(Option,Pesos,columnComplement[i],K_i)
        else:
            ColumnWeight[Cont,1] = Pesos[columnComplement[i]]*100
        Cont = Cont + 1
    ColumnWeight = ColumnWeight[ColumnWeight[:,1].argsort()]

    # We need to get the S complement

    #tam = min(len(ColumnWeight)-1,9)

    Option1 = np.random.randint(0,5)
    if Option1 == 0:
        #print tam, Option1, len(ColumnWeight)
        tam = min(len(ColumnWeight),10)
        #print 'El largo', len(ColumnWeight)
        #print tam
        if tam == 1:
            column = int(ColumnWeight[0,0])
        else:
            column = int(ColumnWeight[np.random.randint(1,tam),0])
    else:
        #print len(ColumnWeight), len(pRows), len(columnComplement)
        column = int(ColumnWeight[0,0])
    #print 'El calculo', column
    return column

def heuristByCols(pesos,uRows,pCols,dictCols):
    ColumnWeight = np.zeros((len(pCols),2))
    #print('pcols',len(pCols))
    for i in range(0,len(pCols)):
        lRows = dictCols[pCols[i]]
        ColumnWeight[i,0] = pCols[i]
        ColumnWeight[i,1] = float(pesos[pCols[i]])/len(list(set(lRows).intersection(set(uRows))))
    ColumnWeight = ColumnWeight[ColumnWeight[:,1].argsort()]
    Option1 = np.random.randint(0,5)
    if Option1 == 0:
        #print tam, Option1, len(ColumnWeight)
        tam = min(len(ColumnWeight),10)
        #print 'El largo', len(ColumnWeight)
        #print tam
        if tam == 1:
            #print('El valor del elemento',ColumnWeight[0,0])
            column = int(ColumnWeight[0,0])
        else:
            #print('El valor del elemento',ColumnWeight[0,0])
            column = int(ColumnWeight[np.random.randint(1,tam),0])
    else:
        #print len(ColumnWeight), len(pRows), len(columnComplement)
        #print('El valor del elemento',ColumnWeight[0,0])
        column = int(ColumnWeight[0,0])
    #print 'El calculo', column
    return column