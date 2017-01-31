#!/usr/bin/env python 
import random
from collections import Counter
respostas= {}
gaussian={}
def addgaussian(fala,resposta):
    gaussian[fala].append(resposta)
def testcommon(fala,resposta):
    mcommon = [ key for key, valor in Counter(gaussian[fala]).most_common(1)]
    if not mcommon[0] == respostas[fala].index(resposta):
        addgaussian(fala,respostas[fala].index(resposta))
def testexist(fala,resposta):
    if fala not in respostas:
        respostas[fala]=[]
        gaussian[fala]=[]
    if resposta not in respostas[fala]:
        respostas[fala].append(resposta)
    if not gaussian[fala]:
        addgaussian(fala,respostas[fala].index(resposta))



def main(time,fala):
    if time=="ppl":
        if fala=='':
            fala=input('you:')
            resposta=fala
        else:
            resposta=input('you:')
        testexist(fala,resposta)
        testcommon(fala,resposta)
        main("pc",resposta)
    else:
        resposta=fala
        testexist(fala,resposta)
        nperg=random.choice(gaussian[fala])
        perg=respostas[fala][nperg]
        print("pc:",perg)
        main('ppl',perg)



main("ppl",'')


