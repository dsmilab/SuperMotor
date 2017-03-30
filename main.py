import matplotlib.pyplot as plt
import numpy as np

from sklearn import decomposition
from sklearn import datasets
from sklearn.svm import SVC

from parser0 import *

K = 3
PERCENT = 10
PASSRATIO = 0.7
SUCCESSRATIO = 0.9
MODE = 4

#####################################################################################
def Draw(fig, ax, X, label0):
    x = np.arange(0, len(X))
    y = X
    ax.plot(x, y, label=label0)


def Fill(fig, ax, minX, maxX, label0):
    x = np.arange(0, max(len(minX), len(maxX)))
    y1 = minX
    y2 = maxX
    ax.fill_between(x, y1, y2, label=label0, facecolor='gray')
#####################################################################################
    
def DrawIndepenet(files):
    fig, ax = plt.subplots(len(files), sharex = True, sharey = True)
    plt.xlim(0, 3000)
    #plt.ylim(-100, 100)
    plt.xlabel('timestamp');
    plt.ylabel('pca_value');
    for i in range(len(files)):
        file = files[i]
        records = LoadCSV(file)
        records = GetPCA(records, 1)
        Draw(fig, ax[i], records, file)
        ax[i].legend()    
    
    ax[0].set_title('PCA of dataset')

def DrawHitLineChart(X, yActive, yPassive, activeLabel):
    fig, ax = plt.subplots()
    plt.xlabel('kMultiplier')
    plt.ylabel('meanHitRatio')
    ax.plot(X, yActive, label = activeLabel)
    ax.plot(X, yPassive, label = 'others')
##    Draw(fig, ax, yActive, activeLabel)
##s    Draw(fig, ax, yPassive, 'others')
    ax.legend()
    ax.set_title('Hit Ratios of %s and others (in model %s)' % (activeLabel, activeLabel))



def DrawHitLineChart2(X, ys, labels, activeLabel):
    fig, ax = plt.subplots()
    plt.xlabel('kMultiplier')
    plt.ylabel('meanHitRatio')
    for j in range(MODE):
        ax.plot(X, ys[j], label = labels[j])
    ax.legend()
    ax.set_title('Hit Ratios (in model %s)' % (activeLabel))
    
    

def DrawMixed(data, labels):
    fig, ax = plt.subplots()
    #plt.ylim(-100, 100)
    plt.xlabel('timestamp');
    plt.ylabel('pca_value');
    for i in range(len(data)):
        Draw(fig, ax, data[i], labels)
        
    ax.legend()      
    ax.set_title('PCA of dataset')


def DrawXYZ(files):
    fig, ax = plt.subplots(3, sharex = True)
    plt.xlim(0, 3000)
   # plt.ylim(-100, 100)
    plt.xlabel('timestamp');
    plt.ylabel('acce');
    ax[0].set_title('original dataset')
    for i in range(len(files)):
        file = files[i]
        records = LoadCSV(file)
        
        xs, ys, zs = [], [], []
        for (x,y,z) in records:
            xs.append(x)
            ys.append(y)
            zs.append(z)
        Draw(fig, ax[0], xs, file + '_X')
        Draw(fig, ax[1], ys, file + '_Y')
        Draw(fig, ax[2], zs, file + '_Z')

    ax[0].legend()     
    ax[1].legend()  
    ax[2].legend()  


def CreateCurve(data):
    meanCurve = []
    stdCurve = []
    
    length = range(len(data[0]))

    for j in length:
        group = []
        for i in range(len(data)):
            group.append(data[i][j])
        group = np.array(group)
        meanCurve.append(np.mean(group))
        stdCurve.append(np.std(group))
        
    meanCurve = np.array(meanCurve)
    stdCurve = np.array(stdCurve)
    
    return meanCurve, stdCurve


def DrawEnvelope(meanCurves, stdCurves, labels, independent = True):
    XLABEL = 'timestamp'
    YLABEL = 'pca_value'
    TITLE = 'Envelope (mean +- ' + str(K) + ' std)'
    
    if(independent):
        fig, ax = plt.subplots(len(meanCurves), sharex = True, sharey = True)
    
        plt.xlabel(XLABEL)
        plt.ylabel(YLABEL)
        ax[0].set_title(TITLE)
        
        for i in range(len(meanCurves)):
            y1 = meanCurves[i] - K * stdCurves[i]
            y2 = meanCurves[i] + K * stdCurves[i]
            Draw(fig, ax[i], meanCurves[i], labels[i] + '_mean')    
            Fill(fig, ax[i], y1, y2, labels[i] + '_envelope')
            ax[i].legend()
    else:
        fig, ax = plt.subplots()
    
        plt.xlabel(XLABEL)
        plt.ylabel(YLABEL)
        ax.set_title(TITLE)
        
        for i in range(len(meanCurves)):
            y1 = meanCurves[i] - K * stdCurves[i]
            y2 = meanCurves[i] + K * stdCurves[i]
            Draw(fig, ax, meanCurves[i], labels[i] + '_mean')    
            Fill(fig, ax, y1, y2, labels[i] + '_envelope')
        ax.legend()


def DrawEnvelope2(trainingDataList, labels):
    XLABEL = 'timestamp'
    YLABEL = 'pca_value'
    TITLE = 'Envelope (mean +- ' + str(K) + ' std)'
    
    meanCurves = []
    stdCurves = []
    for i in range(MODE):
        trainData = np.array(trainingDataList[i])
        mean = np.mean(trainData)
        std = np.std(trainData)
        meanCurves.append([mean for _ in range(PAGESIZE)])
        stdCurves.append([std for _ in range(PAGESIZE)])
        
    fig, ax = plt.subplots()

    plt.xlabel(XLABEL);
    plt.ylabel(YLABEL);
    ax.set_title(TITLE)
    
    for i in range(len(meanCurves)):
        meanCurves[i] = np.array(meanCurves[i])
        stdCurves[i] = np.array(stdCurves[i])
        
        y1 = meanCurves[i] - K * stdCurves[i]
        y2 = meanCurves[i] + K * stdCurves[i]
        Draw(fig, ax, meanCurves[i], labels[i] + '_mean')    
        Fill(fig, ax, y1, y2, labels[i] + '_envelope')
        
    ax.legend()


def BuildSparseVector(meanCurve, stdCurve, spotCurve):
    vec = []
    for i in range(len(meanCurve)):
        if spotCurve[i] > meanCurve[i] + K * stdCurve[i]:
            vec.append(1)
        elif spotCurve[i] < meanCurve[i] - K * stdCurve[i]:
            vec.append(-1)
        else:
            vec.append(0)
    return vec


def FindPeaksSorted(X, RATIO = 10):
    peaks = []
    pagesize = len(X)
    for j in range(1, pagesize - 1):
        now = abs(X[j])
        prevv = abs(X[j - 1])
        nextt = abs(X[j + 1])
        # peak detect
        if now > prevv and now > nextt:
            # stored absolute value
            peaks.extend(now)
    
    peaks.sort()
    peaks.reverse()
    peaks = peaks[:int(pagesize * RATIO / 100)]
    
    return peaks


def CalculateHitRatio(meanCurve, stdCurve, spotCurve):
    hitCount = 0
    for i in range(len(meanCurve)):
        if abs(spotCurve[i] - meanCurve[i]) <= K * stdCurve[i]:
            hitCount += 1
    return float(hitCount) / len(meanCurve)


def CalculateHitRatio2(mean, std, spotCurve, k = K):
    hitCount = 0
    for i in range(len(spotCurve)):
        if abs(spotCurve[i] - mean) <= k * std:
            hitCount += 1
    return float(hitCount) / len(spotCurve)

PEAKMEANS = []
PEAKSTDS = []
KX = []

def Predict(data, peakMeans = PEAKMEANS, peakStds = PEAKSTDS, kX = KX, successRatio = SUCCESSRATIO):
    # preprocess peak
    peaks = FindPeaksSorted(data, 10)
   ## print('peak = ' + str(peaks))
    tmps = []
    for i in range(MODE):
        hitRatio = CalculateHitRatio2(peakMeans[i], peakStds[i], peaks, kX[i])
        tmps.append([hitRatio, i])
    
    return max(tmps)[1]

def _Predict(buffer):
    data = Parse(buffer, 1)
    return Predict(data)

def MakeFeatureMatrix(dataList, peakMeans, peakStds, percent = PERCENT, passRatio = PASSRATIO, kMultiplier = K):
    # calculate hit ratio for every mode which fit itself
    matrix = []
    for i in range(MODE):
        tmp = []
        for j in range(MODE):
            hitRatios = []
            for k in range(len(dataList[j])):
                peaks = FindPeaksSorted(dataList[j][k], percent)
                hitRatio = CalculateHitRatio2(peakMeans[i], peakStds[i], peaks, kMultiplier)
                hitRatios.append(hitRatio)
                
           ## print('Put mode %d into model %d to get hitRatio' % (j, i))
            ##print(hitRatios)
            
            #score
            score = 0
            for a in range(len(hitRatios)):
                if hitRatios[a] > passRatio:
                    score += 1.0
            score /= len(hitRatios)            
            tmp.append(score)
        matrix.append(tmp)
    return matrix

def Train(trainData):
    """
    we consider larger peaks which occupy top (RATIO)%
    """

    # preprocess
    trainDataList = []
    for i in range(MODE):
        trainDataList.append(Paging(trainData[i]))
    
    # preprocess peak
    peakMeans = []
    peakStds = []
    for i in range(MODE):
        # find peak
        peaks = FindPeaksSorted(trainData[i])
        peakMeans.append(np.mean(peaks))
        peakStds.append(np.std(peaks))

    peaksList = []    
    for i in range(MODE):
        peakList = []
        for k in range(len(trainDataList[i])):
            peaks = FindPeaksSorted(trainDataList[i][k])
            peakList.append(peaks)
        peaksList.append(peakList)
    
    # find the best K for every mode, and put into kX
    kX = []
    for i in range(MODE):
        tmps = []

        for k0 in range(5, 100+1, 1):  
            kMulti = k0 * 0.1
            h = [] # list of tuple(h0, h1, h2, h3)
            for j in range(MODE):
                hitRatios = []
                for k in range(len(peaksList[j])):
                    hitRatio = CalculateHitRatio2(peakMeans[i], peakStds[i], peaksList[j][k], kMulti)
                    hitRatios.append(hitRatio)
                hitRatios = np.array(hitRatios)
                h.append(np.mean(hitRatios))

            gaps = []
            for j in range(MODE):
                if i != j:
                    gaps.append(h[i] - h[j])

            if len(gaps) > 0:
                tmps.append([min(gaps), kMulti])
        
        nowMax = 0
        nowK = 0
        for k1 in range(len(tmps)):
            if tmps[k1][0] > nowMax:
                nowMax, nowK = tmps[k1][0], tmps[k1][1]
                
        kX.append(nowK)
                
    return (peakMeans, peakStds, kX)
  
    
def Run(trainPrefix, testPrefix):
    labels = ['fan0',
              'fan1',
              'fan2',
              'fan3']
    
    trainFileList = []
    testFileList = []
    for i in range(MODE):
        trainFileList.append(trainPrefix + '_' + labels[i])
        testFileList.append(testPrefix + '_' + labels[i])
    
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
    
    peakMeans, peakStds, kX = Train(allTrainData)
    
    fpp = open('motorcycle.txt', 'w')
    for i in range(MODE):
        fpp.write(str(peakMeans[i]))
        if i < MODE - 1:
            fpp.write(',')
        else:
            fpp.write('\n')
            
    for i in range(MODE):
        fpp.write(str(peakStds[i]))
        if i < MODE - 1:
            fpp.write(',')
        else:
            fpp.write('\n')
            
    for i in range(MODE):
        fpp.write(str(kX[i]))
        if i < MODE - 1:
            fpp.write(',')
        else:
            fpp.write('\n')
    fpp.close()    
    
    PEAKMEANS = peakMeans
    PEAKSTDS = peakStds
    KX = kX
    
##    print(trainPrefix)
##    print(peakMeans)
##    print(peakStds)
##    print(kX)
    
    """
    # preprocess peak
    peakMeans = []
    peakStds = []
    for i in range(MODE):
        # find peak
        peaks = FindPeaksSorted(allTrainData[i])
        peakMeans.append(np.mean(peaks))
        peakStds.append(np.std(peaks))

    peaksList = []    
    for i in range(MODE):
        peakList = []
        for k in range(len(trainDataList[i])):
            peaks = FindPeaksSorted(trainDataList[i][k])
            peakList.append(peaks)
        peaksList.append(peakList)
        
    
    for i in range(MODE):            
        X = []
        ys = []

        for k0 in range(5, 100+1, 1):
            kMulti = k0 / 10.0
            X.append(kMulti)
        for j in range(MODE):
            y = []
            for k0 in range(5, 100+1, 1):
                kMulti = k0 / 10.0
            
                hitRatios = []
                for k in range(len(peaksList[j])):
                    hitRatio = CalculateHitRatio2(peakMeans[i], peakStds[i], peaksList[j][k], kMulti)
                    hitRatios.append(hitRatio)
                hitRatios = np.array(hitRatios)
                y.append(np.mean(hitRatios))
            ys.append(y)
       ## print(X)
      ##  print(ys)
        
        DrawHitLineChart2(X, ys, labels, labels[i])     
        plt.savefig(trainPrefix + ('@model=%d&pagesize=%d' % (i, PAGESIZE)))  
    """

    
    for i in range(MODE):
        # now at mode i
        print('now at mode %d' % i)
       ## print(Predict(allTestData[i],  peakMeans, peakStds, kX))
        result = []
        ##print(testDataList[i])
        for j in range(len(testDataList[i])):
            result.append(Predict(testDataList[i][j], peakMeans, peakStds, kX))
        print(result)
    
    
    # draw
   ## DrawEnvelope(meanCurves, stdCurves, labels) 
   ## DrawEnvelope(meanCurves, stdCurves, labels, False) 
    
    ## plt.savefig(figurePrefix + ('@pagesize=%d' % pagesize))
        

   ## DrawXYZ(trainingFileList)    
   ## DrawIndepenet(files)
   ## DrawMixed(data, files[0])               
   ## plt.show()       
    
    
if __name__ == '__main__':
    Run('0328_2_9600_d100', '0328_2_9600_d100')
    Run('0328_2_9600_d100', '0328_3_9600_d100')
    Run('0328_2_9600_d100', '0328_4_9600_d100')
    Run('0328_2_9600_d100', '0328_5_9600_d100')
   ## Run('0328_3_9600_d100', '0328_3_9600_d100')
   ## Run('0328_4_9600_d100', '0328_4_9600_d100')
   ## Run('0328_5_9600_d100', '0328_5_9600_d100')
    
    Run('0329_1', '0329_1')
    Run('0329_2', '0329_2')
    
    
    