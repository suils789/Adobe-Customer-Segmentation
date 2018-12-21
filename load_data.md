# Load Data

There is better way to do data loading.
But the way team2 and I attempt is to download the data locally (about 6GB) first and read in.
Just an illustration.

### Preparation:
1. install AWS CLI 

    + https://docs.aws.amazon.com/cli/latest/userguide/installing.html
    + check if it is installed by `aws --version`
2. pip install in your virtual env:
    + boto3 (AWS python API) it's not necessary for loading data here
    + fastparquet 
    make sure you install `cython` and `numba` beforehand :) I got stuck here
    then
    `pip install --upgrade --no-deps --force-reinstall git+https://github.com/dask/fastparquet`
    + brew install snappy
    
    `$ brew install snappy # snappy library from Google
$ CPPFLAGS="-I/usr/local/include -L/usr/local/lib" pip install python-snappy`


### I. set up AWS with access keys
+ you can set up your access keys and secret key interactively by the commmand `aws configure` [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
Or you can create a file in your directory `~/.aws/config` like mine
I am setting the keys as default here.

```{sh}
[default]
aws_access_key_id = AKIAJVG3LIRFYPDZXSHQ
aws_secret_access_key = xTia3YD3F0W0ROQ949mmpHOS2vK5Gb5u4uvfdojZ
region = us-east-1
```
region is optinal to fill in.
Refer to https://docs.aws.amazon.com/cli/latest/topic/config-vars.html.


### II. download the data
+ after setting the configuration, you should be able to access all the files in bucket and copy them all to local (again, you don't have to download all of them if you don't have enough space)
+ `aws s3 cp --recursive s3://adobe-columbia-capstone-2018/ /adobe`
will download the files into current_directory/adobe
+ refer to https://docs.aws.amazon.com/cli/latest/reference/s3/index.html

### III. load data in ipynb
```{python}
from fastparquet import ParquetFile
import pandas as pd
file_path = "your_path_to/adobe/data/part-00000-52f7d874-6802-44d3-a352-0436cead1733-c000.snappy.parquet"
df = pd.read_parquet(file_path, engine="fastparquet")
```