#1
input1=input("#1 introdu numere:")
def cmmdc(a, b):
    while b != 0:
        a, b = b, a % b  
    return a

result=0
for numar in input1.split():
    if result == 0:
        result = int(numar)
    else:
        result = cmmdc(result,int(numar))
if result == 0:
    result = "nu s-au dat numere"
print("#1 cmmdc-ul este: "+str(result))

#2
def countVowels(string):
    vowels = 'aieouAEIOU'
    count = 0

    for letter in string:
        if letter in vowels:
            count+=1
    return count

cuvant = input("#2 introdu cuvant: ")
if len(cuvant)==0:
    print("nu ai scris cuvant...")
else:
    print("#2 nr vocale in cuvant: "+ str(countVowels(cuvant)))

#3
string1="asta"
text="cartea asta e mai buna decat asta"
counter=0
listaCuvinte=text.split()
for cuvant in listaCuvinte:
    if cuvant == string1:
        counter+=1
print("#3 nr aparitii cuvant in text:"+str(counter))

#4 Write a script that converts a string of characters written in UpperCamelCase into lowercase_with_underscores.
text="UpperCamelCase CeFainAmScris"
textFinal=""
newWord=True
for character in text:
    if character == " ":
        newWord=True
        textFinal+=" "
    elif newWord == True:
        newWord=False
        textFinal+=character.lower()
    else:
        if character.isupper():
            textFinal+="_"+character.lower()
        else:
            textFinal+=character
print("#4 "+textFinal)

#5 Write a function that validates if a number is a palindrome.
def isPalindrome(number):
    copyOfNumber = number
    reversedNumber = 0
    while number != 0:
        reversedNumber= reversedNumber*10 + number%10
        number//=10
    return copyOfNumber==reversedNumber

print("#5 12321 e palindrom? "+str(isPalindrome(12321)))

#6 Write a function that extract a number from a text 
# (for example if the text is "An apple is 123 USD", this function will 
# eturn 123, or if the text is "abc123abc" the function will extract 123).
#  The function will extract only the first number that is found.
def extractFirstNumber(text):
    number=0
    digitsFound=False
    for character in text:
        if(digitsFound == True):
            if(character.isdigit()):
                 number=number*10 + int(character)
                 continue
            else:
                return number
        if(character.isdigit()):
            digitsFound=True
            number=int(character)
    return digitsFound
print("#6 number found:"+str(extractFirstNumber("An apple is 123 USD")))

#7 Write a function that counts how many bits with value 1 a number has. 
# For example for number 24, the binary format is 00011000, meaning 2 bits with value "1"

def bitsWithValue1(number):
    counter=0
    while number!=0:
        if number & 1 == 1:
            counter+=1
        number>>=1
    return counter

print("#7 numarul 24 are "+str(bitsWithValue1(24))+" biti pe 1")

#8 Write a function that counts how many words exists in a text.
#  A text is considered to be form out of words that are 
# separated by only ONE space. For example: "I have Python exam" has 4 words.
def countWords(text):
    counter=0
    text=text.strip()
    for character in text:
        if character == " ":
            counter+=1
    if counter > 0:
        return counter+1
    return counter

print("#8 nr cuvinte in text: "+str(countWords(" I have Python exam " )))