# SERVIER_PYTHON_TEST_PROJECT - Documentation
This project provides a solution for Servier’s data engineering technical test. The main objective is to analyze journal data to identify drug mentions within PubMed articles and clinical trial studies. The project is structured with multiple Python modules, configuration files, and testing scripts.

# TABLE OF CONTENTS
 ### PART I. DATA PIPELINE 
- Project Hypotheses
- Configuration and Prerequisites
- Installation and Packaging
- Commands
- Unit Testing
- Production Pipeline Adaptation (Docker, CI/CD, Airflow Composer)
- Execution for Big Data

### PART II. SQL 
- SQl queries



# PART I. DATA PIPELINE 

## Project Hypotheses
- Only articles mentioning a drug in the title are analyzed. Articles without drug mentions are excluded.
- Each drug mention is associated with a unique instance.
- Input data is provided in .csv and .json formats.
- The project can handle multiple input files and process corrupted JSON files if needed.

## Configuration and Prerequisites

- Python >= 3.8: Ensure Python is installed and is of a compatible version.
- Python Dependencies: Use the requirements.txt file or activate the included venv environment to load necessary modules.


## Installation and Packaging

Install Dependencies:
```bash
pip install -r requirements.txt
```
## Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  
```
## Commands
The following commands are available to run the main scripts:

Run Main Script:
```bash
python main.py
```
## List Available Commands:
Use the --help argument to see available options:

```bash
python main.py --help
```

## Unit Testing
Run All Tests:
bash
```bash
pytest tests/
```
Run a Specific Test:
```bash
pytest tests/test_clean.py
```

## Production Pipeline Adaptation
The pipeline can be configured for production with the following adjustments:
Environment Variables: Use environment-specific .env files (e.g., .env_dev, .env_prod).

### A -  Docker Image
1. Docker Image Setup
To ensure a consistent and isolated environment, build and run the project using Docker. Follow the steps below to create and run the Docker image:

   - Steps to Build and Run Docker Image:
Build the Docker Image:

   - From the root directory of the project, run:
```bash
docker build -t servier_project_image .
```
2. Run the Docker Container:

Once the image is built, you can run it with:
```bash
docker run --rm -it servier_project_image

```
3. Access Docker Shell (Optional):

For troubleshooting or running individual commands inside the container, you can access the container's shell:

```bash
docker run -it servier_project_image /bin/
```

4. Environment Variables:

Ensure any required environment variables.

### B - CI/CD Integration: 

Set up a CI/CD pipeline for automated deployments to ensure smooth, consistent updates across environments.
CI/CD 

Setup Steps:

 Step1 : Choose a CI/CD Tool: Use a tool such as Jenkins, GitLab CI/CD, or GitHub Actions.
For our case I initiated a GitLab file as quick sample.

Step2 : Configure Staging and Production   Branches:
  - Define branches in your version control system to separate environments, for example:
     - main or master branch for production.
     - develop branch for development and testing.
- Define CI/CD Pipeline Stages:
   - Build: Configure pipeline to build or  test the code in each stage.
   - Test: Run automated tests to verify each build.
   - Deploy: Set up deployment jobs to automatically deploy to the correct environment when the code is merged into the relevant branch.

- Environment-Specific Deployments:
  - Configure each stage to load the corresponding .env file, ensuring that environment-specific settings are applied.
- Automated Testing and Linting: Include steps to run linting, unit tests, and integration tests for code quality checks.
- Automated Notifications: Set up notifications (e.g., via email or Slack) for deployment status updates.

### C - Orchestration :

Orchestration with Cloud Composer
To manage and schedule the execution of this pipeline in production, Google Cloud Composer (built on Apache Airflow) is used for orchestration.

- Cloud Composer Integration Steps:

1.  Define the DAG (Directed Acyclic Graph):

  - Create a DAG file in Airflow to define the pipeline tasks.
  - Each task (e.g., data extraction, transformation) is represented as a Python function or script to be called with Airflow operators (PythonOperator, BashOperator).

  2.  Environment Setup:

   - In Google Cloud Console, create a Cloud Composer environment with the required resources and configurations (e.g., machine type, disk space).

  3. Upload DAG File:

  - Place the DAG file in the Cloud Composer dags/ folder to activate it.

  4. Environment Variables:

   - Set environment variables within the Cloud Composer environment for each pipeline stage (e.g., API_KEY, DB_CONNECTION_STRING).

 5. Trigger and Monitor DAG:

  - Use the Airflow UI to trigger the DAG manually or set up a schedule for periodic execution.

  - Monitor task progress, check logs, and troubleshoot any issues directly from the Airflow UI.

# Execution for Big Data
To handle larger data volumes, the project can be scaled for Big Data using PySpark or by loading data into BigQuery for distributed SQL analysis.


# PART II.  SQL 

- Before we start, here is a list of hypothesis that I infered before solving the problems :
    - The tables are inside a dataset called `test_servier`
    - We will be using BigQuery's SQL notation
    - Since we are using BigQuery, then we assuume that the date will automatically be fixed and converted to %Y-%m-%d instead of %d/%m/%Y, so no need to use `FORMAT_DATE()` or `PARSE_DATE()` functions

- Query 1 : Daily sales between January 1st 2019 and December 31st 2019 
```sql
SELECT
    date AS date,
    SUM(prod_price * prod_qty) AS ventes
FROM
    `test_sevrier.TRANSACTIONS`
WHERE
    date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
    date
ORDER BY
    date ASC
```


- Query 2 : Decoration and Furniture sales by client, between January 1st 2019 and December 31st 2019 
```sql
SELECT
    t.client_id AS client_id,
    SUM(
        CASE
            WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty
            ELSE 0
        END
    ) AS ventes_meuble,
    SUM(
        CASE
            WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty
            ELSE 0
        END
    ) AS ventes_deco
FROM
    `test_sevrier.TRANSACTIONS` AS t
LEFT JOIN `test_sevrier.PRODUCT_NOMENCLATURE` AS pn ON t.prod_id = pn.product_id
WHERE
    t.date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
    client_id
```