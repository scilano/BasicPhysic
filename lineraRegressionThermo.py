import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


parameters = {"font.size": 20, "axes.titlesize": 35}
plt.rcParams.update(parameters)

#Fake data, remplace with the reals one:
#V=[]
#P=[]
V = np.logspace(-1,1,50)
P = (1/V**1.4)*(1+np.random.normal(1,0.5,50))
logV = np.log(V)
logP = np.log(P)

#Compute linearRegression and plot
linearRegression = st.linregress(logV,logP)

a = linearRegression.slope
b = linearRegression.intercept
r = linearRegression.rvalue

plt.plot(logV,logP, marker='.', linestyle ='',label = "Experimental Data")
plt.plot(logV,a*logV + b, label ="Linear Regression")
plt.legend()

plt.text(-1.5,0,"gamma = {gamma:.2f}".format(gamma=np.abs(a)))
plt.text(-1.5,-1,f"r**2 = {r**2:.2f}")
plt.xlabel("log(V)")
plt.ylabel("log(P)")
plt.show()