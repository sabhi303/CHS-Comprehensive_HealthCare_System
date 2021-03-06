import numpy as np
import pandas as pd
# from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import plot_confusion_matrix

from sklearn.model_selection import train_test_split
import operator
import matplotlib.pyplot as plt  


def kn(inp):
    from sklearn.neighbors import KNeighborsClassifier
    train=pd.read_csv('disease/Training.csv',header=0)
    xtrain=train.iloc[:,:-1]
    ytrain=train.iloc[:,-1]
    # xtrain,xtest,ytrain,ytest=train_test_split(xtrain,ytrain, test_size=0.3, random_state=100)
    test=pd.read_csv('disease/Testing.csv',header=0)
    xtest=test.iloc[:,:-1]
    ytest=test.iloc[:,-1]
    # acc={}
    # for k in range(2,30):
    knn=KNeighborsClassifier(19)
    knn.fit(xtrain,ytrain)
    ypred=knn.predict(xtest)
    acc=int(accuracy_score(ypred,ytest)*100)
    print(acc)

    input=[]
    for i in xtrain.columns:
        if(i in inp):
            input.append(1)
        else:
            input.append(0)
    # input=input[:-1]
    pred=knn.predict([input])
    print(pred)
    return [acc,pred[0]]

def nb(inp):
    from sklearn.naive_bayes import GaussianNB
    train=pd.read_csv('Training.csv',header=0)
    xtrain=train.iloc[:,:-1]
    ytrain=train.iloc[:,-1]
    # xtrain,xtest,ytrain,ytest=train_test_split(xtrain,ytrain, test_size=0.3, random_state=100)
    test=pd.read_csv('Testing.csv',header=0)
    xtest=test.iloc[:,:-1]
    ytest=test.iloc[:,-1]
    gnb=GaussianNB()
    gnb.fit(xtrain,ytrain)
    plot_confusion_matrix(gnb, xtest, ytest) 
    plt.show()
    ypred=gnb.predict(xtest)
    acc=int(accuracy_score(ypred,ytest)*100)
    print(acc)
    print(confusion_matrix(ypred,ytest))

    input=[]
    for i in xtrain.columns:
        if(i in inp):
            input.append(1)
        else:
            input.append(0)
    # input=input[:-1]
    pred=gnb.predict([input])
    print(pred)
    
    return [acc,pred[0]]

def lr(inp):
    from sklearn.linear_model import LogisticRegression
    train=pd.read_csv('disease/Training.csv',header=0)
    xtrain=train.iloc[:,:-1]
    ytrain=train.iloc[:,-1]
    # xtrain,xtest,ytrain,ytest=train_test_split(xtrain,ytrain, test_size=0.3, random_state=100)
    test=pd.read_csv('disease/Testing.csv',header=0)
    xtest=test.iloc[:,:-1]
    ytest=test.iloc[:,-1]
    log=LogisticRegression()
    log.fit(xtrain,ytrain)
    ypred=log.predict(xtest)
    acc=int(accuracy_score(ypred,ytest)*100)
    print(acc)

    input=[]
    for i in xtrain.columns:
        if(i in inp):
            input.append(1)
        else:
            input.append(0)
    # input=input[:-1]
    pred=log.predict([input])
    print(pred)
    return [acc,pred[0]]

def dt(inp):
    from sklearn.tree import DecisionTreeClassifier
    train=pd.read_csv('disease/Training.csv',header=0)
    xtrain=train.iloc[:,:-1]
    ytrain=train.iloc[:,-1]
    # xtrain,xtest,ytrain,ytest=train_test_split(xtrain,ytrain, test_size=0.3, random_state=100)
    test=pd.read_csv('disease/Testing.csv',header=0)
    xtest=test.iloc[:,:-1]
    ytest=test.iloc[:,-1]
    dtc=DecisionTreeClassifier(criterion = "gini", random_state = 100,max_depth=133, min_samples_leaf=5)
    dtc.fit(xtrain,ytrain)
    print("dt")
    ypred=dtc.predict(xtest)
    print(ypred)
    acc=int(accuracy_score(ypred,ytest)*100)
    print(acc)

    input=[]
    for i in xtrain.columns:
        if(i in inp):
            input.append(1)
        else:
            input.append(0)
    # input=input[:-1]
    pred=dtc.predict([input])
    print(pred)
    return [acc,pred[0]]
# lr(["vomiting","nausea"])
# kn(["vomiting","nausea"])
# nb(["vomiting","nausea"])
# dt(["vomiting","nausea"])


