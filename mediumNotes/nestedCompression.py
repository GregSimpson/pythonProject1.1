
# [ expression for item in list if conditional ]

print ( [[j for j in range(3)] for i in range(4)] )


print ( [ [[j for j in range(3)] for i in range(2)] for g in range(3)] )


m = [[j for j in range(3)] for i in range(4)]
print ( m )

print ( [value
      for sublist in m
      for value in sublist] )


