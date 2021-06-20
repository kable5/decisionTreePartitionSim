#########################################################################################
# File: partitionSim.py
# Author: Kris Ables
# Procedures:
# prob:                 - calculates the probability of both 1 & 0 output for a dataset
# entropy:              - calculates entropy of a dataset
# conditionalSplit      - splits a dataset based on its features
# conditionalEntropy    - calculates the entropy of a dataset given a particular feature
# splitPartition        - executes the man partition algorithm
#########################################################################################

import math

m = 0
n = 0

##################################################
# prob(dataSet)
# Author: Kris Ables
# Date: 17 June 2021

# Description - calculates the probability of the given dataset

# Parameters:
# dataSet I/P   - data set to be analysed
#
# probOne O/P   - the probability of 1
# probZero O/P  - the probability of 0
##################################################
def prob(dataSet):
    count = 0
    for ex in dataSet:                  # counts the number of 1 target attributes in the dataset
        if ex[n] == 1:
            count = count + 1

    probOne = count / len(dataSet)      # calculate the probability of 1 in the dataset
    probZero = 1 - probOne              # calculates prob of 0 using complement of 1 prob
    return probOne, probZero

##################################################
# entropy(dataSet)
# Author: Kris Ables
# Date: 17 June 2021

# Description   - calculates the entropy of the given dataset

# Parameters:
# dataSet I/P   - data set to be analysed
#
# ent O/P       - the entropy of the dataset
##################################################
def entropy(dataSet):
    probOne, probZero = prob(dataSet)               # find two necessary probabilities
    if probOne == 0 or probZero == 0:               # return 0 if one of the probs are 0 (completely certain)
        return 0

    entOne = probOne * (math.log(probOne, 2))       # calculates ent of 1
    entZero = probZero * (math.log(probZero, 2))    # calculates ent of 0
    ent = -1 * (entOne + entZero)                   # sums and negates the entropy
    return ent

##################################################
# conditionalSplit(dataSet, feat)
# Author: Kris Ables
# Date: 18 June 2021

# Description   - splits the data in the dataset in accordance to
#               the feature value of a designated feature

# Parameters:
# dataSet I/P           - data set to be split
# feat I/P              - feature that determines data
#                       set split
#
# featurePartitions O/P - a list of lists with examples
#                       separated based on features
##################################################
def conditionalSplit(dataSet, feat):
    featurePartitions = [[], [], []]            # inits return list with three lists for the three possible
                                                # feature options
    for ex in dataSet:                          # adds every example in the dataset
        featurePartitions[ex[feat]].append(ex)  # to their proper feature part in return list

    return featurePartitions

##################################################
# conditionalEntropy(dataSet, feat)
# Author: Kris Ables
# Date: 18 June 2021

# Description   - calculates the entropy of a dataset
#               given a specific feature

# Parameters:
# dataSet I/P   - data set to be split
# feat I/P      - feature that determines data set split
#
# ent O/P       - calculated entropy of the dataset
##################################################
def conditionalEntropy(dataSet, feat):
    splitData = conditionalSplit(dataSet, feat)             # splits the dataset into feature partitions
    ent = 0
    for featureSet in splitData:                            # for every set of examples divided by feature
        if len(featureSet) != 0:                            # if there exists example with given feature
            test = entropy(featureSet)                      # calculates its entropy
            ent += test * (len(featureSet) / len(dataSet))  # adds to total entropy by multiplying the ent to the
                                                            # probability of the feature
    return ent

##################################################
# splitPartition(dataSet, nameSet)
# Author: Kris Ables
# Date: 20 June 2021

# Description   - performs the main decision-tree node
#               splitting algorithm

# Parameters:
# dataSet I/P       - data set to be split
# nameSet I/P       - list of partition names
#
# retNames O/P      - returns the list of the names of the new partitions
# partIndexes O/P   - list of examples in each partition
##################################################
def splitPartition(dataSet, nameSet):
    maxF = -1
    bestFeat = -1
    replacedPart = -1

    for i in range(len(dataSet)):                                               # loops through dataset
        maxGain = -1                                                            # sets max gain and feat to lowest
        feat = -1                                                               # possible value
        for j in range(1, n):                                                   # for every feature
            tempGain = entropy(dataSet[i]) - conditionalEntropy(dataSet[i], j)  # calculates gain by subtracting entropy
                                                                                # given the feature n from the entropy
                                                                                # of the entire dataset
            if tempGain > maxGain:                                              # replaces max gain if calculated is
                maxGain = tempGain                                              # greater than previous biggest
                feat = j                                                        # and sets the feature as bes

        f = (len(dataSet) / m) * maxGain                                        # calculates f
        if f > maxF:                                                            # replaces max f if the calculated is
            maxF = f                                                            # greater than previous
            bestFeat = feat                                                     # marks the feature as best
            replacedPart = i                                                    # as well as the partition to be split

    splitData = conditionalSplit(dataSet[replacedPart], bestFeat)   # splits the partition to be replaced in accordance
                                                                    # to the feature with the best gain
    retParts = dataSet                                              # initialize partitions to be returned as dataset
    retNames = nameSet                                              # initialized list of partition names as the given
                                                                    # name set
    # TODO: print name of partition replaced along with the feature used & the partitions that replaced it
    del retParts[replacedPart]                                      # remove the part to be split from ret
    splitName = nameSet[replacedPart]                               # save name of the split partition
    del nameSet[replacedPart]                                       # remove name of split partition
    i = 1
    for split in splitData:                                         # for every new partition
        if len(split) != 0:                                         # if partition has examples
            name = (splitName + str(i))                             # set its name to old partition name + i
            i += 1                                                  # increment i
            retNames.insert(replacedPart, name)                     # insert the name into its proper place in the list
            retParts.insert(replacedPart, split)                    # insert partition in the proper place in the list

    partIndexes = []                # initialize list of indexes
    for setParts in retParts:       # for every partition in set parts
        temp = []
        for sets in setParts:       # for every example in partition
            temp.append(sets[0])    # add to the front of temp list
        partIndexes.append(temp)    # add temp list of examples per partition to the indexes list

    return retNames, partIndexes


if __name__ == '__main__':

    print("Enter names of the files dataset input-partition output-partition")
    files = input()
    files = files.split(' ')

    # TODO : more robust error checking

    # Reads in database file
    dataFile = open(files[0], "r")                      # selects the data file from the input list
    lines = dataFile.readlines()                        # creates list of lines to easily process
    length = lines[0].split(' ')                        # splits the first lines to extract m & n
    m = int(length[0])
    n = int(length[1])
    data = []                                           # initializes data matrix
    for i in range(m):                                  # for every example in data file
        example = lines[i + 1]                          # obtains example in lines
        example = example.strip("\n")                   # removes the \n at the end of the line
        example = [int(x) for x in example.split()]     # splits the example into a list of ints
        example.insert(0, i + 1)                        # appends example index to the end of example
        data.append(example)                            # adds this list of ints to the data matrix

    # Reads in partition file
    partitionFile = open(files[1], "r")             # selects the partition file from the input
    lines = partitionFile.readlines()               # creates a list of file lines to easily process
    partitionNames = []
    partitions = []
    for i in range(len(lines)):                     # loops through all the lines in the partition file
        part = lines[i]                             # selects given line
        partitionExamples = []                      # instantiates list that stores the features and output
        part = part.strip("\n")                     # removes \n from the end of line
        part = part.split()                         # splits line into list
        partitionNames.append(part[0])              # adds the name of the partition to partitionNames list
        del part[0]                                 # removes this item from list
        part = [int(x) for x in part]               # converts list into list of ints (previously list of str)
        for j in part:                              # for every example in partition
            partitionExamples.append(data[j - 1])   # add to the partition example list
        partitions.append(partitionExamples)        # adds partition example set to list of all partition example sets

    name, part = splitPartition(partitions, partitionNames)     # executes the main algorithm that splits into its
                                                                # proper partitions

    # Writes output file
    outFile = open(files[2], "w")           # selects the partition file from the input
    for i in range(len(part)):              # loops through all partitions in the list
        line = name[i]                      # begins written line with the partition name
        for ex in part[i]:                  # for every partition in the list
            line = (line + ' ' + str(ex))   # adds space and example index to line
        line = line + "\n"                  # newline
        outFile.write(line)                 # writes to the file
