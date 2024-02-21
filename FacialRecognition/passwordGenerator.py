import random

lowercase,uppercase,digits='','',''
for i in range(26):
    if i<10:
        digits+=str(i)
    lowercase+=chr(i+97)
    uppercase+=chr(i+65)
    
specialChars='!@#$&?'

choice=lowercase+uppercase+digits+specialChars

def generatePassword(passwordLength):
    password=''

    for i in range(passwordLength):
        val=random.randint(0,len(choice)-1)
        password+=choice[val]
    return password