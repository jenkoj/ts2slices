# Time Series Slicer for Energy Data

The script is a fork from [ts2img](https://github.com/jenkoj/ts2img).
The slicing of time series was a bi-product of the trasfomation, so
this scipt utilizes only the latter part. 

Many parameters remain so that they dont break the script due to filenames.
Simply igonore those.
Imporatant parameters will be marked.

For easier data handling [NILMTK](https://github.com/nilmtk/nilmtk) was used. 

environment 

Works with all datasets supported by NILMTK. Tested on:

* REFIT
* UKDALE
* iAWE
* REDD
* ECO   

# Install Instructions  
  
❗️ If possible, install on a Linux machine.

1.  Install [Anaconda](https://anaconda.org) by following instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

2.  Clone this repository and change directory to conda:
  
    ```bash
        git clone https://github.com/jenkoj/ts2img && cd ts2img/conda
    ```

3.  Create a new environment by running:

    ```bash
        conda env create --name ts2img --file=ts2img.yml 
    ```
4.  Activate the newly created environment:

    ```bash
        conda activate ts2img
    ```

5.  Get hold of a dataset converted to NILMTK format or convert your dataset.

    * Check if your dataset has supported converter [link](https://github.com/nilmtk/nilmtk/blob/master/docs/source/nilmtk.dataset_converters.rst), if not you can write your own dataset converter by following instructions [here](https://github.com/nilmtk/nilmtk/blob/master/docs/manual/development_guide/writing_a_dataset_converter.md).

    * Convert your dataset by following notebook [here](https://github.com/nilmtk/nilmtk/blob/master/docs/manual/user_guide/data.ipynb).

6.  Place converted dataset in datasets directory.

7.  Set parameters.

8.  Finally, run:
    ```bash
        ipython -c "%run converter.ipynb"
    ```
When adjusting the parameters start with iAWE. Since it is small, it is easy to handle. 

