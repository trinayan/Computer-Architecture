f=open('thread1.txt', 'r')
t1=[];
for line in f:
	t1.append(line);


f=open('thread2.txt', 'r')
t2=[];
for line in f:
	t2.append(line);

f=open('fulltrace.txt', 'r')
trace=[]
for line in f:
	trace.append(line)

f=open('currenthread.txt', 'r')
current_thread=[]
for line in f:
	current_thread.append(line)


#Find all common memory locations accessed by both threads.
t3= list(set(t1).intersection(t2));
t3=list(t3);

print len(t3);

counter1=0;
counter2=0;
success=0;
transactions=0;

    

quantum=0;
conflict=0;

t1list=[0]*4;
t2list=[0]*4;


j=0;
k=0;
m=0;
count=0;
a=0;
execute=[]

for i in range(0,len(trace)):
	current_memory =  trace[i];
	

	if(current_memory in t3):   # If the variable is in the shared variables set between the two threads mark it as the start of the transaction
		
		if(quantum == 0):
		    start=i;

		thread = int(current_thread[i]);  #get the thread ID
		   
		quantum=quantum+1;

		if (thread == 0):
			counter1 = counter1+1;
			t1list[m]= current_memory;
			m=m+1;

		elif(thread == 1):
		    counter2 = counter2+1;
		    t2list[k]= current_memory;
		    k=k+1;

        
        if (quantum == 4):                # run the transaction for a length for "quantum" shared memory writes and check if there was no conflicts to shared variables
        	quantum=0;
        	transactions = transactions+1; # transaction completed. now check if its valid
        	end=i;
        	difference=end-start
            
        	t3x = list(set(t1list).intersection(t2list));
        	t3x = list(t3x);
        	for j in range(0,len(t3x)):
        		a=t3x[j];

            	if(a != 0):
            		
            		count=count+1;
            

        	for j in range(0,4):
        	    t1list[j]=0;
        	    t2list[j]=0;
        	    
        	
        	   
        	if (count == 0):
        	    success=success+1;
        	    execute.append(difference)    

        	for j in range(0,len(t3x)):
        		t3x[j]=0

        	m=0;
        	k=0;
        	count=0;	
        	end=0;

        	
 

total=0;

for i in range(0,len(execute)):
	total=total+execute[i];



total=total/len(execute)
        

print success;        		
print transactions;

print total;
