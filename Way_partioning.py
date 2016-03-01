

f=open('lutrace.txt', 'r');
address=[];
for line in f:
	address.append(line);

f=open('blacktrace.txt', 'r')
address2=[];
for line in f:
    address2.append(line);




interleaved_list=[]
i=0

while i< len(address) and i< len(address2):
	interleaved_list.append(address[i])
	interleaved_list.append(address2[i])
	i += 1
for j in range(i, len(address)):
	interleaved_list.append(address[j])
for j in range(i, len(address2)):
	interleaved_list.append(address2[j])
  





print " This is way partitoning"




Cache1={};
Cache2={};

for i in range(0,len(interleaved_list)):
	interleaved_list[i]=int(interleaved_list[i],16);
	tag=(interleaved_list[i] >> 9) & ((1 << 23)-1);
	index=(interleaved_list[i] >> 4) & ((1 << 5)-1);
	
	Cache1[index]=[0,0,0];
	Cache2[index]=[0,0,0];
	


hit=0;
miss=0;

lru1=0;
lru2=0;

c=0;
d=0;
count=0;


for i in range(0,len(address2+address)):

	
	if (count < 20 and c < len(address) ):
		a=int(address[c],16)
		tag=(a >> 9) & ((1 << 23)-1)
		index=(a >> 4)& ((1 << 5)-1)
		c=c+1;
		count=count+1;
		pid=1;
	elif(count >=20 and d < len(address2)):
		a=int(address2[d],16)
		tag= (a >> 9) & ((1 << 23)-1)
		index=(a >> 9)& ((1 << 5)-1)
		d=d+1
		count=count+1
		pid=2;
		if(count == 40):
			count=0;
			
	
	val1=Cache1[index];
	val2=Cache2[index];

	tag1=val1[0];
	lru1=val1[1];
	id1=val1[2]

	tag2=val2[0];
	lru2=val2[0];
	id2=val1[2];

	if(tag == tag1 and id1==pid):
			hit=hit+1;
			lru1=lru1+1;
			lru1=min(1,lru1);
			lru2=lru2-1;
			lru2=max(0,lru2);

	elif(tag==tag2 and id2==pid):
	        hit=hit+1;
	        lru2=lru2+1;
	        lru2=min(1,lru2);
	        lru1=lru1-1
	        lru1=max(0,lru1);
	else:
	        if(min(lru1,lru2)==lru1):
	        	miss=miss+1;
	        	lru1=1;
	        	Cache1[index]=[tag,lru1,pid];
	        	lru2=0;
	        	Cache2[index]=[tag2,lru2,id2]
	        elif(min(lru1,lru2)==lru2):
	        	miss=miss+1
	        	lru2=1;
	        	Cache2[index]=[tag,lru2,pid];
	        	lru1=0;
	        	Cache1[index]=[tag1,lru1,id1];
	        elif(lru1==lru2):
	        	 miss=miss+1
	        	 lru1=1;
	        	 Cache1[index]=[tag,lru1,pid];
	        	 lru2=0;
	        	 Cache2[index]=[tag2,lru2,id2];    	

	
	
	



	
	
	
    
	

	
		
        
	

print Cache1;
print Cache2;	        
	    
print (hit*100)/(hit+miss)
    

	    
