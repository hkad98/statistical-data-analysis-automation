# Automate Your Statistical Data Analysis

This project is proof of concept for statistical data analysis aromatization.
This proof of concept uses Python and GoodData.CN CE. For more information about this project check out this article.

## Set up

### Run GoodData.CN CE

To run GoodData.CN CE you need to run following command.

```bash
docker run -i -t -p 3000:3000 -p 5432:5432 -v gd-volume:/data gooddata/gooddata-cn-ce:latest
```

After few minutes your GoodData.CN CE will be ready. You can check http://localhost:3000, where you should see login page. Credentials are:
* Email Address = demo@example.com
* Password = demo123
* Token (for REST APIs or Python SDK) = YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz

For more information check out [docker hub](https://hub.docker.com/r/gooddata/gooddata-cn-ce).


### Get Python environment ready
First of all, I recommend to create virtual environment and install all requirements there, but if you want to install libraries in your global environment it's up to you.

```bash
# create python virtual environment
python3 -m venv poc
```

```bash
# activate python environment
source poc/bin/activate
```

```bash
# install python requirements
python3 -m pip install -r requirements.txt
```

## Let's start

First, you can explore GoodData.CN CE. I recommend taking a look at some videos on [GoodData Developers YouTube channel](https://www.youtube.com/channel/UCEfUBavHP9pjvSB_T2RtE6w), or you can have a look at [GoodData University](https://university.gooddata.com/), or you can explore by your own :) 

For checking proof of concept run main.py script.
```bash
python3 main.py
```
Receiving data from GoodData.CN CE and checking assumptions take some time.

On MacBook Pro (13-inch, 2020)

| CPU | 2 GHz Quad-Core Intel Core i5 |
|-----|-------------------------------|
| RAM | 16 GB 3733 MHz LPDDR4X        |

It took 2 minutes 20 seconds.

