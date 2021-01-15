#####################################################################
# ***IMPORTANT***: PYTHON 3.8 IS NECESSARY FOR NormalDist!
#
# Run without arguments (eg., python assign01.py); the script
#   will prompt with stdin dialogs. Can generate an arbitrary 
#   number of distributions and prints overall mean and variance
#   of the cumulative samples generated.
#
# I pledge my honor that I have abided by the Stevens Honor System.
#   Justin Ho
#####################################################################

from statistics import NormalDist  # ***IMPORTANT***: Python 3.8
from math import sqrt
import sys

# Generates and returns N samples from distribution N(mean, var)
def gen_dist (mean, var, N):
  return NormalDist(mean, sqrt(var)).samples(N)

# Generates arbitrary number of N(mean, var) distributions from user input
def main ():
  data = []         # List containing all samples
  cont_loop = True  # Loop boolean
  
  while cont_loop:
    # Accepts user input for distribution parameters
    mean = float(input("Enter mean of the distribution: "))
    var  = float(input("Enter variance of the distribution: "))
    N    = int(input("Enter number of samples: "))

    # Append newly generated samples to data list
    data.extend(gen_dist(mean, var, N))

    # Loop continues if user inputs string starting with 'y'; otherwise breaks
    cont_loop = True if input("Generate another distribution? (y/n): ").startswith('y') else False
    print()

  # Creates a normal distribution from the aggregate samples and prints mean and variance
  exp_data = NormalDist.from_samples(data)
  print("Mean of the combined datasets:", exp_data.mean)
  print("Variance of the combined datasets:", exp_data.variance)

if __name__ == "__main__":
  main()