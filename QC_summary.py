#!/usr/bin/env python
# -*- coding: utf-8 -*-

#raw_input('QC_summary')
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

msScans_total = True
#msScans_total = False
evidence_total = True
evidence_total = False
scan_len = 36

# print to file of just run script
file_output = True
#file_output = False

rewrite = False
#rewrite = True
if rewrite == True:
	last_time = 0
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
	if write == 'w':
		raw_summary_list = [heading_line]
		experiment_summary_list =[heading_line]
	if write == 'a':
		raw_summary_list = []
		experiment_summary_list =[]
	#read_heading_line_list = read_line[0].split
	sn = 0
	en = 0
	scan_write_list = []
	evidence_write_list = []
	for file_name in matches:
		sn += 1
		en += 1
		file_time = os.path.getmtime(file_name)
		#print file_time
		#print int(file_time)
		time_list.append(float(file_time))

			#print file_name

		file_split = file_name.split('/')
		folder_name = '/'.join(file_split[:len(file_split)-1])
		folder_list.append(folder_name)
		
		if float(file_time) > float(last_time):
			print file_time
			word_date = datetime.datetime.fromtimestamp(int(file_time)).strftime('%Y %B %d : %H %M')
			print word_date
			print 'TRUE'
		#run_time = True
		#if run_time == True:
			time_hit = 1 # used to copy the most receent msScans file

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
			scan_hit = 0
			if msScans_total == True:
				scan_file = open(os.path.join(folder_name,'msScans.txt'),'r')
				scan_list = scan_file.readlines()
				scan_file.close()
				if len(scan_list) != 0:
					scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
					#print scan_heading_list
					#raw_input()
					try:

						file_index = scan_heading_list.index('Raw file')
						tic_index = scan_heading_list.index('Total ion current')
						rt_index = scan_heading_list.index('Retention time')
						scan_hit = 1
					except:
						scan_hit = 1
					#raw_input(len(scan_heading_list))
				if sn == 1:

					#raw_input(scan_list)
					#raw_input(scan_list[0])
					#raw_input(len(scan_list))
					if len(scan_list) != 0:

						#raw_input(scan_list[0])
						if write == 'w':
							#scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
							#raw_input(heading_list)
							#raw_input(scan_heading_list)
							scan_entry_list = ['Raw file','Total ion current','Retention time']
							scan_write_list = ['\t'.join(scan_entry_list)+'\r\n']
						else:
							scan_write_list = []
					else:
						sn = 0
				if sn != 0:
					if scan_hit == 1:
						for scan_line in scan_list[1:]:
							scan_line_list = scan_line.split('\t')



							scan_write_list.append('\t'.join([scan_line_list[file_index],scan_line_list[tic_index],scan_line_list[rt_index]]))
						print 'scan hit'
					else:
						print len(scan_heading_list)


			
			if evidence_total == True:
				evidence_file = open(os.path.join(folder_name,'evidence.txt'),'r')
				evidence_list = evidence_file.readlines()
				evidence_file.close()
				if len(evidence_list) != 0:
					evidence_heading_list = evidence_list[0].replace('\r\n','').split('\t')
					print evidence_heading_list
					#raw_input(en)
					try:
						evidence_heading_list.index('Retention length')
						RL_heading = 'Retention length'
					except:
						RL_heading = 'Retention Length'
						
					try:


						file_index = evidence_heading_list.index('Raw file')
						#print file_index
						intensity_index = evidence_heading_list.index('Intensity')
						#print intensity_index
						rt_index = evidence_heading_list.index('Retention time')
						#print rt_index
						rl_index = evidence_heading_list.index(RL_heading)
						#print rl_index
						sequence_index = evidence_heading_list.index('Sequence')
						#print sequence_index
						evidence_hit = 1
					except:
						#file_index = evidence_heading_list.index('Raw file')
						#print file_index
						#intensity_index = evidence_heading_list.index('Intensity')
						#print intensity_index
						#rt_index = evidence_heading_list.index('Retention time')
						#print rt_index
						#rl_index = evidence_heading_list.index('Retention length')
						#print rl_index
						#sequence_index = evidence_heading_list.index('Sequence')
						#print sequence_index
						evidence_hit = 0
						#print 'no evidence'
						#raw_input(len(evidence_heading_list))
				if en == 1:

					#raw_input(evidence_list)
					#raw_input(evidence_list[0])
					#raw_input(len(evidence_list))
					if len(evidence_list) != 0:

						#raw_input(evidence_list[0])
						if write == 'w':
							#evidence_heading_list = evidence_list[0].replace('\r\n','').split('\t')
							#raw_input(heading_list)
							#raw_input(evidence_heading_list)
							evidence_entry_list = ['Raw file','Intensity','Retention time','Retention Length','Sequence']
							evidence_write_list = ['\t'.join(evidence_entry_list)+'\r\n']
						else:
							evidence_write_list = []
					else:
						en = 0
				if en != 0:
					if evidence_hit == 1:
						for evidence_line in evidence_list[1:]:
							evidence_line_list = evidence_line.split('\t')
							#print evidence_line_list
							#print len(evidence_line_list)
							#raw_input()
							#print rl_index
							#raw_input()



							evidence_write_list.append('\t'.join([evidence_line_list[file_index],evidence_line_list[intensity_index],evidence_line_list[rt_index],evidence_line_list[rl_index],evidence_line_list[sequence_index]])+'\n')
						print 'evidence hit'
						#raw_input()
					else:
						print len(evidence_heading_list)










	if file_output == True:
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
	if msScans_total == True:
		write_file_name = '%s/msScans_all.txt' %(output_path)
		#print write_file_name
		write_file = open(write_file_name,write)
		write_file.writelines(scan_write_list)
		write_file.close()
		print write_file_name

	if evidence_total == True:
		write_file_name = '%s/evidence_all.txt' %(output_path)
		#print write_file_name
		write_file = open(write_file_name,write)
		write_file.writelines(evidence_write_list)
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

top_time = sorted(range(len(time_list)), key=lambda i: time_list[i])[-10:]

msScans_top = True
print top_time
print time_index
print time_list[time_index]
scan_write = 'w'
sn = 0

for top_index in top_time:
	
	print folder_list[top_index]
	folder_name = folder_list[top_index]
	if msScans_top == True:
		scan_file = open(os.path.join(folder_name,'msScans.txt'),'r')
		scan_list = scan_file.readlines()
		scan_file.close()
		if len(scan_list) != 0:
			scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
			#print scan_heading_list
			#raw_input()
			try:

				file_index = scan_heading_list.index('Raw file')
				tic_index = scan_heading_list.index('Total ion current')
				rt_index = scan_heading_list.index('Retention time')
				scan_hit = 1
				sn += 1
				scan_hit = 1
				
			except:
				scan_hit = 0
			#raw_input(len(scan_heading_list))
		if sn == 1:

			#raw_input(scan_list)
			#raw_input(scan_list[0])
			#raw_input(len(scan_list))
			if len(scan_list) != 0:

				#raw_input(scan_list[0])
				if scan_write == 'w':
					#scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
					#raw_input(heading_list)
					#raw_input(scan_heading_list)
					scan_entry_list = ['Raw file','Total ion current','Retention time']
					scan_write_list = ['\t'.join(scan_entry_list)+'\r\n']
				else:
					scan_write_list = []
			else:
				sn = 0
		if sn != 0:
			if scan_hit == 1:
				for scan_line in scan_list[1:]:
					scan_line_list = scan_line.replace('\r\n','').split('\t')
					scan_write_list.append('\t'.join([scan_line_list[file_index],scan_line_list[tic_index],scan_line_list[rt_index]])+'\r\n')
				print 'scan hit'
			else:
				print len(scan_heading_list)

if msScans_top == True:
	write_file_name = '%s/msScans_top.txt' %(output_path)
	#print write_file_name
	write_file = open(write_file_name,scan_write)
	write_file.writelines(scan_write_list)
	write_file.close()
	print write_file_name
#raw_input()

#raw_input()

run_r = True
if run_r == True:
	os.system('Rscript %s/MQ_summary.R %s' %(base_path,output_path))

