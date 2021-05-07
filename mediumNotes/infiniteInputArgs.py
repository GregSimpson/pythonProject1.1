
def fun1(*a):
    res=1
    for ele in a:
        res*=ele
    return res
ans=fun1(5,6,9,6,9,6,6)
print(ans)

ans=fun1(1,2,3)
print(ans)

