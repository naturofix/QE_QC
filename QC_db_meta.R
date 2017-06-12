library("RSQLite")
library('ggplot2')
library('reshape')
library(DT)
database_path = '/blackburn3/temp/db/Ref_QC.db'


con = dbConnect(SQLite(),dbname=database_path)
#dbDisconnect(con) 
alltables = dbListTables(con)

alltables  # list of tables in the database
for(table_name in alltables){
  print(table_name)
  fields = dbListFields(con, table_name)
  print(fields)
  print('')
}
summary = dbGetQuery( con,"select * from summary_RAW") # upload the table summary as a data frame

raw_file_list = unique(summary$Raw_file)
length(raw_file_list)
#unique_raw_files = unique(raw_file_list[duplicated(raw_file_list)])
#unique_raw_files
#for(raw_file in raw_file_list[1]){
#  cmd = paste("select * from scans WHERE Raw_file == '",raw_file,"';",sep='')
#  print(cmd)
#  scan_data = dbGetQuery(con,cmd)
#  dim(scan_data)
#}

#cmd = "select * from scans"
#print(cmd)
#scans = dbGetQuery(con,cmd)

#scans$Retention_time = as.numeric(scans$Retention_time)
#scans$Total_ion_current = as.numeric(scans$Total_ion_current)

if('summary_edited' %in% alltables){
  cmd = "select * from summary_edited"
  print(cmd)
  summary_edited = dbGetQuery(con,cmd)
  raw_list = unique(summary$Raw_file)
  edited_raws = unique(summary_edited$Raw_file)
  raw_file_list = raw_list[!raw_list %in% edited_raws]
  
}else{
  raw_file_list = unique(scans$Raw_file)
  length(raw_file_list)
  raw_file_list
  summary_edited = summary
  
}
print(raw_file_list)
print(length(raw_file_list))


if(length(raw_file_list > 0)){
  cmd = paste("select * from scans WHERE Raw_file in ('",paste(raw_file_list,collapse=("', '")),"');",sep='')
  print(cmd)
  print(raw_file_list)
  scans = dbGetQuery(con,cmd)
  scans$Retention_time = as.numeric(scans$Retention_time)
  scans$Total_ion_current = as.numeric(scans$Total_ion_current)


  for(raw_file in raw_file_list){
    #print(raw_file)
    #summary[summary$Raw_file == raw_file,]
    tic = scans$Total_ion_current[scans$Raw_file == raw_file & scans$Retention_time > 40 & scans$Retention_time < 60]
    #print(tic)
    summary$max_TIC[summary$Raw_file == raw_file] = signif(max(tic),2)
    summary$mean_TIC[summary$Raw_file == raw_file] = signif(mean(tic),2)
    summary$min_TIC[summary$Raw_file == raw_file] = signif(min(tic),2)
    
    rt = scans$Retention_time[scans$Raw_file == raw_file]
    summary$max_RT[summary$Raw_file == raw_file] = max(rt,na.rm=TRUE)
    max_rt_1e8 = max(rt[tic > 1e8],na.rm=TRUE)
    max_rt_1e9 = max(rt[tic > 1e9],na.rm=TRUE)
    
    summary$max_RT_1e8[summary$Raw_file == raw_file] = max_rt_1e8
    summary$max_RT_1e9[summary$Raw_file == raw_file] = max_rt_1e9
    
    
    #summary[summary$Raw_file == raw_file,]
    summary_edited = rbind(summary_edited,summary[summary$Raw_file == raw_file,])
    #summary_edited[summary_edited$Raw_file == raw_file,]
    print(summary_edited[summary_edited$Raw_file == raw_file,])
  }
  
  dbWriteTable(con, 'summary_edited', summary_edited, overwrite=TRUE)
}else{
  print('no difference between summary and summary_edited')
}

dbDisconnect(con) 
