import os
import sys
import subprocess

base_path = sys.argv[1]
tex_path = os.path.join(base_path,'tex')
os.system('mkdir %s' %(tex_path))
latex_list = []

def latex_name(name):
	sub_list = ['"',"'",')','(','/','_','?']
	for sub in sub_list:
		name = name.replace(sub,' ')
	return name




start_latex_line = """
\\documentclass{beamer}
% Load a theme ( graphics , colors , . . . ) for the presentation
\\usepackage{beamerthemesplit}
\\usepackage{graphicx}
\\usepackage{grffile}

\\date{\\today}
 
\\begin{document}


"""



end_latex_line = """

\\end{document}
"""
#base_path = '/blackburn3/scripts/QC/'

latex_list.append(start_latex_line)


##### ADD MQ Reference Images ######## created using the MQ_summary script
print '\n\nImporting MQ images\n'
MQ_path = '/mnt/BLACKBURNLAB/QC/Reference/summary/'
file_list = os.listdir(MQ_path)
file_list.sort()
for file_name in file_list:
	if '_month.png' in file_name:
		print file_name
		slide_title = latex_name(file_name.replace('_month.png',''))
		slide_title = 'Reference : MQ : %s' %(slide_title) 
		latex_list.append('\\frame{\n')
		latex_list.append('\\frametitle{%s}\n' %(slide_title))
		latex_list.append('\\center')
		latex_list.append('\\begin{figure}')
		latex_list.append('\\centering')
		latex_list.append('\\includegraphics[width = 0.7\\textwidth]{%s/%s}\n' %(MQ_path,file_name))
		latex_list.append('\\end{figure}')
		latex_list.append('}\n')


################ ADD disk space info #################

print '\n\nAssessing disk space\n'
cmd = 'du -sh /mnt/BLACKBURNLAB/* > %s/du_BLACKBURNLAB.txt &' %(base_path)
print(cmd)
os.system(cmd)

file_name = '%s/du_BLACKBURNLAB.txt' %(base_path)
print(file_name)
read_file = open(file_name,'r')
read_list = read_file.readlines()
read_file.close()
item_list = []
item_list.append('\\frame{\n')
item_list.append('\\frametitle{BLACKBURNLAB Research Data Disk Usage}\n')

item_list = []
item_list.append('\\begin{itemize}\n')
#latex_list.append('\\tiny')
for line in read_list:
	print line
	if line[0].isdigit():
		line = line.replace('%','\\%').replace('$','')
		print [line]
		item_list.append('\\tiny{\\item %s}\n' %(line))


#output = subprocess.check_output("cat du -sh /mnt/BLACKBURNLAB/", shell=True)
#latex_list.append('\\tiny{\\item %s}' %(ouput.replace('%','\\%')))
item_list.append('\\end{itemize}\n')
#latex_list.append('\\normalsize')
item_list.append('}\n')
if len(item_list) > 4:
	latex_list = latex_list + item_list


####### ERRORS and WARNINGS ###########
print '\n\nQE errors and warning\n'

error_files = ['error','warning']
for error_name in error_files:
	error_file_name = error_name+'.txt'
	error_path = os.path.join(base_path,'extract_log',error_file_name)
	read_file = open(error_path,'r')
	read_list = read_file.readlines()
	read_file.close()
	new_read_list = []



	for read_line in read_list:
		read_line_list = read_line.split('\t')
		new_read_list.append('\t'.join([read_line_list[0],read_line_list[2]]))

	read_list = list(set(new_read_list))
	read_list.sort()

	

	last_length = -15
	last_lines = read_list[last_length:]
	#print(last_lines)
	item_list = []
	item_list.append('\\frame{\n')
	item_list.append('\\frametitle{QE : %s}\n' %(error_name))
	
	item_list.append('\\begin{itemize}\n')
	#latex_list.append('\\tiny')
	for line in last_lines:
		item_list.append('\\tiny{\\item %s}\n' %(line.replace('%','\\%')))
	item_list.append('\\end{itemize}\n')
	#latex_list.append('\\normalsize')
	item_list.append('}\n')
	if len(item_list) > 4:
		latex_list = latex_list + item_list


##### TUNE, CALIBRATION AND EVALUATION ##############

print '\n\n TUNE CALIBRATION AND EVALUATION \n'
type_list = ['tune','cal','eval']
path_dic = {}
path_dic['tune'] = 'tune_plots'
path_dic['cal'] = 'calibration_plots'
path_dic['eval'] = 'evaluation_plots'

for type_entry in type_list:
	print(type_entry)
	#type_entry = plot_path_entry.replace('_plots','')
	end_file_name = '%s_end.txt' %(type_entry)
	end_path = os.path.join(base_path,end_file_name)
	read_file = open(end_path,'r')
	read_list = read_file.readlines()
	read_file.close()

	read_list = list(set(read_list))
	read_list.sort()
	

	last_length = -15
	last_lines = read_list[last_length:]
	#print(last_lines)
	item_list = []
	item_list.append('\\frame{\n')
	item_list.append('\\frametitle{%s}\n' %(type_entry))
	
	item_list.append('\\begin{itemize}\n')
	#latex_list.append('\\tiny')
	for line in last_lines:
		item_list.append('\\tiny{\\item %s}\n' %(line.replace('%','\\%')))
	item_list.append('\\end{itemize}\n')
	#latex_list.append('\\normalsize')
	item_list.append('}\n')
	if len(item_list) > 4:
		latex_list = latex_list + item_list

		

#run = False
#if run == True:
	plot_path_entry = path_dic[type_entry]
	plot_path = os.path.join(base_path,plot_path_entry)
	#plot_path = 'tune_plots'
	file_list = os.listdir(plot_path)
	file_list.sort()
	for file_name in file_list:
		if '.txt' in file_name:
			new_file_name = file_name.replace(' ','_')
			#cmd = 'mv %s/%s %s/%s' %(plot_path,file_name,plot_path,new_file_name)
			#print(cmd)
			#os.system(cmd)
			#raw_input()
			print file_name
			slide_title = latex_name(file_name)
			slide_title = '%s : %s' %(plot_path_entry.replace('_plots',''),slide_title[:slide_title.index('.txt')]) 
			latex_list.append('\\frame{\n')
			latex_list.append('\\frametitle{%s}\n' %(slide_title))
			latex_list.append('\\center\n')
			latex_list.append('\\begin{figure}\n')
			latex_list.append('\\centering\n')
			latex_list.append('\\includegraphics[width = 0.7\\textwidth]{%s/%s}\n' %(plot_path,file_name))
			latex_list.append('\\end{figure}\n')
			latex_list.append('}\n')
		



latex_list.append(end_latex_line)
#for latex_line in latex_list:
#	print latex_line
file_name = os.path.join(tex_path,'calibration.tex')
write_file = open(file_name,'w')
write_file.writelines(latex_list)
write_file.close()



os.system('pdflatex %s' %(file_name))

os.system('mv %s %s' %('calibration.pdf',os.path.join(base_path,'calibration.pdf')))
