# Benchmarking CP2K on Piz Daint

A small guide on how to get the data needed for a production proposal ... 

## Objectives

* Analyze performance and scaling of CP2K (PBE) on Piz Daint hybrid nodes

* Setup and test AiiDA on Piz Daint

* Run optimizations for different systems systems to estimate resource requirements


## How to run

* In any case, run the tests maybe first on a EPFL cluster and then on Daint to be sure that the tests themselves work
  
### Structures

* The structures we selected for the benchmark are disorder free, clean and known to converge and come from the [Curated MOFs](https://github.com/danieleongari/CURATED-MOFs).

| CSD Refcode | name      | metal | # atoms | cell volume |
| ----------- | --------- | ----- | ------- | ----------- |
| NAVJAW      | Co-MOF-74 | Co    | 53      | 1322        |
| KISXIU      | UMCM-1    | Zn    | 510     | 26121       |
| UTEWOG      | Ni3(BTP)2 | Ni    | 252     | 6382        |

* For the benchmark, use converged structures to estimate the timings of one SCF cycle
* You can get data on how many SCF cycles are needed on average by other means (e.g. take an average over the last relaxations you did for different system sizes)

113428
113422
113436

### Setting up AiiDA 

* To set up the CP2K code and computer use the instructions in the [aiida-codes](https://github.com/kjappelbaum/aiida-codes/tree/aiida-1) repository
  > ⚠️ **Warning**: You need to set up the ssh proxy if you run `verdi computer configure`. It also [seems](https://github.com/aiidateam/aiida-core/issues/1853) that it can be useful to set a longer `connection timeout`

* For timings, you want to submit the jobs using `/user/bin/time  -p srun -n <total number MPI tasks> -N <number MPI tasks per node> -d <number of openMP threads> <executable>`

### Running the single-point scaling test

* $\mathrm{speedup}_n = \frac{t_0}{t_n}$, with $t_0$ being the reference time and $t_n$ being the time on $n$ nodes.

* $\mathrm{efficiency} = \frac{\mathrm{speedup}_n}{n}$. Codes with $\mathrm{efficiency} > 0.5$ are scalable. 

### Producing the technical report

* Select the most parallel efficient job size (ratio of benchmark speed-up vs. linear speed-up above 50%) to run the performance analysis, on the basis of your scaling data.  

Here, you need to use a specific modulefile

```
module load daint-gpu
module load perftools-lite/7.0.2
module use /apps/daint/UES/6.0.UP07/craypat/easybuild/modules/all
module load CP2K/6.1-CrayGNU-18.08-cuda-9.1-pat-7.0.2
```


### Running the optimization tests

* To test both the AiiDA interaction with Piz Daint and the optimization performance, we submit the `mulitstep_workchain` from D. Ongari 

> ⚠️ **Warning**: CrayPAT adds an overhead to the wall time, therefore you cannot use that timing to justify your request


## Resources

* [Webinar on how to collect the performance data for proposal submission, CSCS, 2015](https://www.youtube.com/watch?v=m3cesC3DsUM).

* [Webinar Slides on Proposal Submission, CSCS, 2015.](https://www.cscs.ch/fileadmin/user_upload/contents_userLab/Webinar-CSCS_Proposal-12_03_2015.pdf)

* [Technical report, CSCS.](https://user.cscs.ch/access/report/)

* [Example Technical Report, CSCS.](https://user.cscs.ch/access/report/example/)

* [General notes about strong and weak scaling](https://www.kth.se/blogs/pdc/2018/11/scalability-strong-and-weak-scaling/)
