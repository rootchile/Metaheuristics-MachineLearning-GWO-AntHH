__author__ = 'INVESTIGACION'

def getRows(matrix, columns):
    """
        Entrega las filas que no cubren la lista columns
        Let go to iterate by row.
        For each row we ask to the actual total column, if these contain the row
        If the row is not contain, then ad to R
        Else, nothing to do.
    """
#    print(columns)
#    exit()
    R = []
    row, col = matrix.shape
    
#    print(f'matrix {columns}')
#    columns = list(columns)
    #print 'Las Filas y Columnas', row, col, len(columns)
    for i in range(0, row):
#        print(f'i,columns {type(i)} {type(columns)}')
        
        if sum(matrix[i,columns]) == 0:
            R.append(i)
#        exit()
    return R

#def checkcolumSolution(column,lsolution):
#    state = 0 # The column is not in the solution
#    while state == 0:

#    return state

def getColumn(row, matrix, lsolution, lHeuristic):
    """
    :param row: the Row that are not cover
    :param matrix: Matrix of row and covered column
    :param lHeuristic: List with the weight of the heuristic associates to a each column
    :return: The best column
    """
    #Primero iteramos por la lista de heuristica
    estado = 0
    i = 0
    column = 0
    while estado ==0:
        cColumns = lHeuristic[i] #The Candidates column
        # The column is right now in the solution?
        # We have to verify if this column covers some row
        i = i + 1
    return column


#file = 'scpnrg3.txt'
#dirIn= 'C:/Optimization/SCP/OR/G/'
#pesos, matrix = rOP.generaMatrix(file,dirIn)
#columns = [3,76,78,90,340,567]
#fechaInicio = tU.obtieneTime()
#getRows(matrix,columns)
#fechaFin = tU.obtieneTime()
#print fechaInicio,fechaFin

