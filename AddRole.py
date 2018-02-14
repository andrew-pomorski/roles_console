import mysql.connector
import configparser
import argparse
import sys

parser = argparse.ArgumentParser(description='Add or remove role for user.')
parser.add_argument('--addrole', type=bool, help="Add role to specified user", default=False)
parser.add_argument('--remrole', type=bool, help="Remove role from user", default=False)
parser.add_argument('--role', type=str, help="Which role to assign")
parser.add_argument('--email', type=str, help="Email address of an user")
args = parser.parse_args()

if (args.role == None or args.email == None):
	parser.print_help()
	sys.exit()


EMAIL = args.email
ROLE = args.role

config = configparser.ConfigParser()
config.read('config.ini')

DBUSER = config['DBAUTH']['db_username']
DBNAME = config['DBAUTH']['db_dbname']
DBHOST = config['DBAUTH']['db_host']
DBPWD  = config['DBAUTH']['db_pwd']

cnx = mysql.connector.connect(user=DBUSER, database=DBNAME, host=DBHOST, password=DBPWD)
cursor = cnx.cursor(prepared=True)

query = "SELECT * FROM users WHERE email= %s " 

cursor.execute(query, (EMAIL,))

for stuff in cursor:
	print "User " + EMAIL + "\nID: " + str(stuff[0])
	ID = stuff[0]

if args.addrole:
	stmt = "INSERT INTO roles(userId, role) VALUES (%s, %s)"
	cursor.execute(stmt, (ID, ROLE))
	cnx.commit()
	print "[+] OK"

if args.remrole:
	query = "DELETE FROM roles WHERE userId = %s AND role = %s"
	cursor.execute(query, (ID, ROLE))
	cnx.commit()
	print "[-] OK"
