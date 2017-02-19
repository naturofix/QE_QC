import os
import sys

script_path = sys.argv[1]
base_path = sys.argv[2]

os.system('python %s/extract_log.py %s' %(script_path,base_path))
os.system('python %s/trim.py %s' %(script_path,base_path))
os.system('Rscript %s/cal_plot.R %s' %(script_path,base_path))

os.system('python %s/presentation.py %s' %(script_path,base_path))
