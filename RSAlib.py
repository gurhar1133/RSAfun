# Library for RSA encryption, decryption and a Pollard's Rho
# factorization function for cracking codes
import random
import math

# BASIC RSA TOOLSET
def Convert_Text(_string):
    #Returns a list of ascii numbers associated with 
     #   each char 
    integer_list = []
    for char in _string:
        integer_list.append(ord(char))
    return integer_list

def Convert_Num(_list):
    #This one is for building a string form a list of ascii nums
    _string = ''
    for i in _list:
        _string += chr(i)
    return _string


def Convert_Binary_String(_int):
    #Binary conversion for Fast Modular Exponentiation 
    bits = []
    while _int > 0:
        k = _int % 2
        bits.insert(0,k)
        _int = _int//2
    
    return bits

def FME( a, n, b):
    #Fast modular exponentiation algorithm """
    result = 1
    bin_n = Convert_Binary_String(n)
    ## used a for loop with my Convert_Binary result rather than while loop
    # like but this is essentially the algorithm Sriram uses
    for bit in reversed(bin_n):
        if bit == 1:
            result = (result*a) % b
        a = (a**2) % b
        
    return result

def Euclidean_Alg(m, n):
   # This algorithm takes two integers and
        # returns their gcd as well as Bezout coeffients 
    m_c = m # copies for m and n
    n_c = n
    # s1, t1, s2, t2 are the initial values for bezout coefficients
    # this is an extended euclidean algorithm. It will return a tuple
    # with three values: (gcd, s, t)
    s1, t1, s2, t2 = 1, 0, 0, 1
    while n > 0:
        k = m % n
        q = m//n
        m = n
        n = k
        # copies of s1, t1
        s1c, t1c = s2, t2
        s2c, t2c = (s1 - q*s2), (t1 - q*t2)
        s1, t1 = s1c, t1c
        s2, t2 = s2c, t2c
    # will return m = gcd and s1, t1 are bezout coefficients
    return (m, s1, t1)

def Find_Public_Key_e(p, q):
    #Generates a public key given two primes
    phi = (p - 1)*(q - 1)
    proceed = True
    while proceed:
        # generates random values to test if they are rel prime
        # to phi. Since Euclidean_Alg returns a tuple, the 0th index
        # of a call on it will be the gcd
        e = random.randint(13,90)
        if e != p and e != q and Euclidean_Alg(e, phi)[0] == 1 :
            proceed = False
    
    return (p*q, e)

def Find_Private_Key_d(e, p, q):
    #Generates a private key, given two primes and e
    phi = (p - 1)*(q - 1)
    # the 1st index of the call on Euclidean_Alg is the
    # s Bezout Coefficient, which will give us the invers of
    # e mod (p-1)*(q-1)
    return Euclidean_Alg(e,phi)[1] % phi

def Encode(n, e, message):
   #THis uses the ascii conversion and FME(publicKey) to ecrypt
    #a message
    cipher_text = []
    message_list = Convert_Text(message)
    for num in message_list:
        # encrypts each ascii number 
        cipher_text.append(FME(num, e, n))
    
    return cipher_text

def Decode(n, d, cipher_text):
    #Decodes messages given a private key
    message = ''
    message_list = []
    for num in cipher_text:
        # decrypts each encrypted number
        message_list.append(FME(num, d, n))
    message = Convert_Num(message_list)
    return message


# FACTORING FUNCTIONS

def is_not_div(n):
    divs = [2, 3, 5, 7, 11, 13, 17, 19, 
    23, 29, 31, 37, 41, 43, 47, 53, 59, 
    61, 67, 71, 73, 79, 83, 89, 97]
    # checks divisibility against each number in divs
    for num in divs:
        if n % num == 0:
            return False
    return True

def brute_semi(n):
    #skips 2
    if n % 2 == 0:
        return 2
    # starting at 3 and up to root(n) skipping every other
    # number (ie. only checking odds)
    for num in list(range(3,int(n**(1/2)) + 1,2)):
        if n % num == 0:
            return num
    return False


def fermat_factor(n):
    # sources i used for this one
    # https://medium.com/coinmonks/integer-factorization-defining-the-limits-of-rsa-cracking-71fc0675bc0e
    # geeksforgeeks.org/fermats-factorization-method/
    # basic idea here is that a product of primes n = pq
    # can be expressed as n = (x-y)(x+y) = x^2 - y^2
    # so if we keep on testing x values so see if they fit
    # the formula we can return a factor of n
    x = 0
    while x < n:
        #looping through potential x values
        y_squared = n + x*x
        y = int(math.sqrt(y_squared))
        # checking that the formula satisfied
        if y*y == int(y_squared):
            return y - x
        x += 1
    print("factor not found")


def rand_f(x):
    # this is a helper function for pollard's rho
    # it returns value of a function that is useful 
    # for random number generation
    # in Pollard's Rho
    return (x**2 + random.randint(2, 2000))

def pollards_factor(n):
    #A pollards rho alorithm
    a = random.randint(2,10)
    b = random.randint(2,10)
    while a != b:
        a = rand_f(a) % n
        b = rand_f(rand_f(b)) % n
        # using random seeds in a and b
        # as well as the rand_f function
        # we then use the birthday paradox 
        # and take the gcd of the difference between 
        # a and b until we get a gcd > 1
        gcd = Euclidean_Alg(abs(b - a), n)[0]
        if gcd > 1:
            return gcd


# CODE BREAKING FUNCIONS:
    
def break_with_pollards(n, e, cipher_text):
    p = pollards_factor(n)
    if p != None:
        q = n/p
        q = int(q)
        print("p: ", p)
        print("q: ", q)
        # gets a d private key given the p and q
        # obtained through Pollard's Rho Factorization
        key_cracker = Find_Private_Key_d(e, p, q)
        # then uses decode to decode it
        decoded = Decode(n, key_cracker, cipher_text)
        return decoded
    else:
        print("factor not found")
        

    
def break_with_fermat(n, e, cipher_text):
    # essentially the same as break with pollards rho
    # uses fermat factorization  to get factor of n
    p = fermat_factor(n)
    if p != None:
        q = n/p
        q = int(q)
        print("p: ", p)
        print("q: ", q)
        key_cracker = Find_Private_Key_d(e, p, q)
        decoded = Decode(n, key_cracker, cipher_text)
        return decoded
    else:
        print('error')


def break_with_semi_brute(n, e, cipher_text):
    # essentially the same as break with pollards rho
    # uses brute semi to get factor of n
    p = brute_semi(n)
    if p != False:
        q = n/p
        q = int(q)
        print("p: ", p)
        print("q: ", q)
        # uses p and q to obtain the privte key
        key_cracker = Find_Private_Key_d(e, p, q)
        #then decodes
        decoded = Decode(n, key_cracker, cipher_text)
        return decoded
    else:
        print("factor not found") 