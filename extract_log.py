import os
import sys



base_path = sys.argv[1]
base_path = os.path.join(base_path,'extract_log')
last_time = sys.argv[2]

write = 'a'

info_list = []
cal_list = []
cal_error_list = []
cal_warning_list = []
cal_end_list = []
eval_list = []
eval_error_list = []
eval_warning_list = []
eval_end_list = []
tune_list = []
tune_error_list = []
tune_warning_list = []
tune_end_list = []
#eval_completed = []

tune_dic = {}
tune_error_dic = {}
tune_warning_dic = {}
tune_end_dic = {}

error_list = []
warning_list = []
error_dic = {}
warning_dic = {}

#	file_name = '/mnt/BLACKBURNLAB/temp_files/Thermo Exactive--2016-10-05--13-25-03.log'
log_path = '/blackburn3/RAW_Data/Q_Exactive_2014/Xcalibur/system/Exactive/log/'

file_list = os.listdir(log_path)
file_list.sort()



for file_name in file_list:
	hit = 0
	file_path = log_path+file_name
	file_time = os.path.getmtime(file_path)
	if file_time > last_time:
		hit = 1
	if write == 'w':
		hit = 1

	if 'Thermo Exactive' in file_name and hit = 1:
		print file_name
		read_file = open(log_path+file_name,'r')
		read_list = read_file.readlines()
		read_file.close()

		cal = 0
		evaluation = 0
		tune = 0
		n = 0
		for read_line in read_list:
			#print read_line
			read_line_list = read_line.replace('\r\n','').split(']')
			#print(read_line_list)
			#cal = 0
			n += 1
			if '= = = Running Calibration.. = = =' in read_line_list:
				#print '\nstart'
				#print read_line_list
				cal = 1
				n = 0
				cal_dic = {}
				cal_error_dic = {}
				cal_warning_dic = {}
				cal_end_dic = {}
			#if 'Calibration successful. Saving calibration results.\t\n' in read_line_list:


			if '= = = Running Evaluation.. = = =' in read_line_list:
				#print '\nstart'
				#print read_line_list
				evaluation = 1
				n = 0
				eval_dic = {}
				eval_error_dic = {}
				eval_warning_dic = {}
				eval_end_dic = {}

			if '= = = running automatic tuning.. = = =' in read_line_list:
				#print '\nstart'
				#print read_line_list
				tune = 1
				n = 0
				tune_dic = {}
				tune_error_dic = {}
				tune_warning_dic = {}
				tune_end_dic = {}

			if cal == 1:
				info_list.append(read_line_list)
				if '[Type=info'in read_line_list:
					cal_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=error'in read_line_list:
					cal_error_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=warning'in read_line_list:
					cal_warning_dic[read_line_list[0]] = read_line_list[-1]


			

			if evaluation == 1:
				info_list.append(read_line_list)
				if '[Type=info'in read_line_list:
					eval_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=error'in read_line_list:
					eval_error_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=warning'in read_line_list:
					eval_warning_dic[read_line_list[0]] = read_line_list[-1]




			if tune == 1:
				info_list.append(read_line_list)
				if '[Type=info'in read_line_list:
					tune_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=error'in read_line_list:
					tune_error_dic[read_line_list[0]] = read_line_list[-1]
				if '[Type=warning'in read_line_list:
					tune_warning_dic[read_line_list[0]] = read_line_list[-1]


			if tune == 0 and cal == 0 and evaluation == 0:
				if file_name in file_list[-40:] :
					if '[Type=error'in read_line_list:
						#print(read_line_list)
						#print read_line_list[0]
						#print read_line_list[-1]
						error_dic[read_line_list[0]] = read_line_list[-1]
						error_list.append(error_dic)

				if file_name in file_list[-10:] :
					if '[Type=warning'in read_line_list:
						#print read_line_list
						#print(read_line_list)
						#print read_line_list[0]
						#print read_line_list[-1]
						warning_dic[read_line_list[0]] = read_line_list[-1]
						warning_list.append(warning_dic)
				



			if read_line_list[-1][:12] == 'Calibration ':
			#if 'Calibration ' in read_line_list[-1]:
				#print '\n\n\ndictionary\n'
				#print diff
				#print '\nstop' 
				#print read_line_list
				cal = 0
				#diff[read_line_list[0]] = read_line_list[-1]
				cal_list.append(cal_dic)
				cal_error_list.append(cal_error_dic)
				cal_end_dic[read_line_list[0]] = read_line_list[-1]
				cal_end_list.append(cal_end_dic)

			if  read_line_list[-1][:11] == 'Evaluation ':
				#print '\n\n\ndictionary\n'
				#print diff
				#print '\nstop' 
				#print read_line_list
				evaluation = 0
				#eval_dic[read_line_list[0]] = read_line_list[-1]
				eval_list.append(eval_dic)
				eval_error_list.append(eval_error_dic)
				eval_warning_list.append(eval_warning_dic)
				eval_end_dic[read_line_list[0]] = read_line_list[-1]
				eval_end_list.append(eval_end_dic)

			if  read_line_list[-1][:9] == 'Autotune ':
				#print(read_line_list)
				#raw_input()
				#print '\n\n\ndictionary\n'
				#print diff
				#print '\nstop' 
				#print read_line_list
				tune = 0
				#eval_dic[read_line_list[0]] = read_line_list[-1]
				tune_list.append(tune_dic)
				tune_error_list.append(tune_error_dic)
				tune_warning_list.append(tune_warning_dic)
				tune_end_dic[read_line_list[0]] = read_line_list[-1]
				tune_end_list.append(tune_end_dic)

			#print cal


# for info_line in info_list:
# 	print info_line
# 	print '\n'
# 	print 'info'

hit_entry_list = [' Ok: ',' Done :']

write_list = []
extract_list = []
print 'Calibration : %s' %len(cal_list)
for diff in cal_list:
	#print '\n\ndictionary\n'
	#print diff
	for key in diff.keys():
		write_line = '\t'.join([key,diff[key]])+'\n'
		write_list.append(write_line)
		#hit_entry = ' Ok: '
		#completed_list = [' Ok: ']
		for hit_entry in hit_entry_list:
			if hit_entry in diff[key]:

				entry_list = key.replace('[Time=','').split('.')[0].split(' ')
				property_list = diff[key].split(hit_entry)
				entry_list.append(property_list[0].replace("'",'')[1:])
				#entry_list = entry_list+property_list[1].split(', ')
				entry_list.append(property_list[1])

				#print(entry_list)

				entry_line = '\t'.join(entry_list)+'\n'
				extract_list.append(entry_line)


write_file_name = os.path.join(base_path,'temp.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()


write_file_name = os.path.join(base_path,'cal.txt')
write_file = open(write_file_name,write)
write_file.writelines(extract_list)
write_file.close()



write_list = []
extract_list = []
print 'Evaluation : %s' %len(eval_list)
for diff in eval_list:
	#print '\n\ndictionary\n'
	#print diff
	for key in diff.keys():
		write_line = '\t'.join([key,diff[key]])+'\n'
		write_list.append(write_line)
		for hit_entry in hit_entry_list:
		
		#completed_list = [' Ok: ']
			if hit_entry in diff[key]:

				entry_list = key.replace('[Time=','').split('.')[0].split(' ')
				property_list = diff[key].split(hit_entry)
				entry_list.append(property_list[0].replace("'",'')[1:])
				#entry_list = entry_list+property_list[1].split(', ')
				entry_list.append(property_list[1])
				#print(entry_list)
				entry_line = '\t'.join(entry_list)+'\n'
				extract_list.append(entry_line)


write_file_name = os.path.join(base_path,'eval_temp.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()


write_file_name = os.path.join(base_path,'eval.txt')
write_file = open(write_file_name,write)
write_file.writelines(extract_list)
write_file.close()

write_list = []
extract_list = []
print 'Tune : %s' %len(tune_list)
for diff in tune_list:
	#print '\n\ndictionary\n'
	#print diff
	for key in diff.keys():
		write_line = '\t'.join([key,diff[key]])+'\n'
		write_list.append(write_line)
		hit_entry = ' Ok: '
		#completed_list = [' Ok: ']
		for hit_entry in hit_entry_list:
			if hit_entry in diff[key]:

				entry_list = key.replace('[Time=','').split('.')[0].split(' ')
				property_list = diff[key].split(hit_entry)
				entry_list.append(property_list[0].replace("'",'')[1:])
				#entry_list = entry_list+property_list[1].split(', ')
				entry_list.append(property_list[1])
				#print(entry_list)
				entry_line = '\t'.join(entry_list)+'\n'
				extract_list.append(entry_line)


write_file_name = os.path.join(base_path,'tune_temp.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()


write_file_name = os.path.join(base_path,'tune.txt')
write_file = open(write_file_name,write)
write_file.writelines(extract_list)
write_file.close()


write_list = []
extract_list = []
print 'Calibration Errors : %s' %len(cal_error_list)
for dic in cal_error_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)
print '%s : %s ' %(write_file_name,len(write_list))
write_file_name = os.path.join(base_path,'cal_error.txt')
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()	


write_list = []
print 'Calibration Warnings : %s' %len(cal_warning_list)
for dic in cal_warning_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'cal_warning.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

write_list = []

write_list = []
print 'Calibration Completion : %s' %len(cal_end_list)
for dic in cal_end_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'cal_end.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

write_list = []
print 'Evaluation Errors : %s' %len(eval_error_list)
for dic in eval_error_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'eval_error.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()	


write_list = []
print 'Evaluation Warnings : %s' %len(eval_warning_list)
for dic in eval_warning_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'eval_warning.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

write_list = []
print 'Evaluation Completion : %s' %len(eval_end_list)
for dic in eval_end_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'eval_end.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

write_list = []
print 'Tune Errors : %s' %len(tune_error_list)
for dic in tune_error_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'tune_error.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()	


write_list = []
print 'Tune Warnings : %s' %len(tune_warning_list)
for dic in tune_warning_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'tune_warning.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

write_list = []
print 'Tune Completion : %s' %len(tune_end_list)
for dic in tune_end_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'tune_end.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()



write_list = []
print 'Errors : %s' %len(error_list)
for dic in error_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'error.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()	


write_list = []
print 'Warning : %s' %len(warning_list)
for dic in warning_list:
	#print '\n\ndictionary\n'
	#print dic
	for key in dic.keys():
		write_line = '\t'.join(key.replace('[Time=','').split('.')[0].split(' ')+[dic[key]])+'\n'
		write_list.append(write_line)

write_file_name = os.path.join(base_path,'warning.txt')
print '%s : %s ' %(write_file_name,len(write_list))
write_file = open(write_file_name,write)
write_file.writelines(write_list)
write_file.close()

