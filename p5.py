for i in range(int(input())):
    n = int(input())
    a = 0
    b = n-1
    l = list(map(int,input().split()))
    t = max(l[a],l[b])
    
    while a != b: 
        if l[a] >= l[b]:
            if l[a]<= t:
                outcome = 'Yes'
                a += 1
            else:
                outcome = 'No'
                break
        else:
            if l[b]<= t:
                outcome = 'Yes'
                b -= 1
            else:
                outcome = 'No'
                break
            
    print(outcome)