import collections

f=open('branchtrace_gzip.txt', 'r')
branches=[];
for line in f:
	branches.append(line);

f=open('branchdecision_gzip.txt', 'r')
decision=[];
for line in f:
    decision.append(line);

BHT={};
correct=0;
incorrect=0;

topbranches=[0]*len(branches);

PRT={};
HHRT={}
historylength=10;
value2=pow(2,historylength)


for i in range(0,len(branches)):
	branches[i]=int(branches[i],16)
	historykey= branches[i]%value2;
	HHRT[historykey]=0;

for i in range(0,value2):
    PRT[i]=0;

correct=0;incorrect=0;predict=0;findex=0;

histindex=0;
for i in range(0,len(branches)):
	histindex=branches[i]%value2;
	entry=HHRT[histindex];
	predict=PRT[entry];
  
	result=int(decision[i]);
	if (predict==2 or predict==3) :
		    
		        if (result == 1):

		                PRT[entry]=PRT[entry]+1;
		                if (PRT[entry] > 3):
		                    PRT[entry]=3;


		                value=HHRT[histindex];
		                value=value<<1;
		                value=value | 1;
		                value&=(1<<historylength)-1;
		                HHRT[histindex]=value;
		                correct=correct+1;

		        else      :
		                 PRT[entry]=PRT[entry]-1;
		                 value=HHRT[histindex];
		                 value=value<<1;
		                 value=value | 0;
		                 value&=(1<<historylength)-1;
		                 HHRT[histindex]=value;
		                 incorrect=incorrect+1;
		                 topbranches.append(hex(branches[i]));
	else:
	            if  (result==1):
	            	                 PRT[entry]=PRT[entry]+1;
	            	                 value=HHRT[histindex];
	            	                 value=value<<1;
	            	                 value=value | 1;
	            	                 value&=(1<<historylength)-1;
	            	                 HHRT[histindex]=value;
	            	                 incorrect=incorrect+1;
	            	                 topbranches.append(hex(branches[i]))
	            else           :
	            	                PRT[entry]=PRT[entry]-1;
	            	                if (PRT[entry] < 0):
	            	                    PRT[entry]=0;


	            	                value=HHRT[histindex];
	            	                value=value<<1;
	            	                value=value | 0;
	            	                value&=(1<<historylength)-1;
	            	                HHRT[histindex]=value;
	            	                correct=correct+1;

accuracy=(correct*100)/len(branches)
print incorrect;
print accuracy;	                 
print PRT;

counter2=collections.Counter(topbranches);
print counter2;

		