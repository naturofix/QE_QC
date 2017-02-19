import os
import sys
import re

base_path = sys.argv[1]
base_path = os.path.join(base_path,'extract_log')

read_file = open(os.path.join(base_path,'cal.txt'),'r')
read_list = read_file.readlines()
read_file.close()


feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	feature_list.append(read_line_list[2])

#print(len(set(feature_list)))
#print(set(feature_list))

dic = {}
for entry in set(feature_list):
	#print(entry)
	dic[entry] = []

feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	dic[read_line_list[2]].append(read_line_list)

regular_expressions = ['-?[0-9]+\.?[0-9]?[0-9]?[0-9]?']

os.system('mkdir calibration')
for key in dic.keys():
	#print key
	write_list = []
	entry_list_list = dic[key]
	for entry_list in entry_list_list:
		#print(entry_list)
		entry_list[-1] = entry_list[-1].replace('\n','')
		search_entry_list = entry_list
		for entry in search_entry_list[2:]:
			for reg in regular_expressions:
				all_ref = re.findall(reg,entry)

				entry_list = entry_list + all_ref

		#print entry_list		
		write_line = '\t'.join(entry_list)+'\n'
		write_list.append(write_line)
	#print(key)
	#print(entry_list)
	#print(len(entry_list))
	if len(entry_list) > 4:
		write_file_name = os.path.join(base_path,'calibration/%s.txt' %(key.replace('/','_')))
		print write_file_name
		write_file = open(write_file_name,'w')
		write_file.writelines(write_list)
		write_file.close()


read_file = open(os.path.join(base_path,'eval.txt'),'r')
read_list = read_file.readlines()
read_file.close()


feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	feature_list.append(read_line_list[2])

print(len(set(feature_list)))
print(set(feature_list))

dic = {}
for entry in set(feature_list):
	#print(entry)
	dic[entry] = []

feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	dic[read_line_list[2]].append(read_line_list)


os.system('mkdir evaluation')
for key in dic.keys():
	#print key
	write_list = []
	entry_list_list = dic[key]
	for entry_list in entry_list_list:
		#print(entry_list)
		entry_list[-1] = entry_list[-1].replace('\n','')
		search_entry_list = entry_list
		for entry in search_entry_list[2:]:
			for reg in regular_expressions:
				all_ref = re.findall(reg,entry)

				entry_list = entry_list + all_ref

		#print entry_list
		write_line = '\t'.join(entry_list)+'\n'
		write_list.append(write_line)

	if len(entry_list) > 4:
		write_file_name = os.path.join(base_path,'evaluation/%s.txt' %(key.replace('/','_')))
		print write_file_name
		write_file = open(write_file_name,'w')
		write_file.writelines(write_list)
		write_file.close()


read_file = open(os.path.join(base_path,'tune.txt'),'r')
read_list = read_file.readlines()
read_file.close()


feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	feature_list.append(read_line_list[2])

#print(len(set(feature_list)))
#print(set(feature_list))

dic = {}
for entry in set(feature_list):
	#print(entry)
	dic[entry] = []

feature_list = []
for read_line in read_list:
	read_line_list = read_line.split('\t')
	#print read_line_list
	dic[read_line_list[2]].append(read_line_list)


os.system('mkdir tune')
for key in dic.keys():
	#print key
	write_list = []
	entry_list_list = dic[key]
	for entry_list in entry_list_list:
		#print(entry_list)
		entry_list[-1] = entry_list[-1].replace('\n','')
		search_entry_list = entry_list
		for entry in search_entry_list[2:]:
			for reg in regular_expressions:
				all_ref = re.findall(reg,entry)

				entry_list = entry_list + all_ref

		#print entry_list
		write_line = '\t'.join(entry_list)+'\n'
		write_list.append(write_line)
	#print(key)
	#print(key)
	#print entry_list
	#print len(entry_list)
	if len(entry_list) > 4:
		write_file_name = os.path.join(base_path,'tune/%s.txt' %(key.replace('/','_')))
		print write_file_name
		write_file = open(write_file_name,'w')
		write_file.writelines(write_list)
		write_file.close()

read_file = open(os.path.join(base_path,'tune_end.txt'),'r')
read_list = read_file.readlines()
read_file.close()


feature_list = []
for read_line in read_list:
	read_line = read_line.replace('\n','')
	read_line_list = read_line.split('\t')
	#print read_line_list
	#print read_line_list	property_list = read_line_list[2].split('. ')
	property_list = read_line_list[2].split('. ')
	#print property_list
	new_read_line_list = read_line_list[:2]+property_list[:2]
	#print new_read_line_list

	#print new_read_line_list[2]
	#raw_input()
	feature_list.append(new_read_line_list[2])

print(len(set(feature_list)))
print(set(feature_list))

dic = {}
for entry in set(feature_list):
	#print(entry)
	dic[entry] = []

feature_list = []
for read_line in read_list:
	read_line = read_line.replace('\n','')
	read_line_list = read_line.split('\t')
	read_line_list = read_line.split('\t')
	property_list = read_line_list[2].split('. ')
	new_read_line_list = read_line_list[:2]+property_list[:2]
	dic[new_read_line_list[2]].append(new_read_line_list)


os.system('mkdir tune')
for key in dic.keys():
	#print key
	write_list = []
	entry_list_list = dic[key]
	for entry_list in entry_list_list:
		#print(entry_list)
		entry_list[-1] = entry_list[-1].replace('\n','').replace('decreased by ','-')
		search_entry_list = entry_list
		#print search_entry_list
		#raw_input()
		for entry in search_entry_list[2:]:
			for reg in regular_expressions:
				all_ref = re.findall(reg,entry)

				entry_list = entry_list + all_ref

		#print entry_list
		
		write_line = '\t'.join(entry_list)+'\n'
		write_list.append(write_line)
	print(key)
	#file_key = key.replace('')
	if len(entry_list) > 4:
		write_file_name = os.path.join(base_path,'tune/%s.txt' %(key.replace('/','_')))
		print write_file_name
		write_file = open(write_file_name,'w')
		write_file.writelines(write_list)
	write_file.close()
