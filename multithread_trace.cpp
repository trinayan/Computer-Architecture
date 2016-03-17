/*BEGIN_LEGAL 
Intel Open Source License 

Copyright (c) 2002-2012 Intel Corporation. All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.  Redistributions
in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.  Neither the name of
the Intel Corporation nor the names of its contributors may be used to
endorse or promote products derived from this software without
specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
END_LEGAL */
/*
 *  This file contains an ISA-portable PIN tool for tracing memory accesses.
 */

#include <stdio.h>
#include "pin.H"


FILE * trace1;
FILE * trace2;
FILE * fulltrace;
FILE * currenthread;
PIN_LOCK lock;
INT32 numThreads=0;
const INT32 MaxNumThreads = 10000;

// Print a memory read record
static VOID PIN_FAST_ANALYSIS_CALL  RecordMemRead(VOID * ip, VOID * addr, THREADID tid)
{
    if(tid == 0)
   {
     // fprintf(trace1,"%p\n",  addr);
   }
  
   else
   {
    // fprintf(trace2, "%p\n" , addr);
   }
}


// Print a memory write record
VOID RecordMemWrite(VOID * ip, VOID * addr, THREADID tid)
{
 
 if(tid == 0)
   {
      fprintf(trace1,"%p\n", addr);
   }

   else
   {
     fprintf(trace2,"%p\n", addr);
   }

   PIN_GetLock(&lock,tid+1);
   fprintf(fulltrace, "%p\n", addr);
   fprintf(currenthread, "%d\n",tid);
   PIN_ReleaseLock(&lock);
   
}

VOID ThreadStart(THREADID threadid, CONTEXT *ctxt, INT32 flags, VOID *v)
{
   PIN_GetLock(&lock, threadid+1);
   numThreads++;
   PIN_ReleaseLock(&lock);

   ASSERT(numThreads <= MaxNumThreads, "Max number of threads exceeded\n");
}

// Is called for every instruction and instruments reads and writes
VOID Instruction(INS ins, VOID *v)
{
    // Instruments memory accesses using a predicated call, i.e.
    // the instrumentation is called iff the instruction will actually be executed.
    //
    // The IA-64 architecture has explicitly predicated instructions. 
    // On the IA-32 and Intel(R) 64 architectures conditional moves and REP 
    // prefixed instructions appear as predicated instructions in Pin.
    UINT32 memOperands = INS_MemoryOperandCount(ins);

    // Iterate over each memory operand of the instruction.
    for (UINT32 memOp = 0; memOp < memOperands; memOp++)
    {
        if (INS_MemoryOperandIsRead(ins, memOp))
        {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)RecordMemRead,IARG_FAST_ANALYSIS_CALL,
                IARG_INST_PTR,
                IARG_MEMORYOP_EA, memOp,
                IARG_THREAD_ID,
                IARG_END);
        }
        // Note that in some architectures a single memory operand can be 
        // both read and written (for instance incl (%eax) on IA-32)
        // In that case we instrument it once for read and once for write.
        if (INS_MemoryOperandIsWritten(ins, memOp))
        {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)RecordMemWrite,
                IARG_INST_PTR,
                IARG_MEMORYOP_EA, memOp,
                IARG_THREAD_ID,
                IARG_END);
        }
    }
}

VOID Fini(INT32 code, VOID *v)
{
    
    fclose(trace1);
    fclose(trace2);
    fclose(fulltrace);
    fclose(currenthread);
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */
   
INT32 Usage()
{
    PIN_ERROR( "This Pintool prints a trace of memory addresses\n" 
              + KNOB_BASE::StringKnobSummary() + "\n");
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */

int main(int argc, char *argv[])
{
    if (PIN_Init(argc, argv)) return Usage();

    trace1 = fopen("thread1.txt", "w");
    trace2=  fopen("thread2.txt", "w");
    fulltrace=fopen("fulltrace.txt", "w");    
    currenthread=fopen("currenthread.txt", "w");    

    INS_AddInstrumentFunction(Instruction, 0);
    PIN_AddFiniFunction(Fini, 0);

    // Never returns
    PIN_StartProgram();
    
    return 0;
}
