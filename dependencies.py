import math, random, time
from os import listdir

# list all files that exist within the storage directory
def retrieveExistingFNames():
    #print('Retrieving File Names')
    direc = './Images/'
    if len(listdir(direc)) == 0:
        time.sleep(5)
        return retrieveExistingFNames()
    names = [direc+str(fName) for fName in listdir(direc) if '.JPG' in fName]
    names.sort()
    return names

# Choose a random file from the storage directory
def chooseFile(fNames):
    #print('Choosing File')
    weights = gen_weights(len(fNames))      # Change these lines to remove biasing
    file = random.choices(fNames, weights)[0]
    print(file)
    #print(f'Index: {index}, Length of File Names: {len(fNames)}')
    #print(f'File Name: {fNames[index]}')
    return file

def gen_weights(length):    # Bias the image selection towards more recent images using the message IDs
    weights = []
    w = 0.9
    for i in range(length):
        if i % int(length/20) == 0:
            w += 0.5
        weights.append(w)
    return weights