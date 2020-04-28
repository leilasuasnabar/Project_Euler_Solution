#______________________________________________________
# Author: Leila Suasnabar
# Date: 4/26/2020
# This version contains only the best method attempted
# For more information please check:
# 
#______________________________________________________

import numpy as np
import time

#Obtain prime numbers up to N
# Using Sieve the Eratosthenes: O(NloglogN)
def get_primes(N):
    IsPrime = [1 for i in range(N+1)]
    
    primes = []
    check = 2
    while check*check<=N:
        if IsPrime[check]:
            primes.append(check)
            # Increment by check
            for i in range(check*check,N+1,check):
                IsPrime[i]=0
        check+=1

    # Store all remaining primes in an array
    for num in range(check,N):
        if IsPrime[num]:
            primes.append(num)
    del IsPrime
    return primes

def sum_consecutive(prime_list,N):
    
    primes = prime_list.copy()
    # Longest sequence added that is < N
    # Sum of first X primes >> Sum of first X even numbers = N(N+1)
    
    max_slide = int(np.round(N**.5))
    # A sum of sequence that starts with 2, can only have a even length 
    # to produce an odd number (possibly prime)
    max_slide -= max_slide%2   
    
    max_sum = np.sum(primes[:max_slide])
    first_prime = primes[0]
         
    # Get the max sum (prime or not) that is <= the highest prime < N
    while max_sum >= primes[-1]:
        max_slide-=2
        max_sum-=(primes[max_slide]+primes[max_slide-1])
        

    # Sequence starting with first element: 2
    # Get the max sum that is a prime, with a sequence starting with 2
    while max_sum not in primes:
        max_slide -= 2
        max_sum = np.sum(primes[:max_slide])
        
    # Check other primes
    check = True

    # Save max slide when sequence starts with 2
    max_slide_even_prime = max_slide
    
    # Check for sequences starting with other primes
    max_slide+=1
    
    while check:
        primes.pop(0) #Remove first element

        # Check if must continue checking
        if np.sum(primes[:max_slide])>primes[-1]:
            check = False
        
        slide, sum_slide, first_element = find_slide(max_slide,primes,N)
        
        # Update longest slide and its sum
        if slide>max_slide:
            max_slide = slide
            if sum_slide:
                max_sum = sum_slide
                first_prime = first_element

    if first_prime==2:
        return max_slide_even_prime, max_sum, first_prime
    else:
        return max_slide, max_sum, first_prime


def find_slide(slide,primes,N):
    
    # Check only on any longer sequences
    # Increase slide by 2 since for a sum of even amount of prime numbers
    # will result in an even number (not prime)
    sum_prime = np.sum(primes[:slide+2])
    
    max_sum = None
    max_slide = slide
    first_element = None
    

    #Only check while sum < max # prime
    while sum_prime<=primes[-1]:         
        slide+=2
        # Update variables if necessary
        if sum_prime in primes:
            max_slide = slide
            max_sum = sum_prime
            first_element = primes[0]
        
        sum_prime = np.sum(primes[:slide+2])
      
    return max_slide, max_sum, first_element

if __name__ == "__main__":

    print('\nFinding the longest sequence of primes that add up to a prime, from 2 to N')
    N = input('Enter a value for N: ')

    # Validate input
    while True:
        if N.isdigit():
            N = int(N)
            break

        else:
            print('\nWrong input')
            N = input('Enter a value for N: ')

    # Check execution time to find the consecutive sum
    start_time = time.time()
    primes = get_primes(N)
    max_slide, prime_sum, first = sum_consecutive(primes,N)
    end_time = time.time() - start_time

    print('\nThe longest sequence contains {0} primes, and its sum/prime is {1}'.format(max_slide,prime_sum))
    print('Sequence starts with prime: ',first)

    index = primes.index(first)
    max_prime_sum = np.sum(primes[index:index+max_slide])

    print('\nDouble checking the sum is a prime: ')
    if max_prime_sum in primes and max_prime_sum==prime_sum:
        print('{} is a prime! \n'.format(prime_sum))
    else:
        print('{} is not a prime! \n'.format(prime_sum))

    print('Program execution time: {:.4f}s seconds\n'.format(end_time))
