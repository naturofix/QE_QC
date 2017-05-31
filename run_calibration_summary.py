import os
import sys

script_path = sys.argv[1]
base_path = sys.argv[2]
last_time = sys.argv[3]

#raw_input('run extract')
os.system('python %s/extract_log.py %s %s' %(script_path,base_path,last_time))
#raw_input('run trim')
os.system('python %s/trim.py %s' %(script_path,base_path))
#raw_input('run cal_plot')
os.system('Rscript %s/cal_plot.R %s' %(script_path,base_path))

#raw_input('run presentation')
os.system('python %s/presentation.py %s' %(script_path,base_path))
