# Statistical Data Analysis Automation

This project serves as a proof of concept for statistical data analysis automatization. The project uses Python and
GoodData.CN Community Edition (CE). To understand what this project is about please first
read [this short article](https://medium.com/gooddata-developers/how-to-automate-your-statistical-data-analysis-852f1a463b95)
.

## Installation and Usage

### 1. Install and Run GoodData.CN CE

If you don't already have an instance of GoodData.CN up and running on your system.

**Follow these steps:**

1. Run the [GoodData.CN CE docker image](https://www.gooddata.com/developers/cloud-native-community-edition/) using the following command:
    ```bash
    docker run -d -i -t -e LICENSE_AND_PRIVACY_POLICY_ACCEPTED=YES -p 3000:3000 -p 5432:5432 -v gd-volume:/data gooddata/gooddata-cn-ce:2.1
    ```

   After few minutes your GoodData.CN CE will be ready.

2. Access your GoodData.CN deployment using your internet browser. The URL is http://localhost:3000, where you should see the login page.

3. Log in using the following credentials:

    * Email Address = demo@example.com
    * Password = demo123
    * Token (for REST APIs or Python SDK) = YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz

For more information you may check out [docker hub](https://hub.docker.com/r/gooddata/gooddata-cn-ce).

### 2. Prepare Your Python Environment

We recommend you prepare a virtual environment and install all requirements there. If you want to use your existing
Python requirement, feel free to skip to Step 3.

**Follow these steps:**

1. Create Python virtual environment:

    ```bash
    python -m venv .venv
    ```

2. Activate the Python virtual environment:

    ```bash
    source .venv/bin/activate
    ```

3. Install Python requirements:

    ```bash
    python -m pip install -r requirements.txt
    ```

### 3. Get Started

If you're new to GoodData.CN, we recommend you take a look at some videos
on [GoodData Developers YouTube channel](https://www.youtube.com/channel/UCEfUBavHP9pjvSB_T2RtE6w), have quick run
through the [GoodData University GoodData.CN](https://university.gooddata.com/first-steps-with-gooddatacn) course, or
just explore it on your own. :)

For checking proof of concept run the `main.py` script:

```bash
python main.py
```

Please note that receiving data from GoodData.CN CE and checking assumptions may take some time.

For example on MacBook Pro (14-inch, 2021) with Python 3.10.8

| CPU | Apple M1 Pro |
|-----|--------------|
| RAM | 32 GB        |

It took us 1 minute 5 seconds. :)
