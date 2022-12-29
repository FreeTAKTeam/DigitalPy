import logging
import pymysql

from exceptions import ConfigurationException
class QueryController:
    
    """  /**
   * Execute a sql script. Execution is done inside a transaction, which is rolled back in case of failure.
   * @param $file The filename of the sql script
   * @param $initSection The name of the configuration section that defines the database connection
   * @return Boolean whether execution succeeded or not.
   */"""
    
	def executeScript(file, initSection):
		logger = logging.getLogger(__name__)
		if os.path.exists(file):
			logger.info(f'Executing SQL script {file} ...')

			# find init params
			config = ObjectFactory.getInstance('configuration')
			if config.getSection(initSection) === False:
				raise ConfigurationException(f"No '{initSection}' section given in configfile.")

			# connect to the database
			conn = createConnection(connectionParams)

			logger.debug('Starting transaction ...')
			conn.beginTransaction()

			exception = None
			with open(file, 'r') as fh:
				for command in fh:
					command = command.strip()
					if len(command) > 0:
						logger.debug(f'Executing command: {command}')
						try:
							conn.query(command)
						except Exception as ex:
							exception = ex
							break
			
			if exception is None:
				logger.debug('Execution succeeded, committing ...')
				conn.commit()
			else:
				logger.error(f'Execution failed. Reason {exception.getMessage()}')
				logger.debug('Rolling back ...')
				conn.rollBack()
			logger.debug(f'Finished SQL script {file}.')
		else:
			logger.error(f'SQL script {file} not found.')

"""
   * Duplicate a database on the same server (same user) e.g for backup. This works only for MySQL databases.
   * @param $srcName The name of the source database
   * @param $destName The name of the source database
   * @param $server The name of the database server
   * @param $user The user name
   * @param $password The password
"""
  def copyDatabase(srcName, destName, server, user, password):
    logger = logging.getLogger(__name__)
    if srcName and destName and server and user:
        createDatabase(destName, server, user, password)

        conn = None
        try:
            conn = pymysql.connect(server, user, password)
        except Exception as ex:
            raise PersistenceException("Couldn't connect to MySql: " + str(ex))

        conn.begin()
        try:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES FROM " + srcName)
            rows = cursor.fetchall()
            for row in rows:
                # create new table
                sqlStmt = "CREATE TABLE " + destName + "." + row[0] + " LIKE " + srcName + "." + row[0]
                logger.debug(sqlStmt)
                cursor.execute(sqlStmt)
                if cursor.rowcount < 0:
                    raise PersistenceException("Couldn't create table: " + str(cursor.errorinfo()))

                # insert data
                sqlStmt = "INSERT INTO " + destName + "." + row[0] + " SELECT * FROM " + srcName + "." + row[0]
                logger.debug(sqlStmt)
                cursor.execute(sqlStmt)
                if cursor.rowcount < 0:
                    raise PersistenceException("Couldn't copy data: " + str(cursor.errorinfo()))
            conn.commit()
        except Exception as ex:
            conn.rollback()
  
  """  /**
   * Crate a database on the server. This works only for MySQL databases.
   * @param $name The name of the source database
   * @param $server The name of the database server
   * @param $user The user name
   * @param $password The password
   */"""
   def createDatabase(name: str, server: str, user: str, password: str) -> bool:
    created = False
    if name and server and user:
        # setup connection
        conn = None
        try:
            conn = pymysql.connect(host=server, user=user, password=password)
        except Exception as ex:
            raise PersistenceException(f"Couldn't connect to MySql: {ex}")
        # create database
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")
        created = True
        if not created:
            raise PersistenceException(f"Couldn't create database: {conn.error()}")
    return created
