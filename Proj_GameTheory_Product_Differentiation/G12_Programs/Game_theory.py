#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
i=int(input("For identical products press 1\nFor complementary products enter 2\n"))
#Model implementing Best response and equilibrium pricing for perfect substitutes
if(i==1):
    #Competetion Parameter 
    c=2
    #Initial Constant
    a=1000
    #Parameter evaluating Impact of price of product on demand of product
    b=4
    #Set cost of the product
    m=320
    pj=460
    print("Competitor's price "+ str(pj))
    #input price of competitor product
    #m=int(input("Marginal cost of the product\n"))
    #pj=int(input("Enter price offered by competitor\n"))
    pi_br=(a+(b*m)+(c*pj))/(2*b)
    pi_eq=(a+(b*m))/((2*b)-c)
    print("Best response price for the company is "+ str(pi_br))
    print("Equilibrium price for both companies is "+str(pi_eq))
    #Plotting Best Response
    plt.axis([0, 1000, 0, 1000])
    plt.xlabel("Firm's Price") 
    # naming the y axis 
    plt.ylabel("Competitor's Price") 
    # giving a title to my graph 
    plt.title('Best Response Function') 
    y=np.arange(0,1000)
    x=(a+(b*m)+(c*y))/(2*b)
    plt.plot(x,y,label="Best Response for company")
    x=np.arange(0,1000)
    y=(a+(b*m)+(c*x))/(2*b)
    plt.plot(x,y,label="Best Response for competitor")
    plt.legend()
    plt.show()

#Model implementing Best responsefor complementary products
if(i==2):
    #Competetion Parameter 
    c=-2
    #Initial Constant
    a=1000
    #Parameter evaluating Impact of price of product on demand of product
    b=4
    #Set cost of the product
    m=320
    #input price of competitor product
    pj=40
    #input price of competitor product
    #m=int(input("Marginal cost of the product\n"))
    #pj=int(input("Enter price offered by competitor\n"))
    print("Competitor's price "+ str(pj))    
    pi_br=(a+(b*m)+(c*pj))/(2*b)
    #pi_eq=(a+(b*m))/((2*b)-c)
    print("Best response price for the company is "+ str(pi_br))
    #Plotting Best Response
    plt.axis([0, 1000, 0, 1000])
    plt.xlabel("Firm's Price") 
    # naming the y axis 
    plt.ylabel("Competitor's Price") 
    # giving a title to my graph 
    plt.title('Best Response Function') 
    y=np.arange(0,1000)
    x=(a+(b*m)+(c*y))/(2*b)
    plt.plot(x,y,label="Best Response for company")
    x=np.arange(0,1000)
    y=(a+(b*m)+(c*x))/(2*b)
    plt.plot(x,y,label="Best Response for competitor")
    plt.legend()
    plt.show()
    


# In[4]:


import math
import matplotlib.pyplot as plt
import numpy as np
def compute_cost(q,sai,theta):
    return (sai*(q**theta))

def compute_alpha(gamma,theta):
    alpha= (gamma+1)/(2*(gamma+1)-(gamma**theta)-gamma**(1-theta))
    return alpha

def compute_lamda(gamma):
    lamda=gamma+1+ math.sqrt((gamma**2)+gamma+1)
    return lamda

def compute_A(lamda,alpha,gamma,theta,q_0,v_max,c_0):
    A=(lamda/((2*lamda)-1))*(1-(alpha*(2-(gamma**(-theta)))) + (((gamma-1)/gamma)*((q_0*v_max)/c_0)))*c_0
    return A
#Taking input number of firms in the market
n=int(input("Enter number of firms\n"))
print("Enter quality for firm in decreasing order\n")
q=[]
#Taking input quality of firms    
for i in range(n):
    k=int(input("Enter quality for firm "+str(i+1)+"\n"))
    if (i>0):
        if (k>=q[i-1]):
            while(k>=q[i-1]):
                print("Quality of firm "+str(i+1)+" cannot be more than or equal to quality of previous firms\n")
                k=int(input("Enter quality for firm "+str(i+1)+"\n"))
            q.append(k)
        else:
            q.append(k)
    elif (i==0):
        q.append(k)
            
#setting parameters            
sai=4
theta=1.2
gamma=1.2
#Set vmax according to the maximum price public is willing to pay
v_max=20
c=[]
for i in range(n):
    c.append(compute_cost(q[i],sai,theta))
alpha=compute_alpha(gamma,theta)
lamda=compute_lamda(gamma)
A=compute_A(lamda,alpha,gamma,theta,q[0],v_max,c[0])
print("c= "+str(c))
print("alpha ="+str(alpha))
print("lamda= "+str(lamda))
print("A="+str(A))
dist_price={}
price={}
#Checking for constraints
if (alpha<1):
    print("Constraints not followed... Can't compute equilibrium prices")
else:
    print("Equilibrium prices for firms:\n")
    for i in range(n):
        k=-i
        p=A*(lamda**k) + alpha*c[i]
        dist_price[q[i]]=p
        price[q[i]]=alpha*c[i]
        print("Firm "+str(i+1)+": "+str(p)+"\n") 
#Plotting price vs quality graph        
plt.axis([0, q[0], 0, dist_price[q[0]]+10])
plt.xlabel("Firm's Quality") 
# naming the y axis 
plt.ylabel("Firm's Equilibrium Price") 
# giving a title to my graph 
plt.title('Pricing vs Quality') 
x=dist_price.keys()
y=dist_price.values()
plt.plot(x,y,label= "Distorted Elasticity")
x=price.keys()
y=price.values()
plt.plot(x,y, label="without distortion")
plt.legend()
plt.show()

