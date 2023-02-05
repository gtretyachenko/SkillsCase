import numpy as np


def levenshtein_distance(s1, t1, ratio_calculation=False):
    # Initialize matrix of zeros
    rows = len(s1) + 1
    cols = len(t1) + 1
    calc_distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            calc_distance[i][0] = i
            calc_distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s1[row - 1] == t1[col - 1]:
                cost = 0
                if ratio_calculation == True:
                    cost = 2
                else:
                    cost = 1

                calc_distance[row][col] = min(calc_distance[row - 1][col] + 1,  # Cost of deletions
                                              calc_distance[row][col - 1] + 1,  # Cost of insertions
                                              calc_distance[row - 1][col - 1] + cost)  # Cost of substitutions
            if ratio_calculation == True:
                # Computation of the Levenshtein calc_distance Ratio
                Ratio = ((len(s1) + len(t1)) - calc_distance[row][col]) / (len(s1) + len(t1))
                return Ratio
            else:
                return "The strings are {} edits away".format(calc_distance[row][col])


Str1 = "Welcome to Javatpoint"
Str2 = "wlcome to Javatpoint"
Distance = levenshtein_distance(Str1, Str2)
print(Distance)
Ratio = levenshtein_distance(Str1, Str2, ratio_calculation=True)
print(Ratio)
