import argparse
import os
import ast
def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    percentage = round(distances[-1] / max(len(s1), len(s2)), 3)
    return percentage



def normalize(code:str):
    tree = ast.parse(code, type_comments=True)
    ast.fix_missing_locations(tree)
    return tree
def openFile(fileName:str):
    path = os.getcwd()
    f = open(path + "/" + fileName, "r")
    return f.read()

def writeFile(fileName:str, data:str):
    path = os.getcwd()
    f = open(path + "/" + fileName, "a")
    f.write(data + "\n")
    f.close()

def main():
    parser = argparse.ArgumentParser(description="compare file similarity")
    parser.add_argument('input', type=str, help="Input file name")
    parser.add_argument('scores', type=str, help="Output file name")
    args = parser.parse_args()

    groups = openFile(args.input)
    temp = groups.split('\n')

    for group in temp:
        files = group.split(' ')

        firstFile = openFile(files[0])
        secondFile = openFile(files[1])

        normalizedFirstFile = normalize(firstFile)
        normalizedSecondFile = normalize(secondFile)

        s1, s2 = str(normalizedFirstFile), str(normalizedSecondFile)

        writeFile(args.scores, str(levenshtein_distance(s1, s2)))



if __name__ == '__main__':
    main()
