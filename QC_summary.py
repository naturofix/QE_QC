#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import time
import datetime

base_path = '/mnt/BLACKBURNLAB/scripts/QC'

try:
	QC_path = sys.argv[1]
	last_time = sys.argv[2]
	write = 'a'
except:
	QC_path = '/mnt/BLACKBURNLAB/QC/Reference'
	last_time = 0
	write = 'w'

# trying to update the scirpt to only append files, but it is not working
#so this is a work arround
last = 0
write = 'w'



output_path = os.path.join(QC_path,'summary')
os.system('mkdir %s' %output_path)

print '\n\n\nSearching %s .......\n\n' %(QC_path)

time_file = '%s/time.txt' %(base_path)
time_list = []
folder_list = []
x = 1
summary = True
time_hit = 0
if summary == True:
	matches = []
	for root, dirnames, filenames in os.walk(QC_path):
	  for filename in fnmatch.filter(filenames, 'summary.txt'):
	    matches.append(os.path.join(root, filename))
	#print matches



	heading_list = ['Raw file', 'Experiment', 'MS', 'MS/MS', 'MS/MS Submitted', 'MS/MS Identified', 'MS/MS Identified [%]']
	heading_list = heading_list + ['Peaks Sequenced', 'Peaks Sequenced [%]', 'Peaks Repeatedly Sequenced [%]', 'Peptide Sequences Identified']
	heading_list = heading_list + ['Av. Absolute Mass Deviation [ppm]', 'Mass Standard Deviation [ppm]']
	heading_line = '\t'.join(['Date']+heading_list)+'\n'

	read_length_list = []
	raw_summary_list = [heading_line]
	experiment_summary_list =[heading_line]
	#read_heading_line_list = read_line[0].split
	for file_name in matches:
		file_time = os.path.getmtime(file_name)
		#print file_time
		#print int(file_time)
		if file_time > last_time:
			time_hit = 1
			time_list.append(float(file_time))

			#print file_name

			file_split = file_name.split('/')
			folder_name = '/'.join(file_split[:len(file_split)-1])
			folder_list.append(folder_name)
			#print(os.listdir(folder_name))
			parameter_name = '/'.join(file_split[:len(file_split)-1]+['parameters.txt'])
			#print parameter_name
			try:
				read_file = open(parameter_name,'r')
				param_list = read_file.readlines()
				read_file.close()
				date_line = ''
				for param_line in param_list:
				
					param_line_list = param_line.split('\t')
					if param_line_list[0] == 'Date of writing':
						date_line_list = param_line_list[1].split(' ')[0].split('/')
						#print(date_line_list)
						new_date_list = [date_line_list[2],date_line_list[0],date_line_list[1]]
						date_line = ''.join(new_date_list)
				#if date_line == '':
				#	for param_line in param_list:
				#		print param_line
					#raw_input()

				#print date_line
			except:
				date_line = ''


			#raw_input()
			read_file = open(file_name,'r')
			read_list = read_file.readlines()
			read_file.close()

			read_heading_line_list = read_list[0].replace('\r\n','').split('\t')
			if x == 0 :
				raw_input(read_heading_line_list)
				x = 1
			index_list = []
			for heading in heading_list:
				try:

					index_entry = read_heading_line_list.index(heading)
				except:
					index_entry = ''
				#print index_entry
				index_list.append(index_entry)

			#raw_input(index_list)
			if len(read_list) > 1:
				for read_line in read_list[1:]:
					read_line_list = read_line.replace('\r\n','').split('\t')
					write_list = []
					for index in index_list:
						if index != '':
							write_list.append(read_line_list[index])
						else:
							write_list.append('')
					#raw_input(write_list)		
					write_line = '\t'.join([date_line]+write_list)+'\n'
					#print(write_line)
					if len(read_line_list) > 1:
						if read_line_list[1] == '':
							#print 'experiment'
							experiment_summary_list.append(write_line)
						else:
							#print 'raw' 
							raw_summary_list.append(write_line)
					else:
						print 'blank line'



	write_file_name = '%s/summary_RAW.txt' %(output_path)
	#print write_file_name
	write_file = open(write_file_name,write)
	write_file.writelines(raw_summary_list)
	write_file.close()
	print write_file_name
	write_file_name = '%s/summary_Experiment.txt' %(output_path)
	#print write_file_name
	write_file = open(write_file_name,write)
	write_file.writelines(experiment_summary_list)
	write_file.close()

	print write_file_name
#raw_input()
print time_list
if time_hit == 1:
	print time_list
	time_index = time_list.index(max(time_list))
	last_folder = folder_list[time_index]
	print last_folder
	#raw_input()
	cmd = 'cp %s/msScans.txt %s/msScans.txt' %(last_folder,output_path)
	print cmd
	os.system(cmd)

#raw_input()

run_r = True
if run_r == True:
	os.system('Rscript %s/MQ_summary.R %s' %(base_path,output_path))

