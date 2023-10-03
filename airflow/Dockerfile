FROM apache/airflow:2.7.1

# Install playwright: required with root user
USER root
RUN apt update 
RUN python3 -m pip install playwright
RUN python3 -m playwright install --with-deps

# Change to user default: airflow and install library requirement
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
RUN playwright install