# Insight_Project
'PROFESSIONAL NETWORK ANALYSIS TO FIND BEST PATHWAYS INTRODUCTION'

## Description:
- **demo** : Include the code to launch the dashboard in streamlit, and input data files
- **test** : This include the scripts 'create_network_structure.py' and a helper utility, 'functions.py'. The scripts reads the raw inital data files by the client, and format it into files suitable for networkX analysis. The raw input files are not added to repository because of privacy, but the scripts can expain the steps used to create the structured data. This folder also include a script 'hide_identities.py', to anonymized the identities. The resultant files are then written to 'demo' directory 
- **analysis** : This has the jupyter notebook with EDA plots and methodolgy used for predictions and inference 
- **static** : This includes images or content to include in the README or web framework if part of the pipeline

## Setup
Clone repository and update python path
```
repo_name=Insight_Project 
git clone https://github.com/skhalil/$repo_name
cd $repo_name
echo "export $repo_name=${PWD}" >> ~/.bash_profile
echo "export PYTHONPATH=$repo_name/src:${PYTHONPATH}" >> ~/.bash_profile
source ~/.bash_profile
```
Optional:
Create new development branch for test development
```
git checkout -b dev-20200605 #Its good idea to add time stamp
```

## Add Remote
```
git remote add origin https://github.com/skhalil/$repo_name
```

## Verify the remote
```
git remote -v  
> origin	https://github.com/skhalil/Insight_Project (fetch)
> origin	https://github.com/skhalil/Insight_Project (push)
```

## To Commit
```
cd $repo_name
git status
git add <DIR/FILE>
git commit -m <"comment">
git push origin <branch_name>
```

## Requisites

- List all packages and software needed to build the environment
- This could include cloud command line tools (i.e. gsutil), package managers (i.e. conda), etc.

#### Dependencies

- [Streamlit](streamlit.io)

#### Installation
To install the package above, pleae run:
```shell
pip install -r requiremnts
```

## Build Environment
- Include instructions of how to launch scripts in the build subfolder
- Build scripts can include shell scripts or python setup.py files
- The purpose of these scripts is to build a standalone environment, for running the code in this repository
- The environment can be for local use, or for use in a cloud environment
- If using for a cloud environment, commands could include CLI tools from a cloud provider (i.e. gsutil from Google Cloud Platform)
```
# Example

# Step 1
# Step 2
```

## Configs
- We recommond using either .yaml or .txt for your config files, not .json
- **DO NOT STORE CREDENTIALS IN THE CONFIG DIRECTORY!!**
- If credentials are needed, use environment variables or HashiCorp's [Vault](https://www.vaultproject.io/)


## Test
- Include instructions for how to run all tests after the software is installed
```
# Example

# Step 1
# Step 2
```

## Run Inference
- Include instructions on how to run inference
- i.e. image classification on a single image for a CNN deep learning project
```
# Example

# Step 1
# Step 2
```

## Build Model
- Include instructions of how to build the model
- This can be done either locally or on the cloud
```
# Example

# Step 1
# Step 2
```

## Serve Model
- Include instructions of how to set up a REST or RPC endpoint
- This is for running remote inference via a custom model
```
# Example

# Step 1
# Step 2
```

## Analysis
- Include some form of EDA (exploratory data analysis)
- And/or include benchmarking of the model and results
```
# Example

# Step 1
# Step 2
```
