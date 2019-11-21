import csv

dataxceiver = open('./HDFS_DataXceiver.log')
dataxceiver_out = open('./dataxceiver_log.csv', 'w')
dataxceiver_out_writer = csv.writer(dataxceiver_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

skip_line = ['WARN', 'ERROR', 'writeBlock', 'Exception', 'exception']

for i, line in enumerate(dataxceiver):
	if any(item in line for item in skip_line):
		continue

	if 'Receiving' in line:
		typ = 'receiving'

		tmp = line.split()
		timestamp = tmp[0]+tmp[1]
		block_id = tmp[7]
		source_ip = tmp[9][1:]
		dest_ip = tmp[11][1:]
		if len(tmp) > 12:
			print('Found receiving with size...line =',(i+1))
			size = tmp[14]
		else:
			size = '-1'
		dataxceiver_out_writer.writerow(
			[timestamp, block_id, source_ip, dest_ip, size, typ]
		)
	elif 'Received' in line:
		typ = 'received'

		tmp = line.split()
		timestamp = tmp[0]+tmp[1]
		block_id = tmp[7]
		source_ip = tmp[9][1:]
		dest_ip = tmp[11][1:]
		if len(tmp) > 12:
			size = tmp[14]
		else:
			size = '-1'
		dataxceiver_out_writer.writerow(
			[timestamp, block_id, source_ip, dest_ip, size, typ]
		)
	elif 'Served' in line:
		typ = 'served'

		tmp = line.split()
		timestamp = tmp[0]+tmp[1]
		source_ip = tmp[5]
		block_id = tmp[8]
		dest_ip = tmp[10][1:]
		size = -1
		if "of size" in line:
			print('Found served with size...line =',(i+1))
		dataxceiver_out_writer.writerow(
			[timestamp, block_id, source_ip, dest_ip, size, typ]
		)

dataxceiver.close()
dataxceiver_out.close()



