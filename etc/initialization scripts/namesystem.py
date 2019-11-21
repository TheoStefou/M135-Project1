import csv

namesystem = open('./HDFS_FS_Namesystem.log')
namesystem_out = open('./HDFS_FS_Namesystem_log.csv', mode='w')
namesystem_out_writer = csv.writer(namesystem_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for i, line in enumerate(namesystem):
	tmp = line.split()

	timestamp = tmp[0]+tmp[1]
	if tmp[9] == 'delete':
		typ = 'delete'
		dest_ip = '-'
		source_ip = tmp[7]
		block_ids = []
		for j in range(10, len(tmp)):
			block_ids.append(tmp[j])
		namesystem_out_writer.writerow(
			[timestamp, ' '.join(block_ids), source_ip, dest_ip, typ]
		)
	elif tmp[9] == 'replicate':
		typ = 'replicate'
		source_ip = tmp[7]
		to_index = 10
		block_ids = []
		for j in range(10, len(tmp)):
			if tmp[j] == 'to':
				to_index = j
				break
			block_ids.append(tmp[j])
		dest_ips = []
		for j in range(to_index+2, len(tmp)):
			dest_ips.append(tmp[j])

		namesystem_out_writer.writerow(
			[timestamp, ' '.join(block_ids), source_ip, ' '.join(dest_ips), typ]
		)
	else:
		print("Something went wrong in line",(i+1))

namesystem.close()
namesystem_out.close()