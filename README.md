# Insight_Project
'PROFESSIONAL NETWORK ANALYSIS TO FIND BEST PATHWAYS INTRODUCTION'

## Description:
- **launch_demo.py** : A dashboard in streamlit with input data files (*.csv)
- **test** : This include the scripts 'create_network_structure.py' and a helper utility, 'functions.py'. The scripts reads the raw inital data files by the client, and format it into files suitable for networkX analysis. The raw input files are not added to repository because of privacy, but the scripts can expain the steps used to create the structured data. This folder also include a script 'hide_identities.py', to anonymized the identities. The resultant files are then written to 'demo' directory 
- **analysis** : This has the jupyter notebook with EDA plots and methodolgy used for predictions and inference 
- **static** : This includes images or content to include in the README or web framework if part of the pipeline

## Setup
Clone repository and update python path
``` 
git clone https://github.com/skhalil/Insight_Project
cd Insight_Project
echo "export Insight_Project=${PWD}" >> ~/.bash_profile
echo "export PYTHONPATH=Insight_Project/src:${PYTHONPATH}" >> ~/.bash_profile
source ~/.bash_profile
```

## Run the App Locally
From the git root directory, run the following
```
streamlit run launch_demo.py

> You can now view your Streamlit app in your browser.
> Local URL: http://localhost:8501
> Network URL: http://192.168.1.172:8501
>
```

## Instructions for Dashbaord User
- Please choose the file `anonymous_nodes.csv` for the node file select tab, and `anonymous_edges.csv` for the edges file seelct tab. Otherwise, it will give an error (Need to fix). 


## Development
<details><summary>CLICK ME</summary>
<p>

Optional:
Create new development branch for test development
```
git checkout -b <branch_name>
```

### Add Remote and Verify it!
```
git remote add origin https://github.com/skhalil/Insight_Project
git remote -v  
> origin	https://github.com/skhalil/Insight_Project (fetch)
> origin	https://github.com/skhalil/Insight_Project (push)
```

### Commit
```
cd Insight_Project
git status
git add <DIR/FILE>
git commit -m <"comment">
git push origin <branch_name>
```
### Merge to master (In case you develop on another branch)
```
git branch
> master
> * test_Jun18

git checkout master
git branch
> * master
> test_Jun18

git merge test_Jun18
```
</p>
</details>

## Pre-requisites before lauching to Server

<details><summary>CLICK ME</summary>
<p>
- List all packages and software needed to build the environment

### Dependencies
- Use `pipreqs` to fetch the dependencies `requirements.txt`, rather than adding manually.
```
pip install pipreqs
cd ../
> /Users/skhalil/Desktop/Analysis/DataCleaningRebel
pipreqs Insight_Project
```
The file looks like as
```
Faker==4.1.0
matplotlib==3.1.1
numpy==1.16.4
pandas==0.23.4
networkx==2.4
streamlit==0.60.0
```
### Build Environment
- Build scripts can include shell scripts or python `setup.py` files
```
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```
- In case if you like to deploy with Heroku, here is another requirement. Create a file called Procfile and commit all to yout github repo
```
web: sh setup.sh && streamlit run launch_demo.py
```
</p>
</details>


## Delployment with AWS

<details><summary>CLICK ME</summary>
<p>

A good set of instructions can be found[here](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3)


### Setup the basic environment
- Once you login to your remote AWS instance, prepare the environment by installing miniconda and any dependencies
```
sudo apt-get update
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.shbash 
~/miniconda.sh -b -p ~/miniconda
echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc
source ~/.bashrc
```
### Clone your github repo, and install any other dependencies

```
git clone https://github.com/skhalil/Insight_Project
cd Insight_Project
pip install -r requirements.txt 
pip install scipy # some how this was not caught in requirements.txt
```
### Lauch the app 
```
streamlit run launch_demo.py
> You can now view your Streamlit app in your browser.

> Network URL: http://172.31.6.90:8501
> External URL: http://34.208.240.95:8501
>
```
At this point, the script `launch_demo.py` should be running on external url.

### Run the session in background
- In order to keep running the session in background, even when you logged off, install TMUX
- Stop the app `Ctrl+C` and install TMUX
```
tmux attach -t StreamSession
```
- Start a new tmux session
```
tmux new -s StreamSession
streamlit run launch_demo.py
```
- To leave the shell

`Ctrl+B` and then `D`

- To reattach to same session
```
tmux attach -t StreamSession
```

### Install nginx

```
ubuntu@ip-172-31-6-90:~/Insight_Project$ cd ..
ubuntu@ip-172-31-6-90:~$ ls -rlt
total 86796
-rw-rw-r--  1 ubuntu ubuntu 88867207 Jun 16 20:05 miniconda.sh
drwxrwxr-x 15 ubuntu ubuntu     4096 Jun 21 17:52 miniconda
drwxrwxr-x  6 ubuntu ubuntu     4096 Jun 21 18:08 Insight_Project


ubuntu@ip-172-31-6-90:~$ sudo apt-get install nginx
ubuntu@ip-172-31-6-90:~$ ls /etc/nginx/sites-enabled/default 
> /etc/nginx/sites-enabled/default
ubuntu@ip-172-31-6-90:~$ sudo rm /etc/nginx/sites-enabled/default
ubuntu@ip-172-31-6-90:~$ sudo vi /etc/nginx/sites-available/flask-project.conf
ubuntu@ip-172-31-6-90:~$ sudo ln -s /etc/nginx/sites-available/flask-project.conf /etc/nginx/sites-enabled/
ubuntu@ip-172-31-6-90:~$ ls /etc/nginx/sites-enabled/
> flask-project.conf
ubuntu@ip-172-31-6-90:~$ sudo systemctl stop  nginx
ubuntu@ip-172-31-6-90:~$ sudo systemctl start  nginx
ubuntu@ip-172-31-6-90:~$ sudo systemctl enable nginx
Synchronizing state of nginx.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable nginx
ubuntu@ip-172-31-6-90:~$ curl http://localhost
> <!doctype html><html l....</html>ubuntu@ip-172-31-6-90:~$ 
```
- The file `/etc/nginx/sites-enabled/flask-project.conf` looks like
```
server {
listen 80;
listen [::]:80;

location / {
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header Host              $http_host;
#proxy_pass http://localhost:8501;
proxy_pass http://127.0.0.1:8501/;
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_read_timeout 86400;
}
}

```

### Run with your domain
- We like to map the external url to a domain such as `www.DataScienceClub.me`


#### Map the ip address with your domain
- Read the instructions.
![DataScienceClub.me](/images/NameCheap_AdvancedDNS.png)
Instructions: ![namecheap](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain)



#### Trouble Shooting
- In case you can't lauch your app in browser, make sure port `8051` (in my case) is available. If another session is already in progress, then kill it (`kill -9 <JOB_NUMBER>`).
```
ps aux | grep streamlit
```

- Check the log files
```
sudo cat /var/log/nginx/access.log

> 99.109.56.32 - - [21/Jun/2020:18:43:22 +0000] "GET /healthz HTTP/1.1" 304 0 "http://34.208.240.95/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:77.0) Gecko/20100101 Firefox/77.0"
```
At this point, check (Network & Security) in your aws account

- Check the error
```
sudo cat /var/log/nginx/error.log

> 2020/06/21 18:41:33 [error] 14373#14373: *8 connect() failed (111: Connection refused) while connecting to upstream, client: 99.109.56.32, server: , request: "GET /healthz HTTP/1.1", upstream: "http://127.0.0.1:8501/healthz", host: "34.208.240.95", referrer: "http://34.208.240.95/"
```
- Go to the main project directory and create `config.toml` file
```
source setup.sh
ls ~/.streamlit/config.toml
vi ~/.streamlit/config.toml
```
```
[server]
headless = true
enableCORS=false
port = 8501
```
- Check again the nginx settings, which happened to be the cause in my case

</p>
</details>

## Delployment with Heroku

<details><summary>CLICK ME</summary>
<p>

- Start with the following blogs:

-1- https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku

-2- https://towardsdatascience.com/from-streamlit-to-heroku-62a655b7319

-3- https://medium.com/@gitaumoses4/deploying-a-flask-application-on-heroku-e509e5c76524

-4- https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3


### Virtual Env
In your conda enviroment or base, first make sure python3 is up to date, and then lauch the virtual environment
```
python3 -m pip install --upgrade pip
pip3 install virtualenv
which virtualenv
which python3
virtualenv -p /Users/skhalil/miniconda2/envs/python37/bin/python3 venv
source venv/bin/activate
```
### Check if app is working
```
streamlit run launch_demo.py
```

- I have to edit the requirements.txt file as otherwise the app was complaining about `scipy` library. So my `requirements.txt` file looks like
```
pandas==0.23.4
numpy==1.16.4
scipy==1.5.0
streamlit==0.60.0
matplotlib==3.1.1
networkx==2.4
Faker==4.1.0
```

### Login to Heroku and create a new repo in Heroku
```
heroku login
heroku create
> Creating app... done, ⬢ ancient-cove-13711
> https://ancient-cove-13711.herokuapp.com/ | https://git.heroku.com/ancient-cove-13711.git
```
### Add the remote and push everything
```
(venv) (python37) PHSX-CMS:Insight_Project skhalil$ heroku git:remote -a ancient-cove-13711
set git remote heroku to https://git.heroku.com/ancient-cove-13711.git

(venv) (python37) PHSX-CMS:Insight_Project skhalil$ git remote -v
heroku    https://git.heroku.com/ancient-cove-13711.git (fetch)
heroku    https://git.heroku.com/ancient-cove-13711.git (push)
origin    https://github.com/skhalil/Insight_Project (fetch)
origin    https://github.com/skhalil/Insight_Project (push)
(venv) (python37) PHSX-CMS:Insight_Project skhalil$ git add .
(venv) (python37) PHSX-CMS:Insight_Project skhalil$ git commit -m "some message"
(venv) (python37) PHSX-CMS:Insight_Project skhalil$ git push heroku master
> Counting objects: 79, done.
> Delta compression using up to 8 threads.
> Compressing objects: 100% (75/75), done.
> Writing objects: 100% (79/79), 1.12 MiB | 1.07 MiB/s, done.
> Total 79 (delta 28), reused 0 (delta 0)
> remote: Compressing source files... done.
> remote: Building source:

```
### Add the domain
- You need to add your credit card information to activate the Heroku account before adding the domain
```
(venv) (python37) PHSX-CMS:Insight_Project skhalil$ heroku domains:add networkrebel.me 
Configure your app's DNS provider to point to the DNS Target corrugated-aardwolf-me1kf9j8yhfnkprywj785qv4.herokudns.com.
For help, see https://devcenter.heroku.com/articles/custom-domains

The domain networkrebel.me has been enqueued for addition
Run heroku domains:wait 'networkrebel.me' to wait for completion
Adding networkrebel.me to ⬢ ancient-cove-13711... done

(venv) (python37) PHSX-CMS:Insight_Project skhalil$ heroku domains --app ancient-cove-13711
=== ancient-cove-13711 Heroku Domain
ancient-cove-13711.herokuapp.com

=== ancient-cove-13711 Custom Domains
Domain Name     DNS Record Type DNS Target                                                 
networkrebel.me ALIAS or ANAME  corrugated-aardwolf-me1kf9j8yhfnkprywj785qv4.herokudns.com 
```

- Now comes the tough part to map the DNS to target domain on namecheap Advanced DNS settings. After that one should be good to go with the it. Note, this method is very different than from adding the target record for AWS.

-5- https://towardsdatascience.com/how-to-deploy-your-website-to-a-custom-domain-8cb23063c1ff

</p>
</details>











