
import collections

f=open('branchtrace.txt', 'r')
branches=[];
for line in f:
	branches.append(line);

f=open('branchdecision.txt', 'r')
decision=[];
for line in f:
    decision.append(line);

BHT={};
correct=0;
incorrect=0;

topbranches=[0]*len(branches);



for i in range(0,len(branches)):
	branches[i]=int(branches[i],16)
	key=branches[i]%1024;
	decision[i]=int(decision[i]);
	BHT[key]=1;

hit=0;


for i in range(0,len(branches)):
    key=branches[i]%1024;
    result=decision[i];
    
    if (result == 1):
    	hit=hit+1;

    prediction=BHT[key];



    if(prediction==2 or prediction==3):
      if(result==1):
           BHT[key]=BHT[key]+1;
           if (BHT[key] > 3):
           	  BHT[key]=3;
           correct=correct+1	  
           
      else:
           BHT[key]=BHT[key]-1;
           incorrect=incorrect+1;
           topbranches.append(hex(branches[i]))

    else:
        if (result==1):
            BHT[key]=BHT[key]+1;
            incorrect=incorrect+1;
            topbranches.append(hex(branches[i]))  
        else:
            BHT[key]=BHT[key]-1;
            if (BHT[key] < 0):
            	BHT[key]=0;
            correct=correct+1;

accuracy= (correct*100)/(correct+incorrect);
print accuracy;


counter2=collections.Counter(topbranches);
print counter2;
