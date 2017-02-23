
#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

output_folder = '/home/sgarnett/Downloads/'
#output_folder = '/Users/sgarnett/Downloads/summary/'
#output_folder = '/mnt/BLACKBURNLAB/QC/Reference/summary/'

output_folder = args[1]

#system(paste('mkdir',output_folder))
raw = read.table(paste(output_folder,'summary_RAW.txt',sep='/'),sep ='\t',header = TRUE, stringsAsFactors = TRUE)
colnames(raw)
dim(raw)
extract_date_function = function(raw_file_name){
  year_list = c('13','14','15','16')
  ##print(raw_file_name)
  first_six = unlist(substr(raw_file_name, 1, 6))
  #print(first_six[1])
  names(first_six) = NULL
  if(!is.na(as.numeric(first_six))){
    if(substr(first_six,1,2) %in% year_list){
      date = first_six
      date = as.character(as.Date(first_six, '%y%m%d'))
    }else{
      date = NA
    }
    
  }else{
    date = NA
  }
  #date
}


date_expr_function = function(raw_file){
  #print(raw_file)
  raw_file
  date_pattern = '[0-9]{6}'
  short_date = regmatches(raw_file, regexpr(date_pattern, raw_file))
  long_date_pattern = '[0-9]{12}'
  long_date = regmatches(raw_file, regexpr(long_date_pattern, raw_file))
  column_pattern = 'C[0-9]{1}'
  column_pattern
  column = regmatches(raw_file, regexpr(column_pattern, raw_file))
  #print(long_date)
  #print(length(long_date))
  if(length(long_date) > 0){
    date = substr(long_date, 1, 6)
    date = as.character(as.Date(date, '%y%m%d'))
  }else{
    if(length(short_date > 0)){
      date = short_date
      date = as.character(as.Date(date, '%y%m%d'))
    }else{
      #print(raw_file)
      date = NA
    }
  }
  #print(short_date)
  #print(column)
  #print('')
  #date
}

date_collapse_function = function(date,last_date,days){
  #print(date)
  #print(strsplit(date,'-'))
  #print(last_date)
  date = as.Date(date, "%Y-%m-%d")
  #print(last_date)
  #print(as.Date(last_date, '%Y-%m-%d'))
  m3 = as.Date(last_date, '%Y-%m-%d') - 30
  #m3 = last_date - days
  #print(m3)
  if(Sys.Date()-30 > date){
    #print('hit')
    new_date = as.character(format(date, '%Y-%m'))
  }else{
    new_date = as.character(date)
  }
}

column_expr_function = function(raw_file){
  #print(raw_file)
  raw_file
  column_pattern = 'C[0-9]{1}'
  column_pattern
  column = regmatches(raw_file, regexpr(column_pattern, raw_file))
  if(length(column) > 0){
    column_name = column
  }else{
    column_name = ''
  }
  #column_name

}

gradient_expr_function = function(raw_file){
  #print(raw_file)
  raw_file
  gradient_pattern = '([0-9]{2,3}min)'
  column = regmatches(raw_file, regexpr(gradient_pattern, raw_file))
  column
  if(length(column) > 0){
    g = unlist(strsplit(column,'min'))[1]
    gradient = g
    
  }else{
    method_pattern = '(G[0-9]{2,3})'
    method = regmatches(raw_file, regexpr(method_pattern, raw_file))
    method
    if(length(method) > 0){
      m = unlist(strsplit(method,'G'))[2]
      gradient = m
    }else{
    #print(unlist(raw_file))
      gradient = NA
    }
  }
  #gradient
  #print(column_name)
  #print('')
}

load_volume_expr_function = function(raw_file){
  #print(raw_file)
  raw_file
  gradient_pattern = '([0-9]{2,4}ng)'
  column = regmatches(raw_file, regexpr(gradient_pattern, raw_file))
  column

  if(length(column) > 0){
    g = unlist(column)[1]
    gradient = g
    
  }else{
    method_pattern = '([0-9]{1,3}ug)'
    method = regmatches(raw_file, regexpr(method_pattern, raw_file))
    method
    if(length(method) > 0){
      m = unlist(strsplit(method,'ug'))[1]
      if(as.numeric(m) > 10){
        m = unlist(method)[1]
        gradient = NA
      }else{
        gradient = paste(as.numeric(m)*1000,'ng',sep='')
      }
    }else{
      #print(unlist(raw_file))
      gradient = NA
    }
  }
  #gradient
  #print(column_name)
  #print('')
  if(!is.na(gradient)){
    #print(gradient)
    r = unlist(strsplit(gradient,'ng'))[1]
    #print(r)
    if(as.numeric(r) > 1000){
      gradient = '>1000ng'
      gradient = ''
    }
    if(as.numeric(r) < 600){
      gradient = '<600ng'
      gradient = ''
    }
  }else{
    gradient = ''
  }
  gradient
}


gradient_list = sapply(raw$Raw.file, function(x) invisible(gradient_expr_function(x)))
gradient_list


date_list = sapply(raw$Raw.file, function(x) invisible(date_expr_function(x)))
date_list

#ERROR HERE
#date_object <- as.POSIXct(date_list)
#date_object
#month_list = sapply(date_object, function(x) strftime(x, '%Y-%m'))
#month_list

#temp fix
month_list = date_list

                    
column_list = sapply(raw$Raw.file, function(x) invisible(column_expr_function(x)))
column_list

volume_list = sapply(raw$Raw.file, function(x) invisible(load_volume_expr_function(x)))
volume_list


raw$extracted_date = date_list
raw$month = month_list
raw$column = column_list
raw$gradient = gradient_list
raw$volume = volume_list
raw$column_volume = paste(raw$column,raw$volume)
dim(raw)





columns_added = 7


#raw$extracted_date_name = date_name_list
date = raw[!is.na(raw$extracted_date),]
dim(date)

print(date$extracted_date)
date = date[as.Date(date$extracted_date, '%Y-%m-%d') <= as.Date(Sys.Date(), '%Y-%m-%d'),]
dim(date)
head(date)
colnames(date)
#print(date$extracted_date)
date_list = date$extracted_date
#print(date_list)
print(max(date_list,na.rm=TRUE))
last_date = max(date_list,na.rm=TRUE)
print(last_date)


collapse_date_list = sapply(date_list, function(x) date_collapse_function(x,last_date,30))
#print(collapse_date_list)
#error
date$date_collapse = collapse_date_list

date_order = date[order(date$extracted_date),]

library(ggplot2)
last = 400
reduced_data = date_order[c((dim(date_order)[1]-last):dim(date_order)[1]),]
dim(reduced_data)
column_name = 'Peptide.Sequences.Identified'
  #print(column_name)
  #column_name = 'Peptide.Sequences.Identified'
  C1_max = C2_max = C1_min = C2_min = 0
  C1_mean = mean(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C1 600ng'],na.rm=T)
  C1_max = max(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C1 600ng'],na.rm=T)
  C1_min = C1_max * 80 / 100
  C2_max = max(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C2 600ng'],na.rm=T)
  C2_mean = mean(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C2 600ng'],na.rm=T)
  C2_min = C2_max * 80 / 100
  cmd = paste('q <- qplot(date_collapse,',column_name,',data=reduced_data,geom=c("boxplot","point"),colour = column_volume)')
  #print(cmd)
  try(eval(parse(text=cmd)))
  try(print(q + theme(axis.text.x = element_text(angle = 90, hjust = 1))+ ggtitle(column_name)+ geom_hline(yintercept=C1_mean, col = 'greenyellow') + geom_hline(yintercept=C2_mean, col = 'magenta') + geom_hline(yintercept=C1_max, col = 'green') + geom_hline(yintercept=C1_min, col = 'lightgreen') + geom_hline(yintercept=C2_max, col = 'red') + geom_hline(yintercept=C2_min, col = 'lightcoral')))

  file_name = paste(output_folder,'/',column_name,'_month_last_',last,'.png',sep='')
  #print(file_name)
  try(ggsave(file_name, plot = last_plot()))
  file_name = paste(output_folder,'/',column_name,'_email.png',sep='')
  #print(file_name)
  try(ggsave(file_name, plot = last_plot()))

#  q = ggplot(date_order[c(length(date_order$date_collapse)-400:length(date_order$date_collapse)),],
#        aes(date_collapse, Peptide.Sequences.Identified)) + 
#   geom_boxplot(aes(colour = column_volume)) +
#   theme(text = element_text(size=15),axis.text.x = element_text(angle = 90, hjust = 1)) +
#   labs(x = NULL, y = NULL)
# print(q)
# file_name = paste(output_folder,'/Peptides_Identified.png',sep='')
# print(file_name)
# try(ggsave(file_name, plot = last_plot()))
#plot(date_order$extracted_date,date_order$Peptide.Sequences.Identified,cex = 0.2,pch = 19,names.arg = date_order$extracted_date)
#plot(date_order$extracted_date,date_order$MS.MS,cex = 0.2,pch = 19,xlim = c(1000,15000))
#plot(date_order$Peptide.Sequences.Identifiedcex = 0.2,pch = 19)




# library(ggplot2)
# 
# dim(date_order)
# colnames(date_order)
# q <- qplot(extracted_date,Peptide.Sequences.Identified,data=date_order,geom="boxplot",colour = gradient,fill=column_volume)
# q + theme(axis.text.x = element_text(angle = 90, hjust = 1))
# q <- qplot(month,Peptide.Sequences.Identified,data=date_order,geom="boxplot",colour = gradient,fill=column_volume)
# q + theme(axis.text.x = element_text(angle = 90, hjust = 1))
# 
# 
# for(column_name in colnames(date_order)[4:(length(colnames(date_order))-columns_added)]){
#   #print(column_name)
#   #column_name = 'Peptide.Sequences.Identified'
#   cmd = paste('q <- qplot(extracted_date,',column_name,',data=date_order,geom=c("boxplot","point"),colour=column_volume)')
#   #print(cmd)
#   try(eval(parse(text=cmd)))
#   try(print(q + theme(axis.text.x = element_text(angle = 90, hjust = 1))+ ggtitle(column_name)))
#   file_name = paste(output_folder,'/',column_name,'.png',sep='')
#   #print(file_name)
#   try(ggsave(file_name, plot = last_plot()))
# }
# 
# for(column_name in colnames(date_order)[4:(length(colnames(date_order))-columns_added)]){
#   #print(column_name)
#   #column_name = 'Peptide.Sequences.Identified'
#   cmd = paste('q <- qplot(date_collapse,',column_name,',data=date_order,geom=c("boxplot","point"),colour = column_volume)')
#   #print(cmd)
#   try(eval(parse(text=cmd)))
#   try(print(q + theme(axis.text.x = element_text(angle = 90, hjust = 1))+ ggtitle(column_name)))
#   file_name = paste(output_folder,'/',column_name,'_month.png',sep='')
#   #print(file_name)
#   try(ggsave(file_name, plot = last_plot()))
# }
# 
# last = 100
# min_pep = 5000
# reduced_data = date_order[date_order$Peptide.Sequences.Identified > min_pep,]
# 
# reduced_data = reduced_data[c((dim(reduced_data)[1]-last):dim(reduced_data)[1]),]
# dim(reduced_data)
# colnames(reduced_data)
# 
# #dim(reduced_data)
# #q <- qplot(extracted_date,Peptide.Sequences.Identified,data=reduced_data,geom="boxplot",colour = column_volume)
# #q + theme(axis.text.x = element_text(angle = 90, hjust = 1))
# 
# 
# for(column_name in colnames(reduced_data)[4:(length(colnames(reduced_data))-columns_added)]){
#   #print(column_name)
#   #column_name = 'Peptide.Sequences.Identified'
#   cmd = paste('q <- qplot(extracted_date,',column_name,',data=reduced_data,geom=c("boxplot","point"),colour = column_volume)')
#   #print(cmd)
#   try(eval(parse(text=cmd)))
#   try(print(q + theme(axis.text.x = element_text(angle = 90, hjust = 1))+ ggtitle(column_name)))
# 
#   file_name = paste(output_folder,'/',column_name,'_last_',last,'.png',sep='')
#   #print(file_name)
#   try(ggsave(file_name, plot = last_plot()))
# }
# 
# 
# last = 200# no larger than 500
# min_pep = 5000
# reduced_data = date_order[date_order$Peptide.Sequences.Identified > min_pep,]
# 
# reduced_data = reduced_data[c((dim(reduced_data)[1]-last):dim(reduced_data)[1]),]
# dim(reduced_data)
# colnames(reduced_data)
# for(column_name in colnames(reduced_data)[4:(length(colnames(reduced_data))-columns_added)]){
#   #print(column_name)
#   #column_name = 'Peptide.Sequences.Identified'
#   C1_max = C2_max = C1_min = C2_min = 0
#   C1_mean = mean(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C1 600ng'],na.rm=T)
#   C1_max = max(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C1 600ng'],na.rm=T)
#   C1_min = C1_max * 80 / 100
#   C2_max = max(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C2 600ng'],na.rm=T)
#   C2_mean = mean(reduced_data[,column_name][reduced_data[,'column_volume'] == 'C2 600ng'],na.rm=T)
#   C2_min = C2_max * 80 / 100
#   cmd = paste('q <- qplot(date_collapse,',column_name,',data=reduced_data,geom=c("boxplot","point"),colour = column_volume)')
#   #print(cmd)
#   try(eval(parse(text=cmd)))
#   try(print(q + theme(axis.text.x = element_text(angle = 90, hjust = 1))+ ggtitle(column_name)+ geom_hline(yintercept=C1_mean, col = 'greenyellow') + geom_hline(yintercept=C2_mean, col = 'magenta') + geom_hline(yintercept=C1_max, col = 'green') + geom_hline(yintercept=C1_min, col = 'lightgreen') + geom_hline(yintercept=C2_max, col = 'red') + geom_hline(yintercept=C2_min, col = 'lightcoral')))
#   
#   file_name = paste(output_folder,'/',column_name,'_month_last_',last,'.png',sep='')
#   #print(file_name)
#   try(ggsave(file_name, plot = last_plot()))
#   file_name = paste(output_folder,'/',column_name,'_email.png',sep='')
#   #print(file_name)
#   try(ggsave(file_name, plot = last_plot()))
#  
# }

 save.image('/mnt/BLACKBURNLAB/QC/Reference/summary/QC.RData') 
