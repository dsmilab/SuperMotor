import sys
from lib import *

def Run(trainPrefix, testPrefix):
    
    trainFileList = []
    testFileList = []
    for i in range(MODE):
        trainFileList.append(trainPrefix + '_' + LABELS[i])
        testFileList.append(testPrefix + '_' + LABELS[i])
    
    # preprocess
    trainDataList = []
    testDataList = []
    allTrainData = []
    allTestData = []
    
    
    # read file   
    for i in range(MODE):
        trainData = Parse(Read(trainFileList[i]))
        testData = Parse(Read(testFileList[i]))
        ##
        allTrainData.append(trainData)
        allTestData.append(testData)
        ##
        trainDataList.append(Paging(trainData))
        testDataList.append(Paging(testData))
        
    X, y = Train(allTrainData, trainPrefix)
    

   ## peakMeans, peakStds, peakKX, valleyMeans, valleyStds, valleyKX = 
  ##  WriteToFile(peakMeans, peakStds, peakKX, valleyMeans, valleyStds, valleyKX)
  
    """
    predict
    """
    """
    for i in range(MODE):
        # now at mode i
        print('now at mode %d' % i)
        result = []
        for j in range(len(testDataList[i])):
            result.append(Predict(testDataList[i][j], peakMeans, peakStds, peakKX, valleyMeans, valleyStds, valleyKX))
        print(result)
    """
def main(argv):
    if len(argv) == 0:
        print('Error: Please give a filename as a parameter')
        sys.exit(2)
    elif len(argv) > 2:
        print('Error: Only accept at most 2 parameters.')
        sys.exit(2)
              
    trainFileName = argv[0]
    testFileName = argv[0]
    if len(argv) == 2:
        testFileName = argv[1]
    
    print('>> The machine is training ...')        
    Run(trainFileName, testFileName)
    print('>> Completed the training!')   
    
if __name__ == '__main__':
    testdata = ['0328_2_9600_d100',
                '0328_3_9600_d100',
                '0328_4_9600_d100',
                '0328_5_9600_d100',
                '0329_1',
                '0329_2',
                '0330_2',
                '0331_1']
    for data in testdata:
        main([data])
   ## main(sys.argv[1:])