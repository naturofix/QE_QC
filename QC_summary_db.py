#!/usr/bin/env python
# -*- coding: utf-8 -*-

#raw_input('QC_summary')
import os
import sys
import fnmatch
import time
import datetime
import sqlite3 as lite
import re

def sql_replace(entry):
	sql_replace_list = [' ','/']
	for sql in sql_replace_list:
		entry = entry.replace(sql,'_')
	return entry

database_name = '/blackburn3/temp/db/Ref_QC.db'
con = lite.connect(database_name)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

commit_db = True
#commit_db = False # prevent changing of the database


base_path = '/mnt/BLACKBURNLAB/scripts/QC'

try:
	QC_path = sys.argv[1]
	last_time = sys.argv[2]
	write = 'a'
except:
	QC_path = '/mnt/BLACKBURNLAB/QC/Reference'
	last_time = 0
	write = 'w'

# print to file of just run script
run_summary = True
#run_summary = False

file_output = True
#file_output = False
summary_table = 0 #drop table


msScans_total = True
#msScans_total = False
scan_table = 0 #drop table
s_index_list = []

evidence_total = True
#evidence_total = False
evidence_table = 0 #drop table
scan_len = 36


rewrite = True
#rewrite = False

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

	sql_header_list = ['Raw_file', 'Experiment', 'MS', 'MS_MS', 'MS_MS_Submitted', 'MS_MS_Identified', 'MS_MS_Identified_percentage']
	sql_header_list = sql_header_list + ['Peaks_Sequenced', 'Peaks_Sequenced_percentage', 'Peaks_Repeatedly_Sequenced_percentage', 'Peptide_Sequences _dentified']
	sql_header_list = sql_header_list + ['Av_Absolute_Mass_Deviation_ppm', 'Mass_Standard_Deviation_ppm']
	sql_header_list = sql_header_list + ['Date',"Column",'Gradient','Loading','Flow_Rate']
	#sql_header_line = '\t'.join(['Date']+heading_list)+'\n'

	read_length_list = []
	if write == 'w' and summary_table != 1:
		raw_summary_list = [heading_line]
		experiment_summary_list =[heading_line]

		table_name = 'summary_RAW'
		header_list = sql_header_list
		cmd = 'DROP TABLE IF EXISTS %s' %(table_name)
		print cmd
		cur.execute(cmd)
		sql_header_line = 'Create Table if not exists %s (%s)' %(table_name,', '.join(header_list))
		print sql_header_line
		raw_input()
		cur.execute(sql_header_line)

		table_name = 'summary_Experiment'
		cur.execute('DROP TABLE IF EXISTS %s' %(table_name))
		sql_header_line = 'Create Table if not exists %s (%s)' %(table_name,', '.join(header_list))
		summary_table = 1
		#print sql_header_line
		#raw_input()
		#cur.execute(sql_header_line)
	if write == 'a':
		raw_summary_list = []
		experiment_summary_list =[]
	#read_heading_line_list = read_line[0].split
	sn = 0
	en = 0
	evidence_write_list = []
	m = 0
	for file_name in matches:
		m += 1
		print '\n\n##################################\n\n' 
		print '%s of %s' %(m,len(matches))
		pse = 0
		psr = 0
		ps = 0
		pe = 0
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
			print word_date +'\n'
			#print 'TRUE'
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
			if run_summary == True:
				read_file = open(file_name,'r')
				read_list = read_file.readlines()
				read_file.close()

				read_heading_line_list = read_list[0].replace('\r\n','').split('\t')
				if x == 0 :
					#raw_input(read_heading_line_list)
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
						entry_list = write_list
						date = ''
						try:			
							nums_list = re.findall(r'\d+',entry_list[0])
							#print nums_list
							if len(nums_list) > 0:
					
								long_num = max(nums_list, key=len)
								#print long_num
								if len(long_num) > 8:
									date = datetime.datetime.strptime(long_num[0:6], '%y%m%d').date()
								elif len(long_num) == 8:
									date = datetime.datetime.strptime(long_num, '%Y%m%d').date()
								elif len(long_num) == 6:
									date = datetime.datetime.strptime(long_num, '%y%m%d').date()


								#print date
								#print str(date)
						except:
							date = ''
						entry_list.append(str(date))
						column = ''
						column_search = re.search('(c|C)(1|2)',entry_list[0])
						if column_search != None:
							#print entry_list[0]						
							#print column_search
							#print column_search.group()
							column = column_search.group().upper()
							#print column
							#raw_input()
						entry_list.append(column)
						gradient = ''
						gradient_search = re.search('\d{2,3}min',entry_list[0])
						if gradient_search != None:
							#print entry_list[0]
							#print gradient_search.group()
							gradient = gradient_search.group().replace('min','')
							#raw_input()
						gradient_search = re.search('G\d{2,3}',entry_list[0])
						if gradient_search != None:
							#print entry_list[0]
							#print gradient_search.group()
							gradient = gradient_search.group().replace('G','')
							#raw_input()
						entry_list.append(gradient)
						loading = ''
						loading_search = re.search('\d{2,4}ng',entry_list[0])
						if loading_search != None:
							#print entry_list[0]
							#print loading_search.group()
							loading = loading_search.group()
						loading_search = re.search('\d{1}ug',entry_list[0])
						if loading_search != None:
							#print entry_list[0]
							#print loading_search.group()
							loading = loading_search.group().replace('ug','')
							loading = '%sng' %(int(loading)*1000)
							#print loading
							#raw_input()
						entry_list.append(loading)
						flow = ''
						loading_search = re.search('\d{2,3}nl',entry_list[0])
						if loading_search != None:
							#print entry_list[0]
							#print loading_search.group()
							flow = loading_search.group()
						entry_list.append(flow)

						#print(write_line)
						if len(read_line_list) > 1:
							if read_line_list[1] == '':
								#print 'experiment'
								#experiment_summary_list.append(write_line) 
								table_name = 'summary_Experiment'
								cmd = 'INSERT INTO %s VALUES("%s")' %(table_name,'","'.join(entry_list))
								if pse == 2:
									print cmd
									pse = 1
									print 'please wait ...'
								#cur.execute(cmd)
							else:
								#print 'raw' 
								#raw_summary_list.append(write_line)
								table_name = 'summary_RAW' 
								cmd = 'INSERT INTO %s VALUES("%s")' %(table_name,'","'.join(entry_list))
								if psr == 0:
									print cmd
									psr = 1
									print '\n'
								cur.execute(cmd)
						else:
							print 'blank line'
				#scan_hit = 0
			if msScans_total == True:
				
				table_name = 'scans'
				scan_file = open(os.path.join(folder_name,'msScans.txt'),'r')
				scan_list = scan_file.readlines()
				scan_file.close()
				if len(scan_list) != 0:
					scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
					#print scan_heading_list
					#raw_input()
					try:

						s_file_index = scan_heading_list.index('Raw file')
						s_tic_index = scan_heading_list.index('Total ion current')
						s_rt_index = scan_heading_list.index('Retention time')

						scan_hit = 1
					except:
						#s_file_index = scan_heading_list.index('Raw file')
						#s_tic_index = scan_heading_list.index('Total ion current')
						#s_rt_index = scan_heading_list.index('Retention time')
						#raw_input('scan error')
						scan_hit = 0
					#raw_input(len(scan_heading_list))
				if sn == 1:

					#raw_input(scan_list)
					#raw_input(scan_list[0])
					#raw_input(len(scan_list))
					if len(scan_list) > 1:

						#raw_input(scan_list[0])
						if write == 'w' and scan_table != 1:
							#scan_heading_list = scan_list[0].replace('\r\n','').split('\t')
							#raw_input(heading_list)
							#raw_input(scan_heading_list)
							scan_entry_list = ['Raw_file','Total_ion_current','Retention_time']
							scan_write_list = ['\t'.join(scan_entry_list)+'\r\n']
							
							header_list = scan_entry_list
							cmd = 'DROP TABLE IF EXISTS %s' %(table_name)
							print cmd
							cur.execute(cmd)
							sql_header_line = 'Create Table if not exists %s (%s)' %(table_name,', '.join(header_list))
							print sql_header_line
							raw_input()
							cur.execute(sql_header_line)
							scan_table = 1
						else:
							scan_write_list = []
					else:
						print scan_list
						#raw_input()
						sn = 0
				if sn != 0:
					if scan_hit == 1:
						for scan_line in scan_list[1:]:
							scan_line_list = scan_line.split('\t')

							scan_entry_list = [scan_line_list[s_file_index],scan_line_list[s_tic_index],scan_line_list[s_rt_index]]

							#scan_write_list.append('\t'.join(scan_entry_list))
							cmd = 'INSERT INTO %s VALUES("%s")' %(table_name,'","'.join(scan_entry_list))
							if ps == 0:
								print cmd
								ps = 1
								print '\n'
							cur.execute(cmd)
						#print 'scan hit'
					else:
						print scan_list[0]
						print scan_list[1]
						print len(scan_heading_list)
						#raw_input()

			
			if evidence_total == True:
				table_name = 'evidence'
				evidence_file = open(os.path.join(folder_name,'evidence.txt'),'r')
				evidence_list = evidence_file.readlines()
				evidence_file.close()
				if len(evidence_list) != 0:
					evidence_heading_list = evidence_list[0].replace('\r\n','').split('\t')
					#print evidence_heading_list
					#raw_input(en)
					try:
						evidence_heading_list.index('Retention length')
						RL_heading = 'Retention length'
					except:
						RL_heading = 'Retention Length'
					e_select_heading_list = ['Raw file','Sequence','Charge','m/z','Intensity','Retention time',RL_heading]
						
					try:
						e_index_list = []
						for e_heading in e_select_heading_list:
							e_index_list.append(evidence_heading_list.index(e_heading))

						#raw_input(e_index_list)
						#file_index = evidence_heading_list.index('Raw file')
						#print file_index
						#intensity_index = evidence_heading_list.index()
						#print intensity_index
						#rt_index = evidence_heading_list.index()
						#print rt_index
						#rl_index = evidence_heading_list.index(RL_heading)
						#print rl_index
						#sequence_index = evidence_heading_list.index()
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
						if write == 'w' and evidence_table != 1:
							#evidence_heading_list = evidence_list[0].replace('\r\n','').split('\t')
							#raw_input(heading_list)
							#raw_input(evidence_heading_list)
							header_list = []
							for e_heading in e_select_heading_list:
								header_list.append(sql_replace(e_heading))

							#evidence_write_list = ['\t'.join(evidence_entry_list)+'\r\n']

							
							#header_list = evidence_entry_list
							cmd = 'DROP TABLE IF EXISTS %s' %(table_name)
							print cmd
							cur.execute(cmd)
							sql_header_line = 'Create Table if not exists %s (%s)' %(table_name,', '.join(header_list))
							print sql_header_line
							raw_input()
							cur.execute(sql_header_line)
							evidence_table = 1
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
							evidence_entry_list = []
							for e_index in e_index_list:
								evidence_entry_list.append(evidence_line_list[e_index])

							#evidence_entry_list = [evidence_line_list[file_index],evidence_line_list[intensity_index],evidence_line_list[rt_index],evidence_line_list[rl_index],evidence_line_list[sequence_index]]
							#evidence_write_list.append('\t'.join(evidence_entry_list)+'\n')
							cmd = 'INSERT INTO %s VALUES("%s")' %(table_name,'","'.join(evidence_entry_list))
							if pe == 0:
								print cmd
								pe = 1
								print '\n'
							cur.execute(cmd)

						print 'evidence hit'
						#raw_input()
					else:
						print len(evidence_heading_list)









	file_output = False
	msScans_file_output = False
	evidence_file_output = False
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
	if msScans_file_output == True:
		write_file_name = '%s/msScans_all.txt' %(output_path)
		#print write_file_name
		write_file = open(write_file_name,write)
		write_file.writelines(scan_write_list)
		write_file.close()
		print write_file_name

	if evidence_file_output == True:
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

msScans_top = True #generates a additional msScans file last run files
msScans_top = False
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
msScans_top_file_output = False
if msScans_top_file_output == True:
	write_file_name = '%s/msScans_top.txt' %(output_path)
	#print write_file_name
	write_file = open(write_file_name,scan_write)
	write_file.writelines(scan_write_list)
	write_file.close()
	print write_file_name
#raw_input()

#raw_input()
if commit_db == True:
	con.commit()
	print 'databases committed'
run_r = False
if run_r == True:
	os.system('Rscript %s/MQ_summary.R %s' %(base_path,output_path))

