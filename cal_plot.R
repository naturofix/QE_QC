#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)


library(ggplot2)
getwd()
base_path = args[1]
extract_path = paste(base_path,'extract_log',sep='/')

test_type_list = c('calibration','evaluation','tune') 
test_type_list = test_type_list
for(test_type in test_type_list){

  file_path = paste(extract_path,test_type,sep='/')
  print(file_path)
  output_path = paste(base_path,'/',test_type,'_plots',sep='')
  #system(paste('rm -r',output_path))
  system(paste('mkdir',output_path))
  file_list = list.files(file_path)
  print(file_list)
  print(file_list)
#}
#  run = FALSE
#if(run == TRUE){
  error_list = c()
  for(file_name in file_list){
    print(file_name)
    
    cal = 0
    #cal = read.table(paste(file_path,file_name,sep='/'),sep ='\t',header = FALSE, stringsAsFactors = TRUE)
    cmd = paste("cal = read.table('",file_path,"/",file_name,"',sep ='\t',header = FALSE, stringsAsFactors = FALSE)",sep='')
    #print(cmd)
    try(eval(parse(text=cmd)))
    #print(head(cal))
    if(!grepl('neg',file_name)){
    if(cal != 0){
      print('hit')
    
      #print(colnames(cal))
      #print(dim(cal))
      #print(head(cal))
      #print(cal$V1[1])
      #cal$V5 = as.numeric(cal$V5)
      #print(head(cal))
      cal$date = as.Date(cal$V1, '%Y-%m-%d')
      #print(date)
      
      date_collapse_function = function(date,last_date){
        #print(date)
        #print(strsplit(date,'-'))
        #print(last_date)
        m3 = as.Date(last_date, '%Y-%m-%d') - 90
        if(m3 > date){
          #print('hit')
          new_date = as.character(format(date, '%Y-%m'))
        }else{
          new_date = as.character(date)
        }
      }
      
      date = cal$date[1]
      last_date = cal$date[length(cal$date)]
      cal$date_summary = sapply(cal$date, function(x) date_collapse_function(x,last_date))
      #print(cal$date_summary)
      #error
      
      run = TRUE
      if(run == TRUE){
      print(colnames(cal))
      last_num = length(colnames(cal))-2
      print(last_num)
      reduced_colnames = colnames(cal)[c(5:last_num)]
      print(reduced_colnames)
      property = cal[dim(cal)[1],'V4']
      print(property)
      for(column_name in reduced_colnames){
        print(column_name)
        cal[,column_name] = as.numeric(cal[,column_name])
        cmd = paste('q <- qplot(date_summary,',column_name,',data=cal,geom=c("boxplot","point"))')
        print(cmd)
        try(eval(parse(text=cmd)))
        #try(q + theme(position = position_jitter(width = 0.2)))
        #try(q + )
        try(q + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + ggtitle(expression(atop(file_name, atop(property,'')))))
        
        cmd = paste("q + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + ggtitle(expression(atop('",file_name,"', atop('",property,"',''))))",sep='')
        print(cmd)
        eval(parse(text=cmd))
        #try(q + scale_x_continuous(breaks = 100))
        plot_file_name = paste(output_path,'/',file_name,'_',column_name,'_.png',sep='')
        print(plot_file_name)
        try(ggsave(plot_file_name, plot = last_plot()))
      }
      }
    }else{
      print('error')
      error_list = c(error_list,file_name)
    }
    }
      
  }
  print(error_list)
}
