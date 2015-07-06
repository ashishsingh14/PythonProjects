from cmath import sqrt

def doublestring():
    t = int(raw_input())
    for i in xrange(t):
        n = int(raw_input())
        if (n%2==0):
            print (n)
        else:
            print (n)-1
    


def palindromenumber(a):
    if (a>=0 and a <=9):
        return 1
    else:
        x = str(a)
        l = len(x)
        i = 0
        j = l-1
        while i<j:
            if(x[i]!=x[j]):
                return 0
                break
            else:
                i = i+1
                j = j-1
        return 1


def checkprime(a):
    for i in xrange(sqrt(a)):
        if(i==0 or i==1):
            continue
        elif (a%i==0):
            return 0
            break
        else:
            return 1
        
        
    
def primepalindrome():
    t = int(raw_input())
    for i in xrange(t):
        a = int(raw_input())
        print checkprime(a)
        
        
                    
if __name__ == "__main__":
    primepalindrome()
    
    