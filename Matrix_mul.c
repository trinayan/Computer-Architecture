#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

#define N 700

#define LOOP 10  

static double a[N][N], b[N][N] , c[N][N];

int no_threads;


void* matmul2 (void* identifier)
{
  
  

  int id=(int)identifier;

  int row_per_thread = (N / no_threads);

       

  int begin = (id * row_per_thread);
  int end = begin+row_per_thread;
  
  
  

  int i,j,k;

  int temp_sum;
  
  for (i=begin; i<end ; i++) 
  {
    for (j=0; j<N; j++) 
    {
      temp_sum=0;
      for (k=0; k<N; k++)
      {
        temp_sum = temp_sum + a[i][k]*b[j][k];
      }
      c[i][j]=temp_sum;
      
    }
  }
  


 
  return 0;
}

void* matmul (void* identifier)
{
  



  int i,j,k;
  double temp;
  int error2;


   int no_internal_threads=2;

   pthread_t *internal_threads;
   internal_threads=malloc(no_threads*sizeof(pthread_t));

   for (i=0; i < no_internal_threads;i++)
   {
    error2=pthread_create(&internal_threads[i],NULL,matmul2, (void *)i);
    if (error2!=0)
    {
      printf(" \n Thread creation failed due to some reason");
    }
     
   }

   int join_error2;

   for(i=0; i < no_internal_threads;i++)
   {
    join_error2=pthread_join(internal_threads[i], NULL);
    if(join_error2!= 0)
      {
       
        printf("Join failed");
      }
   }

  printf("a result %g \n", fabs(c[7][8]));
  
  return 0;
  
  

}

int main(int argc, char *argv[])
{

  
  
  no_threads=LOOP;
   
   int error;
  
  int i,j,temp;


  for(i=0; i<N; i++){    
    for(j=0; j<N; j++)
    {
      a[i][j] = (double)(i+j);
      b[i][j] = (double)(i-j);
    }
  }

  for(i=0; i<N; i++)
  {
    for(j=0; j<N; j++)
    {
      temp=b[i][j];
      b[i][j]=b[j][i];
      b[j][i]=temp;
    }
  }


  pthread_t *thread ;

  thread= malloc(no_threads*sizeof(pthread_t));

  for (i=0; i<no_threads; i++)
   {
    error=pthread_create(&thread[i],NULL,matmul, (void *)i);
    if (error!=0)
    {
      printf(" \n Thread creation failed due to some reason");
    }
    
   }


   int join_error;

   for(i=0; i<no_threads;i++)
   {
      join_error=pthread_join(thread[i], NULL);
      if(join_error!= 0)
      {
       
        printf("Join failed");
      }
   }

 
   
  printf("Matrix Mul Completed \n");
  
  return 0;

}











