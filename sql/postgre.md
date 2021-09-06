
|Command|Action|Arguments|
|------|--------|--------|
| psql -d database -U user -W |	Connects to a database under a specific user |	-d: used to state the database name -U: used to state the database user |
| psql -h host -d database -U user -W|	Connect to a database that resides on another host |	-h: used to state the host -d: used to state the database name -U:used to state the database user |
| psql -U user -h host “dbname=db sslmode=require”	| Use SSL mode for the connection	-h: used to state the host | -U:used to state the database user |
| \c dbname |	Switch connection to a new database	
| \l |	List available databases	
| \dt |	List available tables	
| \d table_name |	Describe a table such as a column, type, modifiers of columns, etc.	
| \dn |	List all schemas of the currently connected database	
| \df |	List available functions in the current database	
| \dv |	List available views in the current database	
| \du |	List all users and their assign roles	
| SELECT version(); |	Retrieve the current version of PostgreSQL server	
| \g |	Exexute the last command again	
| \s |	Display command history	
| \s filename |	Save the command history to a file	
| \i filename |	Execute psql commands from a file	
| \? |	Know all available psql commands	
| \h COMMAND |	Get help	
| \e |	Edit command in your own editor	
| \a |	Switch from aligned to non-aligned column output	
| \H |	Switch the output to HTML format	
| \q |	Exit psql shell


#### By default postgres makes all strings lowercase, to prevent this, use double quotes