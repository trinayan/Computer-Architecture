
                     	


f=open('lutrace.txt', 'r');
address=[];
for line in f:
	address.append(line);

f=open('blacktrace.txt', 'r')
address2=[];
for line in f:
    address2.append(line);

processor_id=[];
#processor_id= interleave(len(address),len(address2));


print len(processor_id);
print " This is size partitoning"

interleaved_list=[];
i=0;

while i< len(address) and i< len(address2):
	interleaved_list.append(address[i])
	interleaved_list.append(address2[i])
	i += 1
for j in range(i, len(address)):
	interleaved_list.append(address[j])
for j in range(i, len(address2)):
	interleaved_list.append(address2[j])



Cache1={};
Cache2={};

for i in range(0,len(interleaved_list)):
	interleaved_list[i]=int(interleaved_list[i],16);
	tag=(interleaved_list[i] >> 9) & ((1 << 23)-1);
	index=(interleaved_list[i] >> 4) & ((1 << 5)-1);
	
	Cache1[index]=0;
	Cache2[index]=0;
	
print len(interleaved_list);

hit=0;
miss=0;

lru1=0;
lru2=0;
c=0;
d=0;
count=0;
for i in range(0,len(address+address2)):
	if (count < 200000 and c < len(address) ):
		a=int(address[c],16)
		tag=(a >> 9) & ((1 << 23)-1)
		index=(a >> 4)& ((1 << 5)-1)
		c=c+1;
		count=count+1
		pid=1;
	elif(count >=200000 and d < len(address2)):
		pid=2;
		a=int(address2[d],16)
		tag= (a >> 9) & ((1 << 23)-1)
		index=(a >> 9)& ((1 << 5)-1)
		d=d+1
		count=count+1
		if(count == 400000):
			count=0;
	
	
	
    
	tag1=Cache1[index];
	tag2=Cache2[index];

	

	if(pid == 1):
		if(tag1==tag):
			hit=hit+1;
		else:
		    miss=miss+1;
		    Cache1[index]=tag;
	elif(pid == 2):
	    if(tag2==tag):
	        hit=hit+1;
	    else:
	        miss=miss+1;
	        Cache2[index]=tag;    	    		    		    

	

	
		

	        
	    


print (hit*100/(hit+miss));
print miss;    	    
print Cache1;
print Cache2;

    	    	    
