
# coding: utf-8

# In[100]:


# ------------------------------------------------ ### PROBLEMA DA DIETA ### ------------------------------------------------

#       Tenta resolver o problema de dado N elementos e M caracteristicas escolher K porções de cada elemento tal que a seguinte 
# lei não é violada:
# => Somatório[i até N] (xi*mij) <= ou >= Tj (xi é o K do elemento i, e mij é a j-éssima caracteristica, indo até M, do i-éssimo 
# elemento) e Tj é um valor dado. Isso deve ser verdade para todas as M características dadas.

import numpy as np
import math
from random import randrange, uniform
from scipy.optimize import linprog


# In[101]:


# Vamos criar um exemplo de problema, será importante para nós no futuro!

numberElements = 5
numberCharacteristcs = 10
space = 100

file = open('problem ' + str(numberElements) + '-' + str(numberCharacteristcs) + '.txt', 'w')

file.write(str(numberElements) + '\n')
file.write(str(numberCharacteristcs) + '\n')
for i in range(numberElements):
    for j in range(numberCharacteristcs):
        file.write(str(randrange(0, space)) + ' ')
    file.write(str(randrange(0, space / 10)))
    file.write('\n')
for j in range(numberCharacteristcs + 1):
        file.write(str(randrange(space * 4, space * 10)) + ' ')

file.close()


# In[102]:


# Vamos ler agora os exemplos criados

#file = open('problem ' + str(numberElements) + '-' + str(numberCharacteristcs) + '.txt', 'r')
file = open('real problem.txt' , 'r')

nE = int(file.readline())
nC = int(file.readline())

matrix = np.zeros((nE+1,nC+1))
for i in range(nE + 1):
    aux = (file.readline().split())
    matrix[i] = [float(item) for item in aux]
matrix[-1][-1] = 0

print(matrix) 


# In[103]:


# Após ler os exemplos vamos achar uma resposta para a solução, primeiro de tudo vamos setar as listas a seguir

variables = [0] * nE # Lista das variáveis a serem usadas
constraints = [0] * nC # Lista de restrições, ou seja, xi*mij => variables[i]*matrix[i][j]

# Função para decidir se é viável
def isViable(constraint, j):
    return constraint <= matrix[nE][j]

# Vamos criar uma função para calcular a lista dos constraints
def calcConstraints():
    for j in range(nC):
        aux = 0
        for i in range(nE):
            flag = True
            while flag:
                aux = aux + (variables[i] * matrix[i][j])
                if isViable(aux, j):
                    flag = False
                else:
                    variables[i] = uniform(0, space)
        constraints[j] = aux
    return constraints

# E agora a função objetiva
def calcObjFunction():
    aux = 0
    for i in range(nE):
        aux = aux + (matrix[i][nC] * variables[i])
    return aux

def inv(x):
    return x * (-1)


# In[106]:


#Agora vamos tentar achar a solução por tentativa, queremos a menor função objetiva!!

# minimizar c quando A_lb >= b, adaptando
# minimizar c quando A_ub * (-1) <= b * (-1)

# Tratando c
# Valores de c = [x[nC] for x in matrix]
# A função optmizations.linprog() sempre minimiza

objFun = [x[nC] for x in matrix]
del objFun[-1]
#objFun = [i*(-1) for i in objFun] #caso queiramos maximizar

print(f'Funcao Objetiva: {objFun}')

#Tratando A_lb
#Valores de A_lb = matrix[0:nE][0:nC-1])
A_lb = list()

for j in range(nC):
    A_lb.append(list())
    for i in range(nE):
        A_lb[j].append(inv(matrix[i][j])) #função inv inverte o valor da A, pois a inequação é >=.

print(f'Coeficientes: {A_lb}')

#Tratando b
#Valor de b = matrix[nE][0:nC]

b = list()
for i in matrix[nE]:
    b.append(inv(i)) #função inv inverte o valor da b, pois a inequação é >=.
    
del b[-1]
print(f'Valores Nutricionais Mínimos: {b}')

#Tratando os limites
x_bnds = list()

for i in range(nE):
    x_bnds.append((0.1, None))
x_bnds[2] = (0.5, None)
x_bnds[5] = (0, 1)
print(f'Limites {x_bnds}')

res = linprog(objFun, A_lb, b, bounds=(x_bnds))
print(res)        


# In[109]:


file = open('result.txt', 'w')

file.write(str(res))
print("Archive printed in .txt successfully!!")

file.close()

