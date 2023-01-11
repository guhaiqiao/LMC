# Replication Package for 'Self-Admitted Library Migrations in Java, JavaScript, and Python Packaging Ecosystems: A Comparative Study'

This is the replication package for our SANER 2023 paper *Self-Admitted Library Migrations in Java, JavaScript, and Python Packaging Ecosystems: A Comparative Study*. It can be used to replicate all four research questions in the paper using our preprocessed and manually labeled data. The replication package have been permanently archived at XXXX.

## Introduction

Reusing open-source software libraries has become the norm in modern software development, but libraries can fail due to various reasons, e.g., security vulnerabilities, lacking features, and end of maintenance.
In some cases, developers need to replace a library with another competent library with similar functionalities, i.e., *library migration*.
Previous studies have leveraged library migrations as a unique lens of observation to reveal insights into library selection and dependency management in general. However, they are heavily biased toward Java while the generalizability of their findings remains unknown.

We aim to empirically investigate the prevalence, domains, rationals and directionality of self-admitted library migrations(SALMs) in Java/Maven, Python/PyPI, and JavaScript/npm, that explain *how* and *why* SALMs occur and well serve the comparison.
We attempt to prove that SALMs are indeed universal (i.e., not unique to Java/Maven) and demonstrate some sort of common patterns (e.g., unidirectionality); the rationales can also help the establishment of best practices for library selection and migration.

More specifically, we ask the following research questions:

- **RQ1:** How common are SALMs in Java/Maven, JavaScript/npm, and Python/PyPI? How do the longitudinal trends differ in the three ecosystems? 
- **RQ2:** In what library domains do SALMs happen? How do the domains differ in the three ecosystems?
- **RQ3:** What are the rationales for SALMs? How do the rationales differ in the three ecosystems?
- **RQ4:** Are SALMs unidirectional? How does the directionality differ in the three ecosystems?

To answer the research questions, we proposed a semi-automatic method that can accurately locate SALM commits and their rationales from git repositories, and conduct manual labelling, data analysis and visualization to generate the presented results. We implement all automated processing using Python in an Anaconda environment and we conduct all manual labelling using Microsoft Excel. We hope the scripts and dataset in this replication package can be useful to further studies in library migration and other related fields.

## Replication Package Setup
```shell script
conda create -n SALMC python=3.8
conda activate SALMC
python -m pip install -r requirements.txt
conda install -n SALMC ipykernel --update-deps --force-reinstall
```

Then, activate the SALMC environment and run `jupyter lab` in the repository folder for replication.

## Replicating Results
After the replication package is setup, you should have a Jupyter Lab server instance running at http://localhost:8888. In Jupyter Lab, you should see the whole git repository folder, in which there are four notebooks: rq1_prevalance.ipynb, rq2_domain.ipynb, rq3_rationale.ipynb, and rq4_directionality.ipynb. They correspond to the four RQs in our paper. You can directly see the plots and numbers used in our paper in the cells' output. For each notebook, you can start a Python kernel and run all cells, and then you should be able to replicate all the results in this notebook. The results should look identical or similar to the plots in the paper if it is working properly.


## Migration Dataset
Our migration dataset is in the migration folder, where each file is named as `{language}_migration.csv` or `{language}_migration_group.csv`, corresponding to the ungrouped dataset and grouped dataset in three ecosystems. 
For each .csv file, it contains 10 columns, 
`repo_name,commit_sha,time_stamp,add_lib,rem_lib,commit_message,pattern,possible_reason,num,domain`.

|name|meaning|
|---|---|
|repo_name| The git repo where migrations happen.|
|commit_sha| The commit sha of migrations.|
|time_stamp| The time when migrations happen.|
|add_lib| The library added in migrations.|
|rem_lib| The library removed in migrations.|
|commit_message| The commit message of the migration commits.|
|pattern| `<add_lib rem_lib>`, different from migration rules `<l1, l2>`.|
|possible_reason| The sentences that possibly contains information about migration in commit message.|
|num| The number of times migration occurs in our dataset.|
|domain| The labeled domain of migration rules|

 Our manual labelled reasons are in the reason folder, where each file is named as `{language}_reason.csv`.
 For each .csv file, it contains 5 columns, `repo_name,time_stamp,pattern,reason_type,group_reason`

|name|meaning|
|---|---|
|repo_name| The git repo where migrations happen.|
|time_stamp| The time when migrations happen.|
|pattern| `<add_lib rem_lib>`, different from migration rules `<l1, l2>`.|
|reason_type| The type of reason mentioned in commit message. Refer to `rq3_raionale.ipynb` for the corresponding relationship between the number and the specific reason.|
|group_reason| Three themes of reason: source library, target library and project specific.|