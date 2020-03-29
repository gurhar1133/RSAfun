import random
from RSAlib import *

def main():
    # a list of some primes. Yes a small sample,
    #  but more for demonstration
    
    primes = [10000019,10000079,10000103,10000121,10000139,10000141,10000169,10000189]
    
    print('Welcome to main menu:\n')
    ans = ""
    subans = ""
    while ans != "quit":
        print("""
        Make your selection:
        1) Generate Keys
        2) Encode data
        3) Decode data
        4) Crack code
        5) enter 'quit' to exit

        """)
        ans = input("Your selection: ")
        if ans == "1":
            print("Would you like to use your own primes p and q?")
            print("Or would you like me to use some of mine?\n")
            subans = input("Enter 1 for your own or 2 for mine: ")
            
            if subans == "1":
                p = int(input("Enter value for p: "))
                q = int(input("Enter value for q: "))
                publicKey = Find_Public_Key_e(p, q)
                privateKey = Find_Private_Key_d(publicKey[1],p,q)
                print("your public key (n, e):", publicKey)
                print("your private key d: ", privateKey)
            
            elif subans == "2":
                
                index1 = random.randint(0,len(primes)-1)
                p = primes[index1]
                index2 = random.randint(0,len(primes)-1)
                
                while index2 == index1:
                    index2 = random.randint(0,len(primes)-1)
                q = primes[index2]
            
                publicKey = Find_Public_Key_e(p, q)
                privateKey = Find_Private_Key_d(publicKey[1],p,q)
                print("your public key (n, e):", publicKey)
                print("your private key d: ", privateKey)
            else:
                print("Invalid input entered. Back to main menu")
        elif ans == "2":
            message = input("please enter your message to be encryted: ")
            n = int(input("please enter public key n value: "))
            e = int(input("please enter public key e value: "))
            
            encoded = Encode(n, e, message)
            print("Your encoded message:")
            print(encoded)
        elif ans == "3":
            
            encrypted = input("please enter your encoded message: ")
            
            #cleans up the input to be turned into a nice list of numbers
            #for processing
            encrypted = encrypted.replace("[","")
            encrypted = encrypted.replace("]","")
            encrypted = encrypted.split(",")
            e_list = []
            for num in encrypted:
                e_list.append(int(num))
            
            
            n = int(input("please enter public key n value: "))
            d = int(input("please enter private key d value: "))
            decoded = Decode(n, d, e_list)
            print("Your decoded message:\n")
            print(decoded)
        elif ans == "4":
            n = int(input("please enter the public key n: "))   
            e = int(input("please enter the public key e: "))
            
            encrypted = input("please enter your encoded message you wish to break: ")
            
            #cleans up the input to be turned into a nice list of numbers
            #for processing
            encrypted = encrypted.replace("[","")
            encrypted = encrypted.replace("]","")
            encrypted = encrypted.split(",")
            e_list = []
            for num in encrypted:
                e_list.append(int(num))

            subans = input("""
                Which factorization method?
                a) Brute
                b) Pollards Rho
                c) Fermat Factorization
                ?""")
            if subans == "a":
                decoded = break_with_semi_brute(n,e,e_list)
                print("Your decoded message:\n")
                print(decoded)
            elif subans == "b":
                decoded = break_with_pollards(n, e, e_list)
                print("Your decoded message:\n")
                print(decoded)
            elif subans == "c":
                decoded = break_with_fermat(n, e, e_list)
                print("Your decoded message:\n")
                print(decoded)

        elif ans == "quit":
            print("bye bye")
        else:
            print("I think you might have entered an invalid answer")
        
    
if __name__ == '__main__':

    main()