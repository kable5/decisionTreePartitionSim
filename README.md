# Decision Tree Partition Sim

This program determines what node of a tree should be partitioned and how this partition should be further split. 
The algorithm implemented is similar to the ID3 approach to inferring partitions, in which we split the node with the maximum gain, in an effort to minimize the overall entropy of the set.

## Running the Program
To run the program, navigate to the program directory in the Linux terminal. Enter **python3 partitionSim.py** in the command line. 

The program will prompt you to enter the name of the data file, the name of the partition file, and the name of the output file.
The data file should begin with two numbers, the number of examples followed by the number of features. 
This is followed by the list of examples, with the last column being the target attribute and all others being the feature value.
Features can be a value of 0-2, while the target value is a binary 0 or 1.

Each of the lines in the partition file begin with the partition id, followed by the index of the examples in the partitioin.

An example of both the data and partition files are included in the project directory, with *data.txt* and *part.txt* respectfully.

## TODO

- [ ] More robust error checking