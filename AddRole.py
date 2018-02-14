#!/usr/bin/env python

import mysql.connector
import configparser
import argparse
import sys

parser = argparse.ArgumentParser(description='Add or remove role for user.')
parser.add_argument('--addrole', type=bool, help="Add role to specified user", default=False)
parser.add_argument('--remrole', type=bool, help="Remove role from user", default=False)
parser.add_argument('--checkrole', type=bool, help="Check what roles are assigned to given user", default=False)
parser.add_argument('--role', type=str, help="Which role to assign")
parser.add_argument('--email', type=str, help="Email address of an user")
args = parser.parse_args()

if (args.checkrole == False and (args.role == None or args.email == None)):
	parser.print_help()
	sys.exit()


EMAIL = args.email
ROLE = args.role
HAS_ROLES = []

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

rows = cursor.fetchall()

if (len(rows)) < 1:
	print "User with email: " + EMAIL + " not found."
	sys.exit()



for stuff in rows:
	#print "User " + EMAIL + "\nID: " + str(stuff[0])
	ID = stuff[0]


# check what roles the user already has
query = "SELECT * FROM roles WHERE userId= %s"
cursor.execute(query, (ID,))
rows = cursor.fetchall()
for row in rows:
	HAS_ROLES.append(row[4])


if args.checkrole:
	stmt = "SELECT * FROM roles WHERE userId = %s"
	cursor.execute(stmt, (ID, ))
	rows = cursor.fetchall()
	print "User: " + EMAIL + " roles:"
	for row in rows:
		print "ROLE: " + row[4]

if args.addrole:
	if not ROLE in HAS_ROLES:
		stmt = "INSERT INTO roles(userId, role) VALUES (%s, %s)"
		cursor.execute(stmt, (ID, ROLE))
		cnx.commit()
		print "[+] OK"
	else:
		print "User: " + EMAIL + " already has the role: " + ROLE

if args.remrole:
	query = "DELETE FROM roles WHERE userId = %s AND role = %s"
	cursor.execute(query, (ID, ROLE))
	cnx.commit()
	print "[-] OK"
