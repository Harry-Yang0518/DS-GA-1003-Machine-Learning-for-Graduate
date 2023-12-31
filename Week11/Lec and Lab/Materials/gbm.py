import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
import sklearn

X = np.array([1,2,3,4,8,9,10,11,15,16,17,18]).reshape(12,1)
Y = np.array([1,1,10,2,-4,-5,-10,-3,0,1,-1,5])
# Y = np.array([0,0,0,1,1,0,0,0,0,0,0,0]) # outlier 

n = 300
Xtest = np.linspace(0,20,n).reshape(-1,1)

depth = 1 #decision stump
stepsize = 1

i = 0

print(sklearn.__version__)

def onclick(event) :
    plot()

def plot() :
    global i,depth,stepsize,n
    est = GradientBoostingRegressor(n_estimators=i+1,learning_rate=stepsize,loss='squared_error',max_depth=depth).fit(X,Y)
    pest = GradientBoostingRegressor(n_estimators=i,learning_rate=stepsize,loss='squared_error',max_depth=depth).fit(X,Y) if i > 0 else None
    fig1 = plt.figure(1)
    plt.clf()
    pY = pest.predict(Xtest) if i>0 else np.zeros(n)
    plt.plot(Xtest,pY,label='Fit at Stage %d'%i)
    plt.plot(Xtest,est.predict(Xtest),label='Fit at Stage %d'%(i+1))
    plt.scatter(X,Y)
    plt.title('Least Squares From Stage %d -> %d (Press any key to advance)'%(i,i+1))
    plt.legend()
    plt.draw()
    
    pY = pest.predict(X) if i>0 else np.zeros(12)
    print('Pseudoresiduals For Least Squares At Stage %d'%i)
    print(est.loss_.negative_gradient(Y,pY))
    
    gbr = GradientBoostingRegressor(n_estimators=i+1,learning_rate=stepsize,loss='absolute_error',max_depth=depth)
    pgbr = GradientBoostingRegressor(n_estimators=i,learning_rate=stepsize,loss='absolute_error',max_depth=depth)
    est = gbr.fit(X,Y)
    pest = pgbr.fit(X,Y) if i > 0 else None

    fig2 = plt.figure(2)
    plt.clf()
    pY = pest.predict(Xtest) if i>0 else np.zeros(n)
    plt.plot(Xtest,pY,label='Fit at Stage %d'%i)
    plt.plot(Xtest,est.predict(Xtest),label='Fit at Stage %d'%(i+1))
    plt.scatter(X,Y)
    plt.title('Least Absolute Deviation From Stage %d -> %d'%(i,i+1))
    plt.legend()
    plt.draw()
    
    pY = pest.predict(X) if i>0 else np.zeros(12)    
    print('Pseudoresiduals For Least Absolute Deviation At Stage %d'%i)
    print(est.loss_.negative_gradient(Y,pY))

    fig1.canvas.mpl_connect('key_press_event',onclick)
    fig2.canvas.mpl_connect('key_press_event',onclick)

    i = i+1

plot()
plt.show()
