---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Understanding Virtual Memory Usage in Oracle GoldenGate"
subtitle: ""
summary: " "
tags: ["GoldenGate","Oracle"]
categories: ["GoldenGate","Oracle"]
url: goldengate-vmemory-use.html
date: 2019-04-20
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---



#### **Introduction**

GoldenGate is middleware that runs on the OS, so it uses physical memory and virtual memory.

Since GoldenGate replicates only committed transactions, it must hold each transaction's operations in a `managed virtual memory pool` called the *cache* until it receives a commit or rollback for the transaction. Note that we are referring to virtual memory here, not physical memory.

Unless explicitly stated otherwise in this article, the word "memory" refers to virtual memory.

The actual amount of physical memory used by GoldenGate processes is controlled by the operating system.

This article does not cover specifics of memory usage or swap space consumption.

#### **Required Virtual Memory**

The virtual memory estimation formula is documented in the manual as follows:

> https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-B910F3D9-E41C-4335-AC0A-442435481A19.htm
>
> CACHEMGR

```
1. Start one Extract process and one Replicat process.
2. Run GGSCI.
3. View the report file for each running process and look for the PROCESS VM AVAIL FROM OS (min) line.
4. If necessary, round each value up to the next whole number (GB). For example, round 1.76GB up to 2GB.
5. Multiply the rounded Extract value by the number of Extract processes.
6. Multiply the rounded Replicat value by the number of Replicat processes.
7. Add additional swap space required by Oracle GoldenGate processes and other processes on the system to the two results.

(PROCESS_VM x number_Extracts) + (PROCESS_VM x number_Replicats) + (swap_for_other_processes) = max_swap_space_on_system

This total represents the maximum swap space required for these processes. The actual amount of physical memory used by all Oracle GoldenGate processes is controlled by the operating system, not by Oracle GoldenGate. The global cache size is controlled by the CACHESIZE option of CACHEMGR.
```

#### **Virtual Memory Behavior**

The following are memory statistics output to the report file when a process starts:

```
CACHEMGR virtual memory values (may have been adjusted)
CACHEPAGEOUTSIZE (default):               4M
PROCESS VM AVAIL FROM OS (min):           2G
CACHESIZEMAX (strict force to disk):   1.74G
```

To set a virtual memory upper limit, configure the CACHESIZE parameter. This represents a soft limit on virtual memory that the process can use to cache transaction data. It is dynamically determined based on the PROCESS VM AVAIL FROM OS (min) value and can be controlled using the CACHESIZE option of CACHEMGR. Since it is a soft limit, some transactions may use more memory than this size. In that case, the hard upper limit is `CACHESIZEMAX` as shown in the statistics above.

PROCESS VM AVAIL FROM OS (min) indicates the approximate amount of virtual memory this process considers available. For internal reasons, this amount may be less than what the operating system reports as available.

CACHESIZEMAX (strict force to disk) is derived from PROCESS VM AVAIL FROM OS and CACHESIZE. Normally, only transactions whose virtual memory buffer currently exceeds a specific internal value are candidates for paging. When the total memory request exceeds the CACHESIZE value, the cache manager looks for transactions to write to disk and selects transactions from the list of paging candidates. If paging candidate transactions have already been paged to disk and the virtual memory in use exceeds CACHESIZEMAX (strict force to disk), all transactions that need additional buffers can become paging candidates. In this way, virtual memory availability is always ensured.

When memory usage exceeds the limit, transaction data is swapped to the `dirtmp` subdirectory of the GoldenGate installation directory.

When long transactions run, depending on the configured CACHESIZE, there is a high likelihood of swapping to disk, so disk capacity should also be monitored.

#### **About SEND EXTRACT <Capture Name>, CACHEMGR CACHESTATS**

To check virtual memory usage, run the following command:

A lot of information is output, but you can check the memory behavior by looking at the "CACHE OBJECT MANAGER statistics" section. Information about file caching can be found in "CACHE File Caching".

```
GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 40> SEND EXTRACT c11, CACHEMGR CACHESTATS

Sending CACHEMGR request to EXTRACT C11 ...

CACHE OBJECT MANAGER statistics

CACHE MANAGER VM USAGE
vm current     =      0    vm anon queues =      0
vm anon in use =      0    vm file        =      0
vm used max    =   1.27G   ==> CACHE BALANCED

CACHE CONFIGURATION
cache size            =   1G   cache force paging = 1.74G
buffer min            =  64K   buffer max (soft)  =   4M
pageout eligible size =   4M

================================================================================
RUNTIME STATS FOR SUPERPOOL

CACHE Transaction Stats
trans active    =      0    max concurrent =    238
non-zero total  =      1    trans total    =  42.58K

CACHE File Caching
filecache rqsts        =    129    bytes to disk      =   8.20G
file retrieves         =   2.08K   objs filecached    =      1
queue entries          =    129    queue processed    =    130
queue entry not needed =      0    queue not signaled =      0
fc requesting obj      =      0

CACHE MANAGEMENT
buffer links   =   2.06K  anon gets   =      0
forced unmaps  =     39   cnnbl try   =    200
cached out     =    114

```

If you suspect more virtual memory is being used than expected, it is best to check `CACHE MANAGER VM USAGE` first.

```
CACHE MANAGER VM USAGE
vm current = 1015M vm anon queues = 320M
vm anon in use = 692M vm file = 3M
vm used max = 1G ==> CACHE BALANCED
```

##### **Field Descriptions**

- vm current: Total virtual memory size currently allocated (memory + paging)
- vm anon queues: Free memory size within vm current (memory that is no longer in use, temporarily held in a queue as free memory)
- vm anon in use: Total virtual memory size currently in use by processing
- vm file: Size currently being paged
- vm used max: Maximum total virtual memory size used so far
