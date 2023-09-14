# Using the Alembic Library in Python for Managing Database Change History

![Alembic Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvKIRRHbM4rK4Emm1D8USQjzsShFva069qCi6KZP9V4jhjKQXfaN92FYi1K9EMbdWabg&usqp=CAU)

Alembic is a database change history management tool for Python. It allows you to manage database versions, track change history, and easily perform database updates.

## Installation

1. Run the `docker-compose.yml` file to create a local PostgreSQL database.
    ```shell
    docker-compose up -d
    ```

2. Create a Python virtual environment.
    ```shell
    python -m venv .venv
    ```

3. Active .venv
    ```shell
    => Windows: 
    .venv\Scripts\activate
    => Linux: 
    source .venv/bin/activate
    ```

3. Install the required libraries from the `requirements.txt` file.
    ```shell
    pip install -r requirements.txt
    ```

## Usage
1. **Initialize Alembic**:

   Use the following command to initialize Alembic:
   ```shell
   alembic init alembic
   ```
   ***Note***: This is **alembic\alembic** folder in project.

2. **Creating a New Revision**:

   Use the following command to create a new revision:
   ```shell
   alembic revision -m "Description of the revision"
   ```
   This will create a new migration file in the versions directory of Alembic containing database changes.

3. **Checking the Current Version**:

   To check the current database version, use the command:
   ```shell
   alembic current
   ```

4. **Version History**:

   To view the version history, use the command:
   ```shell
   alembic history
   ```

5. **Performing Upgrades and Downgrades**:

   To perform an upgrade to the latest version, use the following command:
   ```shell
   alembic upgrade head
   ```
   To perform a downgrade to an older version, use the following command, replacing {revision} with the desired version number:
   ```shell
   alembic upgrade head
   ```
   ***Note***: 
   
   The first time you run the project, you must run the command <code>alembic upgrade head</code> to migrate the database with all the changes.

   The first time you run the project, you must run the command 'alembic upgrade' to migrate the database with all the changes