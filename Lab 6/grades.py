"""
Name(s): Zekarias Asaminew 
CSC 201
Lab6

grades reads data for a multiple choice exam from a file, scores
each exam, computes statistics for the exam, and scales the
exam if desired by the user. The stats are displayed in the console
window, while each student's score is written to a file.

Did you complete this lab file during the class period (yes or no)?
No

If no, leave the one that applies. If yes, delete this entire section!
I completed grades.py independently.

Document any assistance you get if you complete the lab after the class period:
I gave and received no assistance. 


"""

import os
import math 

def getFileToRead():
    """
    Prompts the user to enter the file name until valid and opens the file for reading
    Returns:
        the file variable connected to the data file
        the name of the file without the extension
    """
    infileName = input('Enter a class file to grade (i.e. class1 for class1.txt): ')
    infileNameWithExtension = infileName + '.txt'
    while not os.path.exists(infileNameWithExtension):
        print('File not found. Re-enter file name.')
        infileName = input('Enter a class file to grade (i.e. class1 for class1.txt): ')
        infileNameWithExtension = infileName + '.txt'
    infile = open(infileNameWithExtension, 'r')
    return infile, infileName


def gradeExam(infile):
    """
    Reads through the file to grade each student's exam. The first line of the file
    is the answer key. They remaining lines are each student's answers. The method creates
    two parallel lists: a list of student id numbers and a list of the student's exam scores.
    It also counts the number of lines of the file that are corrupt.
    
    Params:
    infile: the file object connected to the data file
    
    Returns:
    the list of student id numbers
    a parallel list of exam scores for each student
    the number of corrupt lines in the file
    """
    countCorruptLines = 0
    idList = []
    scoreList = []
    
    firstLine = infile.readline()
    firstLine = firstLine.strip()
    keyList = firstLine.split(',')
    
    # your loop goes here to read through the rest of the file
    
    for line in infile:
        line = line.strip()
        answerList = line.split(',')
        score = 0
        if len(keyList) == len(answerList):
            idList.append(answerList[0])
            
            for i in range(len(keyList) - 1):
                if keyList[i + 1] == answerList[i + 1]:
                    score += 4
                elif answerList[i + 1] == '':
                    score += 0
                elif keyList[i + 1] != answerList[i + 1]:
                    score = score -1
                
            scoreList.append(score)
        else:
            countCorruptLines += 1
    return (idList, scoreList, countCorruptLines)
            
            
                    
        


def calculateMedian(scoreList):
    """
    Calculates the median score for the exam
    
    Params:
    scoreList: the list of exam scores (which needs to stay inorder)
    
    Returns:
    the median of the scores
    """
    scoreListCopy = scoreList.copy()
    scoreListCopy.sort()
    
    if len(scoreListCopy) % 2 != 0:
        middleIndex = math.floor(len(scoreListCopy) / 2)
        medianScore = scoreListCopy[middleIndex]
    elif len(scoreListCopy) % 2 == 0:
        upperIndex = int(len(scoreListCopy) / 2)
        lowerIndex = int(len(scoreListCopy) / 2) - 1
        medianScore = (scoreListCopy[upperIndex] + scoreListCopy[lowerIndex])/2
    return medianScore 

def calculateStats(scoreList):
    """
    Calculates the highest score, lowest score, mean score, and median score for the exam
    
    Params:
    scoreList: the list of exam scores (which needs to stay inorder)
    
    Returns:
    the highest score, lowest score, mean score, and median score
    """
    scoreListCopy = scoreList.copy()
    scoreListCopy.sort()
    maxScore = scoreListCopy[-1]
    minScore = scoreListCopy[0]
    #Calculate mean score
    totalScore = 0 
    for score in scoreListCopy:
        totalScore += score
    meanScore = totalScore/len(scoreListCopy)
    medianScore = calculateMedian(scoreList)
    
    return (maxScore, minScore, meanScore, medianScore)
    
def outputSummary(numScores, countCorrupt, max, min, mean, median):
    """
    Outputs a summary of the exam's stats
    
    Params:
    numScores: the number of scored exams
    countCorrupt: the number of lines of the file that could not be scored
    max: the highest score
    min: the lowest score
    mean: the arithmetic mean (average) of the exam scores
    median: the median of the exam scores
    
    """
    print('\nGrade Summary')
    print(f'Total students: {numScores + countCorrupt}')
    print(f'Corrupt lines in the file: {countCorrupt}')
    print(f'Highest score: {max}')
    print(f'Lowest score: {min}')
    print(f'Mean score: {mean:.2f}')
    print(f'Median score: {median:.2f}')
    print()
    
    
def scaleExam(scoreList, mean):
    """
    Prompts the user to determine if the exam will be scaled, and if so, prompt the user
    for the desired mean for the exam. The method modifies the scores by the amount required
    make the mean the desired value.
    
    Params:
    scoreList: the list of exam scores (which needs to stay inorder)
    mean: the arithmetic mean (average) of the current scores
    """
    choice = input("Would you like to scale the exam? 'y' or 'n': ")
    choice = choice.lower()
    choice_list = ['y','n']
    while choice not in choice_list:
        print("Invalid input. Enter 'y' or 'n'.")
        choice = input("Would you like to scale the exam? 'y' or 'n': ")
        choice = option.lower()
    
    if choice == 'y':
        newMean = float(input('Enter desired mean: '))
        while newMean <= mean:
            print("Invalid input. That wouldn't raise the scores.")
            newMean = float(input('Enter desired mean: '))

        scalePoint = newMean - mean
        for i in range(len(scoreList)):
            scoreList[i] = scoreList[i] + scalePoint
        return scoreList

    
def createResultsFile(idList, scoreList, infileName):
    """
    Writes the exam data to a file. Each file of the file is the student's id
    followed by their score.
    
    Params:
    idList: the list of student ids
    scoreList: a parallel list of exam scores for each student
    infileName: the name of the data file without the extension
    """
    outFileName = infileName + '_grades.txt' 
    outFile = open(outFileName, 'w')
    for index in range(len(idList)):
        outFile.write(f'{idList[index]},{scoreList[index]:.2f}\n')
    outFile.close()
    print(f'Check file {outFileName} for student scores!')


def main():
    infile, infileName = getFileToRead()
    idList, scoreList, numCorrupt = gradeExam(infile)
    #print(idList, scoreList, numCorrupt)
    maxScore, minScore, meanScore, medianScore = calculateStats(scoreList)
    outputSummary(len(scoreList), numCorrupt, maxScore, minScore, meanScore, medianScore)
    scaleExam(scoreList, meanScore)
    createResultsFile(idList, scoreList, infileName)

main()