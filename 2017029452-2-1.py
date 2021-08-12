import numpy as np
M = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])
print(M)
M = M.reshape(5,5)
print(M)
M[0,0] = 0
M[1,0] = 0
M[2,0] = 0
M[3,0] = 0
M[4,0] = 0
print(M)
M = M@M
print(M)
v = M[0,]

sum = 0
for a in v:
    sum += a*a
print(np.sqrt(sum))
