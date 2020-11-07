#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:36:14 2020
@author: Bernardo Bresolini
@author: Thalles Campagnani
    Codigo usado para computar a matriz de transformaçao homogenea de n para 0.
    É preciso ser inserido a tabela DH na ordem:
                   alf,   a,    d,   theta
    É necessario ter instalado a biblioteca SymPy e NumPy. Em plataformas Linux, basta fazer
    LINUX:
        1) Abra o prompt de comando:
            CTRL + ALT + T
        2) Digite:
            python3 -m pip install sympy numpy
    Caso esteja no Windows e o Python tenha sido instalado via Anaconda, SymPy ja vem
    instalado, mas talvez possa ser necessario atualiza-lo fazendo
    WINDOWS:
        conda update sympy numpy
    Mais informaçoes podem ser obtidas em>
        <https://docs.sympy.org/latest/>
"""

import numpy as np
from numpy import eye
import sympy as sp    # Pacote para manipulaçoes simbolicas
from sympy import pi, cos, sin
from sympy.physics.vector import init_vprinting   # Usada para printar em latex
from sympy.physics.mechanics import dynamicsymbols

init_vprinting(use_latex='mathjax', pretty_print=False)   # Configurando o vprinting


def DH (rows,TDH):
    #rows = len(TDH) #Linhas de TDH

    theta, alpha, a, d = dynamicsymbols('theta alpha a d')
    # Rotação de theta/ em z com Rotação de alpha em x
    Rot = sp.Matrix([[cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha)],
                    [ sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha)],
                    [         0,              sin(alpha),             cos(alpha)]])

    # Translação dos links
    Tran = sp.Matrix([a*cos(theta),a*sin(theta),d])

    # Distorção e Escala
    S = sp.Matrix([[0, 0, 0, 1]])

    # Matriz A genérica
    A = sp.Matrix.vstack(sp.Matrix.hstack(Rot, Tran), S)

    # Matriz A de cada linha
    Ai = []
    for i in range(0,rows):
        Ai.append(A.subs({ alpha:TDH[i,0], a:TDH[i,1], d:TDH[i,2], theta:TDH[i,3] }))
        #print(Ai[i])

    # Matriz de transformação do end-effector para base
    T = eye(4)
    print("\n")
    for i in range(0,rows):
        #print("\n")
        #print(T)
        T = T*Ai[i]
    #print(T)
    return T

def ROT (eixo,angulo):
    if eixo == 'x':
        return sp.Matrix([[                   1,            0,             0,             0],
                          [                   0,  cos(angulo),  -sin(angulo),             0],
                          [                   0,  sin(angulo),   cos(angulo),             0],
                          [                   0,            0,             0,             1] ])
    else:
        if eixo == 'y':
            return sp.Matrix([[     cos(angulo),            0,   sin(angulo),             0],
                              [               0,            1,             0,             0],
                              [    -sin(angulo),            0,   cos(angulo),             0],
                              [               0,            0,             0,             1] ])
        else:
            if eixo == 'z':
                return sp.Matrix([[ cos(angulo), -sin(angulo),             0,             0],
                                  [ sin(angulo),  cos(angulo),             0,             0],
                                  [           0,            0,             1,             0],
                                  [           0,            0,             0,             1] ])
            else:
                return -1


def TRANS (eixo,distancia):
    if eixo == 'x':
        return sp.Matrix([[1, 0, 0, distancia],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1] ])
    else:
        if eixo == 'y':
            return sp.Matrix([[1, 0, 0, 0],
                              [0, 1, 0, distancia],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1] ])
        else:
            if eixo == 'z':
                return sp.Matrix([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, distancia],
                                  [0, 0, 0, 1] ])
            else:
                return -1

def THETA(qtd):
    theta = [0]
    for i in range(1,qtd+1):
        theta.append(dynamicsymbols('theta'+str(i)))
    return theta

def L(qtd):
    l = [0]
    for i in range(1,qtd+1):
        l.append(dynamicsymbols('l'+str(i)))
    return l

def valid(T,theta,Q,l,L):
    if T == [] or theta == [] or l == []:
        return -1
    else:
        if Q != []:
            for i in range(1,len(Q)+1):
                if Q[i-1] != []:
                    T = T.subs({theta[i]:Q[i-1]})
        if L != []:
            for i in range(1,len(L)+1):
                if L[i-1] != []:
                    T = T.subs({l[i]:L[i-1]})
    return T

def valid_euler(x,y,z,a,b,c):
    return TRANS('x',x) * TRANS('y',y) * TRANS('z',z) * ROT('z',a) *  ROT('y',b) *  ROT('z',c)

def print_compacto(matriz):
    matris = str(matriz)#'\n'.join(map(str, list))
    matris = matris.replace("Matrix([","")
    matris = matris.replace("]])","]")
    matris = matris.replace("], ","]\n")
    matris = matris.replace("1.0*","")
    matris = matris.replace("1.00000000000000","1")
    matris = matris.replace("(t)","")
    matris = matris.replace("theta","")
    matris = matris.replace("sin","s")
    matris = matris.replace("cos","c")
    matris = matris.replace("(1)","1")
    matris = matris.replace("(2)","2")
    matris = matris.replace("(3)","3")
    matris = matris.replace("(4)","4")
    matris = matris.replace("(5)","5")
    matris = matris.replace("(6)","6")
    matris = matris.replace("(7)","7")
    print(matris)
    print("\n\n")
    #print(matriz)

def print_expandido(matriz):
    matris = str(matriz)#'\n'.join(map(str, list))
    matris = matris.replace("s1","sin(theta1(i))")
    matris = matris.replace("s2","sin(theta2(i))")
    matris = matris.replace("s3","sin(theta3(i))")
    matris = matris.replace("s4","sin(theta4(i))")
    matris = matris.replace("s5","sin(theta5(i))")
    matris = matris.replace("s6","sin(theta6(i))")
    matris = matris.replace("s7","sin(theta7(i))")
    matris = matris.replace("c1","cos(theta1(i))")
    matris = matris.replace("c2","cos(theta2(i))")
    matris = matris.replace("c3","cos(theta3(i))")
    matris = matris.replace("c4","cos(theta4(i))")
    matris = matris.replace("c5","cos(theta5(i))")
    matris = matris.replace("c6","cos(theta6(i))")
    matris = matris.replace("c7","cos(theta7(i))")
    matris = matris.replace("r11","POSE(1,1)")
    matris = matris.replace("r12","POSE(1,2)")
    matris = matris.replace("r13","POSE(1,3)")
    matris = matris.replace("r21","POSE(2,1)")
    matris = matris.replace("r22","POSE(2,2)")
    matris = matris.replace("r23","POSE(2,3)")
    matris = matris.replace("r31","POSE(3,1)")
    matris = matris.replace("r32","POSE(3,2)")
    matris = matris.replace("r33","POSE(3,3)")
    print(matris)
    print("\n\n")
    #print(matriz)

def main():
    # Variáveis simbólicas
    theta = THETA(7) #Quanridade de Juntas
    l = L(4)         #Quantidade de Links

    # Matriz DH:        alfi,     ai,      di,     theta
    TDH = sp.Matrix([ [-pi/2,   0,       l[1],     theta[1]],
                      [ pi/2,   0,          0,     theta[2]],
                      [ pi/2,   0,       l[2],     theta[3]],
                      [-pi/2,   0,          0,     theta[4]]])


    TDH2= sp.Matrix([ [-pi/2,   0,       l[3],     theta[5]],
                      [ pi/2,   0,          0,     theta[6]],
                      [    0,   0,       l[4],     theta[7]]])

    TDH3= sp.Matrix([ [-pi/2,   0,       l[1],     theta[1]],
                      [ pi/2,   0,          0,     theta[2]],
                      [ pi/2,   0,       l[2],     theta[3]],
                      [-pi/2,   0,          0,     theta[4]],
                      [-pi/2,   0,       l[3],     theta[5]],
                      [ pi/2,   0,          0,     theta[6]],
                      [    0,   0,       l[4],     theta[7]]])

    #Transformação A3
    #A3 = ROT('z',theta[3])* TRANS('x',l[4]) * ROT('y',pi/2) * ROT('z',pi/2)
    #Matriz de Transformação Homogenea
    #T = DH(4,TDH) #* A3
    #print(A3)
    #print("\n")
    print_compacto(DH(4,TDH))
    print_compacto(DH(3,TDH2))
    #print_compacto(DH(7,TDH3))
    #print_compacto(valid(T,theta,[-30,-30,-30,-30],l,[[],[],[],[]]))
    #print("\n\n\n")

    # Validação: home (todas as juntas em 0)
    #print(valid(T,theta,[0,0,0],l,[]))
    #print("\n\n\n")

    # Validação 2: outros valores
    #T_ = valid(T,theta,[45/180*pi,30/180*pi,-30/180*pi],l,[0.2,[],0.3,0.3])
    #print(T_)
    #print(np.asarray(T_).astype(np.float64))

    #print("\n\n\n")
    #print(np.asarray(ROT('z',-pi/2)*ROT('y',-pi/2)*ROT('z',-pi/4)).astype(np.float64))
    #print(np.asarray(ROT('z',pi*135/180)*ROT('x',pi)).astype(np.float64))
    #print("\n\n\n")
    #print(ROT('y',theta[2])*ROT('x',theta[2])*ROT('y',theta[3])*TRANS('x',l[3]))
    
    #R13
    print_expandido("r23*(c4*(c1*s3 + c2*c3*s1) + s1*s2*s4) - r13*(c4*(s1*s3 - c1*c2*c3) - c1*s2*s4) + r33*(c2*s4 - c3*c4*s2)")
    #R23
    print_expandido("r23*(c1*c3 - c2*s1*s3) - r13*(c3*s1 + c1*c2*s3) + r33*s2*s3")
    #R31
    print_expandido("r11*(s4*(s1*s3 - c1*c2*c3) + c1*c4*s2) - r21*(s4*(c1*s3 + c2*c3*s1) - c4*s1*s2) + r31*(c2*c4 + c3*s2*s4)")
    #R32
    print_expandido("r12*(s4*(s1*s3 - c1*c2*c3) + c1*c4*s2) - r22*(s4*(c1*s3 + c2*c3*s1) - c4*s1*s2) + r32*(c2*c4 + c3*s2*s4)")
    #R33
    print_expandido("r13*(s4*(s1*s3 - c1*c2*c3) + c1*c4*s2) - r23*(s4*(c1*s3 + c2*c3*s1) - c4*s1*s2) + r33*(c2*c4 + c3*s2*s4)")






main()
