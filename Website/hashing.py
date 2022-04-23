def hashPasswordEncrypt(password):
    '''How does that hashing function work?
    It takes password + random string then goes through fixed hashing algo and churns out hashed pw
    To decrypt just run through the hashing func reverse and then detach the string to get the password'''

    import string    
    import random # define the random module  
    S = 10  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    
    salt_password = ran2+password+ran
    newPassword = hashAlgo(salt_password,len(salt_password)-1)
    return newPassword

#recursive Hashing Algorithm
def hashAlgo(string,count):
    if count == -1:
        return string
        
    character = string[count]
    hashedChar = chr((ord(character)%40)+40)
    newstring = string[:count]+hashedChar+string[count+1:]
    string = hashAlgo(newstring,count-1)

    return string

def checkPassword(password,enteredPassword):
    pw = hashPasswordEncrypt(enteredPassword)
    enteredToCheck = pw[10:-10]
    passwordToCheck = password[10:-10]

    return enteredToCheck==passwordToCheck




