from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
import pandas as pd
import copy
from tslib import tsUtils
from tslib.synthcontrol.syntheticControl import RobustSyntheticControl
from tslib.synthcontrol.multisyntheticControl import MultiRobustSyntheticControl
import math
from matplotlib.pyplot import figure
import random

def rankDiagnostic(filename_metric, filename_secondary_metric):
    df1 = pd.read_csv(filename_metric)
    df1 = df1.drop(['id'], axis=1)
    df1 = df1.fillna(axis=1, method='ffill')

    df2 = pd.read_csv(filename_secondary_metric)
    df2 = df2.drop(['id'], axis=1)
    df2 = df2.fillna(axis=1, method='ffill')

    M1 = np.matrix(df1.values, dtype='float')
    d11,d12 = M1.shape

    M2 = np.matrix(df2.values, dtype='float')
    d21, d22 = M2.shape

    M = np.zeros([d11, d12+d22])
    M[:, 0:d12] = M1
    M[:, d12:] = M2
    d1,d2 = M.shape

    u, s, v = np.linalg.svd(M1, full_matrices=False)
    u, s_, v = np.linalg.svd(M2, full_matrices=False)
    u, sA, v = np.linalg.svd(M, full_matrices=False)

    k = 50

    plt.subplot(3, 1, 1)
    plt.plot(range(0, k), s[0:k], color='magenta', label=f'metric1 rank {np.linalg.matrix_rank(M1)}')
    plt.title('Diagnostic: Rank Preservation Property')
    plt.xlabel('Singular Value Index (largest to smallest)')
    plt.ylabel('Singular Value')
    legend = plt.legend(loc='best', shadow=True)

    plt.subplot(3, 1, 2)
    plt.plot(range(0, k), s_[0:k], color='black', label=f'metric2 rank {np.linalg.matrix_rank(M2)}')
    plt.xlabel('Singular Value Index (largest to smallest)')
    plt.ylabel('Singular Value')
    legend = plt.legend(loc='best', shadow=True)

    plt.subplot(3, 1, 3)
    plt.plot(range(0, k), sA[0:k], color='blue', label=f'Combined rank {np.linalg.matrix_rank(M)}')
    plt.xlabel('Singular Value Index (largest to smallest)')
    plt.ylabel('Singular Value')
    legend = plt.legend(loc='best', shadow=True)

    plt.show()

def score_rsc(filename, idColumnName, treatment, start, training_end, test_end, MetricName):
    df = pd.read_csv(filename)
    allColumns = df.columns.values
    country_list = list(np.unique(df[idColumnName]))
    days = np.delete(allColumns, [0])

    treatment = treatment

    country_list.remove(treatment)
    control_group = country_list

    start = start
    training_end = training_end
    test_end = test_end
    singvals = 20
    p = 1.0

    trainingDays = []
    for i in range(start, training_end, 1):
        trainingDays.append(str(i))

    testDays = []
    for i in range(training_end, test_end, 1):
        testDays.append(str(i))

    trainDataMasterDict = {}
    trainDataDict = {}
    testDataDict = {}

    for key in control_group:
        series = df[df[idColumnName] == key]
        trainDataMasterDict.update({key: series[trainingDays].values[0]})

        # randomly hide training data
        (trainData, pObservation) = tsUtils.randomlyHideValues(copy.deepcopy(trainDataMasterDict[key]), p)
        trainDataDict.update({key: trainData})
        testDataDict.update({key: series[testDays].values[0]})

    series = df[df[idColumnName] == treatment]
    trainDataMasterDict.update({treatment: series[trainingDays].values[0]})
    trainDataDict.update({treatment: series[trainingDays].values[0]})
    testDataDict.update({treatment: series[testDays].values[0]})

    trainMasterDF = pd.DataFrame(data=trainDataMasterDict)
    trainDF = pd.DataFrame(data=trainDataDict)
    testDF = pd.DataFrame(data=testDataDict)

    # model
    rscModel = RobustSyntheticControl(treatment, singvals, len(trainDF), probObservation=1.0, modelType='svd',
                                      svdMethod='numpy', otherSeriesKeysArray=control_group)

    # fit the model
    rscModel.fit(trainDF)

    # save the denoised training data
    denoisedDF = rscModel.model.denoisedDF()

    # predict - all at once
    predictions = rscModel.predict(testDF)

    # plot
    daysToPlot = range(start, test_end, 1)
    interventionDay = training_end - 1
    plt.plot(daysToPlot, np.append(trainMasterDF[treatment], testDF[treatment], axis=0), color='red',
             label='observations')
    plt.plot(daysToPlot, np.append(denoisedDF[treatment], predictions, axis=0), color='blue', label='predictions')
    plt.axvline(x=interventionDay, linewidth=1, color='black', label='Lockdown Day')
    legend = plt.legend(loc='best', shadow=True)
    plt.title(f'{treatment}', fontsize=8)
    plt.xlabel('Dates')
    plt.ylabel(MetricName)
    plt.show()



def score_mrsc(filename_metric, filename_secondary_metric, idColumnName, treatment, start, training_end, test_end, MetricName, country):
    df1 = pd.read_csv(filename_metric)

    df2 = pd.read_csv(filename_secondary_metric)

    allColumns = df1.columns.values
    country_list = list(np.unique(df1[idColumnName]))
    days = np.delete(allColumns, [0])

    treatment = treatment

    country_list.remove(treatment)
    control_group = country_list

    start = start
    training_end = training_end
    test_end = test_end

    singvals = 10
    p = 1.0

    trainingDays = []
    for i in range(start, training_end, 1):
        trainingDays.append(str(i))

    testDays = []
    for i in range(training_end, test_end, 1):
        testDays.append(str(i))

    trainDataMasterDict1 = {}
    trainDataDict1 = {}
    testDataDict1 = {}

    trainDataMasterDict2 = {}
    trainDataDict2 = {}
    testDataDict2 = {}


    for key in control_group:
        series1 = df1[df1[idColumnName] == key]
        trainDataMasterDict1.update({key: series1[trainingDays].values[0]})

        # randomly hide training data
        (trainData1, pObservation1) = tsUtils.randomlyHideValues(copy.deepcopy(trainDataMasterDict1[key]), p)
        trainDataDict1.update({key: trainData1})
        testDataDict1.update({key: series1[testDays].values[0]})

        series2 = df2[df2[idColumnName] == key]
        trainDataMasterDict2.update({key: series2[trainingDays].values[0]})

        # randomly hide training data
        (trainData2, pObservation2) = tsUtils.randomlyHideValues(copy.deepcopy(trainDataMasterDict2[key]), p)
        trainDataDict2.update({key: trainData2})
        testDataDict2.update({key: series2[testDays].values[0]})

    series = df1[df1[idColumnName] == treatment]
    trainDataMasterDict1.update({treatment: series[trainingDays].values[0]})
    trainDataDict1.update({treatment: series[trainingDays].values[0]})
    testDataDict1.update({treatment: series[testDays].values[0]})

    trainMasterDF1 = pd.DataFrame(data=trainDataMasterDict1)
    trainDF1 = pd.DataFrame(data=trainDataDict1)
    testDF1 = pd.DataFrame(data=testDataDict1)

    #-------
    series = df2[df2[idColumnName] == treatment]
    trainDataMasterDict2.update({treatment: series[trainingDays].values[0]})
    trainDataDict2.update({treatment: series[trainingDays].values[0]})
    testDataDict2.update({treatment: series[testDays].values[0]})

    trainMasterDF2 = pd.DataFrame(data=trainDataMasterDict2)
    trainDF2 = pd.DataFrame(data=trainDataDict2)
    testDF2 = pd.DataFrame(data=testDataDict2)

    relative_weights = [1.0, 1.0]

    # instantiate the model
    mrscModel = MultiRobustSyntheticControl(2, relative_weights, treatment, singvals, len(trainDF1),
                                            probObservation=1.0, svdMethod='numpy', modelType='svd',
                                            otherSeriesKeysArray=control_group)

    # fit the model
    mrscModel.fit([trainDF1, trainDF2])

    # save the denoised training data
    denoisedDF = mrscModel.model.denoisedDF()

    # predict - all at once
    predictions = mrscModel.predict([testDF1,testDF2])

    final_deaths_predicted = math.ceil(max(predictions[0]))
    final_cases_predicted = abs(math.floor(max(predictions[1])))

    final_deaths_actual = int(max(testDF1[treatment].values.tolist()))
    final_cases_actual = int(max(testDF2[treatment].values.tolist()))


    # plot
    daysToPlot = range(start, test_end, 1)
    interventionDay = training_end - 1
    plt.plot(daysToPlot, np.append(trainMasterDF1[treatment], testDF1[treatment], axis=0), color='red',
             label='observations')
    plt.plot(daysToPlot, np.append(denoisedDF[treatment][start:training_end], predictions[0], axis=0), color='blue', label='predictions')
    plt.axvline(x=interventionDay, linewidth=1, color='black', label='Lockdown Day')
    legend = plt.legend(loc='best', shadow=True)
    plt.title(f'{treatment} \n Actual - Deaths:{final_deaths_actual}, Confirmed:{final_cases_actual} \n Predicted - Deaths: {final_deaths_predicted}, Confirmed:{final_cases_predicted}', fontsize=8)
    plt.xlabel('Days')
    plt.ylabel(MetricName)
    plt.savefig(f'../img/{country}/{treatment}.png')