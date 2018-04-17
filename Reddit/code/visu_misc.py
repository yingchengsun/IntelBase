'''
Created on Apr 10, 2018

@author: yingc
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from decorator import append
from io import BytesIO
import logging
from time import asctime
 
def piupiu():
    
    #logger = logging.getLogger('my logger')
    #logger.setLevel(logging.INFO)
    logging.warning('piupiu')

piupiu()
 
# create a file handler
 
#handler = logging.FileHandler('hello4.log')
#handler.setLevel(logging.INFO)

# create a logging format

for i in range(10):
    formatter = logging.Formatter('%(message)s')
        #handler.setFormatter(formatter)
         
        # add the handlers to the logger
         
        #logger.addHandler(handler)
         
        #logger.info('Hello baby')
        #logger.info(str(i)+'\t'+'6xauzw')
    #logger.warning('6xauzw')
        #tt.write(str(asctime())+str(i)+'\t'+'hello baby \n')


'''
df = pd.DataFrame({'key1':list('aabba'),
                  'key2': ['one','two','one','two','one'],
                  'data1': np.random.randn(5),
                  'data2': np.random.randn(5)})
print df
'''

arr1 = np.array([1,3,5,7,9])
#print arr1

arr2 = np.array((10,20,30,40,50))
#print arr2

arr3 = np.array([[1,2,3,4],[5,6,7,8],[3,4,5,6]])
#print arr3
'''
print arr3[[0,2],:]
print arr3[:,[0,1,3]]
print arr3[[0,2],:][:,[2,3]]
print arr3[np.ix_([0,2],[2,3])]
'''

arr = np.array([[ 3,  2],[ 1,  6],[ 2,  1],[ 0,  9],[ 4, 8],[ 5, 7]])  
#print arr
c = np.r_[arr,[[8,9]]]
#print c
'''
file = open('nn.txt','a')

a = 'asdf\n'
file.write(a)
a = a.strip('\n')
file.write(a)
print a


data = BytesIO("1 6 'ff'\n 4 5 'ee'")
#ndtype=[('a',int), ('b', float), ('c', int)]
ndtype = 'i,f,S10'
names = 'a,b,c'

d = np.genfromtxt(data, names=names, dtype=ndtype)
print d['a'],d['b']
row_vec = np.array([1, 2, 3])
col_vec = np.array([row_vec]).T

dd =  np.array([d['a']]).T
ddd =  np.array([d['b']]).T
print np.hstack((dd,ddd))

a_arg = np.argsort(d['b'])
print d[a_arg]
'''
'''
dd = d['b']
print dd[0:2]
nn = d['c']
x = range(len(d['c']))
plt.plot(x, d['b'])
plt.xticks(x,nn)
#plt.show()

print arr
aa = arr[np.argsort(arr[:,0])]

a = np.array([[1,2,3],[4,5,6],[0,0,1]])
a_arg = np.argsort(a[:,1])
print a
print a[a_arg]

nn = ['a','b','c','d','e']
N=5

index=np.arange(N)
plt.barh(index, y,color='r')
plt.yticks(index,nn)
plt.show()


mu=100
sigma=20
x=mu+sigma*np.random.randn(20000)
plt.hist(x,bins=100,color='green',normed=False)
plt.show()
'''

'''
def normfun(x,mu,sigma):
   pdf = np.exp(-((x-mu)**2)/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
   return pdfx=np.array([10,20,20,25,30])
mean = x.mean()  
sd = x.std() 
xx = range(len(x))
y = normfun(x,mean,sd)
plt.plot(xx,y) 
plt.show()    

plt.hist(x, bins = 6,rwidth=0.9,normed=True) 
plt.xlabel(u'subreddits') 
plt.ylabel(u'subscribers')
plt.show()  
'''

#t = '        rootfs                            1777284\n1443560\t333724  82% /'
'''
data = '988128\t\t444'
kwargs = dict(delimiter="\t",comments='%', dtype=int,names="a,b,c",missing_values={0:None, 'b':" ", 2:"???"},filling_values={0:0, 'b':0, 2:-999})
print np.genfromtxt(BytesIO(data), **kwargs)
'''
'''
from time import time 
t = time() 
list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
#list = dict.fromkeys(list,list) 
print zip(list,range(len(list)))
list = dict(zip(list,range(len(list))))
if not list.has_key('name'):
    print 'fuck'
filter = [] 
for i in range (1000000): 
    for find in ['is','hat','new','list','old','.']: 
        if find not in list: 
            filter.append(find) 
print "total run time:"
print time()-t
'''
'''
from time import time 

t = time() 
list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
total=[] 
for i in range (1000000): 
    for w in list: 
        total.append(w) 
print "total run time:"
print time()-t

t = time() 
list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
total=[] 
for i in range (1000000): 
    a = [w for w in list]
    total = ",".join(a)
print "total run time:"
print time()-t



t = time() 
list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
total=[] 
for i in range (1000000): 
    a = (w for w in list)
    total = ",".join(a)
print "total run time:"
print time()-t

t = time() 
list = ['a','b','is','python','jason','hello','hill','with','phone','test', 
'dfdf','apple','pddf','ind','basic','none','baecr','var','bana','dd','wrd'] 
total=[] 
for i in xrange (1000000): 
    a = (w for w in list)
    total = ",".join(a)
print type(total)
print [total]
print "total run time:"
print time()-t

a = {1,2,3}
print a
print type(a)


# initialize my_set
my_set = [1,2]
my_set.append(3)
print(my_set)

a_set=set()         
print a_set

print len(a_set)   

a_set.add(4)       
print a_set

a_set.update({2,4,6})   
print len(a_set)

data ='submission.txt'
d = np.genfromtxt(data, dtype='S10')
print d
print len(d)
with open(data,'a+') as subm:
    subm.write('aaa\n')
    subm.write('bbb\n')
print d
print len(d)


a = {'a':1,'b':2,'c':3}
a['d']=4
print a

a=[0, 1, 2, 3, 4]
aa=len(a)
print range(aa)
aa+=1
    
print aa
'''


with open('hello.log','a+') as hello:
    infile_subr_id = hello.readlines()
    print infile_subr_id
    ids = dict(zip(infile_subr_id,range(len(infile_subr_id))))
    print ids



