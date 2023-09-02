# Using MySQL
To start using MySQL, you'll need to go to the MySQL tab on your dashboard, and set up a password. You'll also find the connection settings (host name, username) on that tab, as well as the ability to create new databases.

You can start a new MySQL console to access your databases from this tab too, or alternatively you can open a MySQL shell with the following command from a bash console or ssh session:

`mysql -u USERNAME -h HOSTNAME -p 'USERNAME$DATABASENAME'`
In this:

The USERNAME is the username you use to log in to PythonAnywhere
The HOSTNAME is on your Databases tab
The 'USERNAME$DATABASENAME' is the full name of your database, which comprises your username, then a dollar sign, then the name you gave it. The single quotes around it are important! If you don't put them in there, bash will try to interpret the $DATABASENAME as an environment variable, which will lead to an error saying ERROR 1044 (42000): Access denied for user 'USERNAME'@'%' to database 'USERNAME'
When you run the command, it will prompt you for a password -- use the one you entered on the Databases tab.

Accessing MySQL from Python

The appropriate libraries are installed for all versions of Python that are supported, so if you're not using a virtualenv, to access a MySQL database just import MySQLdb.

If you are using a virtualenv, you'll need to install the correct package yourself. Start a bash console inside the virtualenv, then:

For Python 3.x

`pip install mysqlclient`

### MySQL with Django
To configure Django to access a MySQL database on PythonAnywhere, you need to do this in your settings file:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<your_username>$<your_database_name>',
        'USER': '<your_username>',
        'PASSWORD': '<your_mysql_password>',
        'HOST': '<your_mysql_hostname>',
    }
}

```
Again, you can get the username and hostname details from the "Databases" tab.

### MySQL with Django tests
When you run Django tests that use the database, Django tries to create a database called `test_<original database name>` and that will fail because Django does not have permissions to create a new database. To run Django tests on PythonAnywhere, add a TEST key to your database definition in settings.py. Like this:

```
DATABASES = {
    'default': {
         ...
        'TEST': {
          'NAME': '<your username>$test_<your database name>',

```
[More info here:](https://docs.djangoproject.com/en/3.2/ref/settings/#test)

We suggest you use a form like `<your username>$test_<your database name>`. Create this database from the PythonAnywhere Databases tab and Django will happily use it and run your tests.

## Accessing your MySQL database from outside PythonAnywhere
There are a number of ways to do this. The first thing to know is the SSH hostname for your account:

If the account is on the global, US-based system at www.pythonanywhere.com, then the SSH hostname is ssh.pythonanywhere.com
If the account is on the EU-based system at eu.pythonanywhere.com, then the SSH hostname is ssh.eu.pythonanywhere.com
Note the difference in hostnames for both SSH and MySQL:

Hostname	
Global-US:	ssh.pythonanywhere.com	username.mysql.pythonanywhere-services.com
EU:	ssh.eu.pythonanywhere.com	username.mysql.eu.pythonanywhere-services.com

SSH	MySQL
Global-US: username.mysql.pythonanywhere-services.com
EU:	username.mysql.eu.pythonanywhere-services.com

### From Django
If running the project on your local machine, and you want it to access your MySQL database, you can install the sshtunnel package (`pip install sshtunnel`)and then use code like this:

1. In the django settings.py create an ssh tunnel before the django DB settings block:
```
from sshtunnel import SSHTunnelForwarder

# connect to a server uisng ssh username and password
server = SSHTunnelForwarder(
    'SERVER_IP',
    ssh_username="SSH_USERNAME",
    ssh_password="SSH_PASSWORD",
    remote_bind_address=('your database hostname', 3306)
)

server.start()

print(server.local_bind_port)  # show assigned local port
# work with `SECRET SERVICE` through `server.local_bind_port`.

```
2. Then add the Database info block in the settings.py. Here I am adding a default local mySQLite DB and the remote MySQL DB that we connect to using the ssh tunnel

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'server_db': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'PORT': server.local_bind_port,
        'NAME': REMOTE_DB_DB_NAME,
        'USER': REMOTE_DB_USERNAME,
        'PASSWORD': REMOTE_DB_PASSWORD,
    },
}
```
3. Executions like make migratations can be made to the remote db using commands like `$ python manage.py migrate --database=server_db` or make calls to the db from within the python code using lines like Models.objects.all().using('shhtunnel_db')


# How to set up environment variables in Django for security
It is important to keep sensitive bits of code like API keys and passwords away from the public.

1. Install Django Environ
In your terminal, inside the project directory, type:

`$ pip install django-environ`

2. Import environ in settings.py
`import environ`

3. Initialise environ
Below your import in settings.py:

```
    #Initialise environment variables
    env = environ.Env()
    environ.Env.read_env()
```

4. Create your .env file
In the same directory as settings.py, create a file called `.env`

5. Declare your environment variables in .env
Make sure you don’t use quotations around strings.

    SECRET_KEY=h^z13$qr_s_wd65@gnj7a=xs7t05$w7q8!x_8zsld#
    DATABASE_NAME=mysql
    DATABASE_USER=bob
    DATABASE_PASS=supersecretpassword

6. IMPORTANT: Add your .env file to .gitignore
If you don’t have a .gitignore file already, create one at the project root. Make sure the name of your .env file is included.

7. Replace all references to your environment variables in settings.py, like so

```
DATABASES = {
‘default’: {
‘ENGINE’: ‘django.db.backends.mysql’,
‘NAME’: env(‘DATABASE_NAME’),
‘USER’: env(‘DATABASE_USERNAME’),
‘PASSWORD’: env(‘DATABASE_PASSWORD’),
}
}
```
And

`SECRET_KEY = env(‘SECRET_KEY’)`

## Migrating the database from SQLite to MySQL
1. Verify database by running `python manage.py dbshell`
2.  Backup data`python manage.py dumpdata > mydb.json `
3.  Create a new database on my pythonanywhere
4. Add my Sql database settings to settings file :
``` DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
 ```
 5. Run `python manange.py migrate`
 6. Run `python manage.py loaddata 'mydb.json'`


```

