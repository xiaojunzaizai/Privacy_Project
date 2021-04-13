import numpy as np


def noisyCount():
    beta = 1
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        n_value = -beta*np.log(1.-u2)
    else:
        n_value = beta*np.log(u2)
    return n_value

def add_noise(data):
    new_data = []
    for j in data:
        temp = []
        for i in range(len(j)):
            if  i == 4 or  i == 5  or i == 0 or i == 10:
                j[i] += noisyCount()
                temp.append(j[i])
            else:
                temp.append(j[i])
        new_data.append(temp)
    return new_data