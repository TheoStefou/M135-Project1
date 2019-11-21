import csv

access_out = open('./access_log.csv', mode='w')
access_out_writer = csv.writer(access_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

#access has: IP_address, UserID, Timestamp, HTTPmethod, resource, response_status, size, referer, agent
with open('./access.log') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter= ' ')
	for i,row in enumerate(csv_reader):
		ip = row[0]
		userid = row[2]
		timestamp = row[3][1:]+' '+row[4][:-1]
		tmp = row[5].split() #split into method, resource, protocol
		http_method = tmp[0]
		resource = tmp[1]
		response_status = row[6]
		size = row[7]
		referer = row[8]
		agent = row[9]
		
		if http_method not in ['GET','POST','HEAD','OPTIONS','DELETE', 'PUT', 'CONNECT', 'TRACE', 'PATCH']:
			continue

		try:
			size = int(size)
			response_status = int(response_status)
		except:
			continue

		access_out_writer.writerow(
			[ip, userid, timestamp, http_method, resource, response_status, size, referer, agent]
		)


access_out.close()




