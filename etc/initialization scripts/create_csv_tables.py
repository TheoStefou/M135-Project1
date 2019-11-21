import csv
import datetime


#THE FILES WITH THE DATA
access_log 		= open('./access_log.csv')
dataxceiver_log = open('./dataxceiver_log.csv')
namesystem_log 	= open('./HDFS_FS_Namesystem_log.csv')

#CSV READERS OF THE FILES
access_log_reader 		= csv.reader(access_log, delimiter=',')
dataxceiver_log_reader 	= csv.reader(dataxceiver_log, delimiter=',')
namesystem_log_reader 	= csv.reader(namesystem_log, delimiter=',')

#THE FILES THAT REPRESENT THE TABLES
log 						= open('./tables/log.csv', 'w')
access_arguments 			= open('./tables/access_arguments.csv', 'w')
dataXceiver_arguments 		= open('./tables/dataXceiver_arguments.csv', 'w')
namesystem_block 			= open('./tables/namesystem_block.csv', 'w')
namesystem_destination_ip 	= open('./tables/namesystem_destination_ip.csv', 'w')

#WRITERS FOR THE FILES-TABLES
log_writer 							= csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
access_arguments_writer 			= csv.writer(access_arguments, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
dataXceiver_arguments_writer 		= csv.writer(dataXceiver_arguments, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
namesystem_block_writer 			= csv.writer(namesystem_block, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
namesystem_destination_ip_writer 	= csv.writer(namesystem_destination_ip, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

log_id_counter = 1

print("Starting access...")
#ACCESS LOG
access_arguments_id_counter = 1
for row in access_log_reader:
	ip 			= row[0]
	userid 		= row[1]
	timestamp 	= row[2]
	http_method = row[3]
	resource	= row[4]
	status 		= row[5]
	size		= row[6]
	referer		= row[7]
	agent 		= row[8]
	
	if userid in ["", "-"]:
		userid = None
	if referer in ["", "-"]:
		referer = None
	if size in ["", "-"]:
		size = -1
	if http_method not in ['GET','POST','HEAD','OPTIONS','DELETE', 'PUT', 'CONNECT', 'TRACE', 'PATCH']:
		continue


	log_writer.writerow([log_id_counter, timestamp, 'access', ip])
	access_arguments_writer.writerow(
		[log_id_counter, userid, http_method, resource, status, size, referer, agent]
	)
	
	log_id_counter += 1
	access_arguments_id_counter += 1
print("Finished access.")

print("Starting dataXceiver...")
#DATAXCEIVER LOG
dataxceiver_arguments_id_counter = 1
for row in dataxceiver_log_reader:
	timestamp 	= row[0]
	block_id 	= row[1]
	source_ip 	= row[2]
	dest_ip 	= row[3]
	size 		= row[4]
	typ 		= row[5]

	timestamp = datetime.datetime.strptime(timestamp, "%d%m%y%H%M%S")
	timestamp = datetime.date.strftime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

	log_writer.writerow([log_id_counter, timestamp, typ, source_ip])
	dataXceiver_arguments_writer.writerow(
		[log_id_counter, block_id, dest_ip, size]
	)

	log_id_counter += 1
	dataxceiver_arguments_id_counter += 1
print("Finished dataxceiver.")

print("Starting namesystem...")
#NAMESYSTEM LOG
namesystem_arguments_id_counter 		= 1
namesystem_block_id_counter 			= 1
namesystem_destination_ip_id_counter 	= 1
for row in namesystem_log_reader:
	timestamp = row[0]
	block_ids = row[1].split()
	source_ip = row[2]
	dest_ips  = row[3].split()
	typ 	  = row[4]

	timestamp = datetime.datetime.strptime(timestamp, "%d%m%y%H%M%S")
	timestamp = datetime.date.strftime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

	log_writer.writerow([log_id_counter, timestamp, typ, source_ip])

	for block in block_ids:
		namesystem_block_writer.writerow([namesystem_block_id_counter, block, log_id_counter])
		namesystem_block_id_counter += 1
	if dest_ips[0] != '-':
		for dest in dest_ips:
			namesystem_destination_ip_writer.writerow([namesystem_destination_ip_id_counter, dest, log_id_counter])
			namesystem_destination_ip_id_counter += 1

	log_id_counter += 1
	namesystem_arguments_id_counter += 1
print("Finished namesystem.")

#CLOSE ALL THE FILES
access_log.close() 		
dataxceiver_log.close()
namesystem_log.close()

log.close() 						
access_arguments.close()
dataXceiver_arguments.close()
namesystem_block.close()
namesystem_destination_ip.close()