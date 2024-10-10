#1
def toBase2(number):
    resultString=""
    if number==0:
        return "0"
    while number > 0:
        resultString=str(number%2) + resultString
        number//=2
    return resultString


number = input("introdu numar: ")
print("numarul in baza 2: " + toBase2(int(number)) )


#2
def b2To16(number):
    nrString=str(number)
    while len(nrString)%4 != 0:
        nrString="0"+nrString
    
    resultString=""
    index=0
    while index*4<len(nrString):
        sum=0
        sum= int(nrString[0+index*4])*(2**3)+ int(nrString[1+index*4])*(2**2) + int(nrString[2+index*4])*(2**1) + int(nrString[3+index*4])*(2**0)
        if sum < 10:
            resultString+=str(sum)
        else:
            resultString+=str(chr(sum-10+65))
        index+=1
    return "0x"+resultString

numar=input("introdu numar in baza 2: ")
print(b2To16(int(numar)))     
       
#3
def pb3(text,numar):
    resultString=""
    while numar>0:
        resultString=text[numar%4] + resultString
        numar//=4
    return resultString

text=input("intordu sir: ")
numar= int(input("intordu numar: "))

print("rezultat: "+pb3(text,numar))

#4
def b10Tob16(numar):
    return b2To16(toBase2(numar))

numar=int(input("introdu numar in baza 10: "))
print("rezultat in baza 16: "+b10Tob16(numar))

#5 
def checkParanteze(expresie):
    counter=0
    foundOpenParanthesis = False

    for caracter in expresie:
        if caracter == "(":
            foundOpenParanthesis=True
            counter+=1
        elif caracter == ")":
            if foundOpenParanthesis==False:
                return False
            counter-=1
    if counter == 0:
        return True
    return False

expresie = input("introdu expresie: ")
print("parantezele sunt ok? " + str(checkParanteze(expresie)))
