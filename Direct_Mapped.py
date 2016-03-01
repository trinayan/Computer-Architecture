



f=open('lutrace.txt', 'r');
address=[];
for line in f:
	address.append(line);

f=open('blacktrace.txt', 'r')
address2=[];
for line in f:
    address2.append(line);

i=0


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



print len(address);
print len(address2);



Cache={};

for i in range(0,len(interleaved_list)-1):
	interleaved_list[i]=int(interleaved_list[i],16);
	tag=(interleaved_list[i] >> 10) & ((1 << 22)-1);
	index=(interleaved_list[i] >> 4)& ((1 << 6)-1);
	

	Cache[index]=[0,0];
	

print("Doing please wait");

hit=0;
miss=0;
count=0;
c=0;
d=0;

for i in range(0,len(address+address2)):
	
    if (count < 200000 and c < len(address) ):
    	a=int(address[c],16)
    	tag=(a >> 10) & ((1 << 22)-1)
    	index=(a >> 4)& ((1 << 6)-1)
    	c=c+1;
    	count=count+1
        pid=1;
    elif(count >=200000 and d < len(address2)):
    	a=int(address2[d],16)
    	tag= (a >> 10) & ((1 << 22)-1)
    	index=(a >> 4)& ((1 << 6)-1)
    	d=d+1
    	count=count+1
        pid=2;
    	if(count == 400000):
    		count=0;
        	
	


    val=Cache[index];
    tagvalue=val[0];
    identity=val[1]

    if(tagvalue==tag and identity==pid):
		hit=hit+1;
    else:
		miss=miss+1;
		Cache[index]=[tag,pid];


print (hit*100)/(hit+miss)
print Cache
