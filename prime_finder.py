import math
import pickle
import os.path

def pfind(n_max = 1E6):
    primefile = 'primes.pkl'
    prime_list = [2,3,5]
    if(os.path.isfile(primefile)):
        with open(primefile,'rb') as file:
            prime_list = pickle.load(file)

    n = max(prime_list)
    prime_count = len(prime_list)
    while n < n_max:
        if ((n % 10) == 3):
            n = n+4
        else:
            n = n+2
        if(isprime(n,prime_list)):
            prime_count = prime_count + 1
            prime_list.append(n)
            print(f'New Prime! {prime_count}: {n}')

    with open('primes.pkl','wb') as file:
        pickle.dump(prime_list,file)

def isprime(n,prime_list = [2,3]):
    if (len(prime_list) == 2):
        primefile = 'primes.pkl'
        prime_list = [2, 3, 5]
        if (os.path.isfile(primefile)):
            with open(primefile, 'rb') as file:
                prime_list = pickle.load(file)

    p_max = max(prime_list)
    if(n> p_max**2):
        print('candidate too large')
        return -1

    composite = False
    i = 0
    while i < len(prime_list) and \
            (not composite) and \
            (prime_list[i] <= math.sqrt(n)):
        known_prime = prime_list[i]
        # print(f'Testing divisibility by {known_prime}')
        if (n % known_prime == 0):
            composite = True
            return False
        i = i + 1

    if (not composite):
        return True
    else:
        return False

