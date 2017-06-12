library("RSQLite")
library('ggplot2')
library('reshape')
library(DT)

numeric_columns = function(df,col_num_list){
  for(col_entry in col_num_list){
    #print(col_entry)
    df[,col_entry] = as.numeric(df[,col_entry])
  }
  return(df)
}


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


summary_cmd = paste("select * from summary_RAW")
summary = dbGetQuery(con,summary_cmd)
summary = numeric_columns(summary,c(3:13))
summary$Date = as.Date(summary$Date, '%Y-%m-%d')

summary_edited_cmd = paste("select * from summary_edited")
summary_edited = dbGetQuery(con,summary_edited_cmd) 
summary_edited = numeric_columns(summary_edited,c(3:13))
summary_edited = numeric_columns(summary_edited,c(19:24))
summary_edited$Date = as.Date(summary_edited$Date, '%Y-%m-%d')

head(summary_edited)
dim(summary_edited)
colnames(summary_edited)



start_date = '2017-06-04'
recent_date = summary_edited$Raw_file[as.Date(summary_edited$Date, '%Y-%m-%d') > as.Date('2017-06-05', '%Y-%m-%d') &  as.Date(summary_edited$Date, '%Y-%m-%d') <= as.Date(as.character(Sys.Date()), '%Y-%m-%d')]
recent_date[!is.na(recent_date)]

number_of_days = 14
recent_days = summary_edited$Raw_file[as.Date(summary_edited$Date, '%Y-%m-%d') > as.Date(as.character(Sys.Date()-number_of_days), '%Y-%m-%d') &  as.Date(summary_edited$Date, '%Y-%m-%d') <= as.Date(as.character(Sys.Date()), '%Y-%m-%d')]
recent_days[!is.na(recent_days)]
recent_days_cmd = paste("recent = summary_edited$Raw_file[as.Date(summary_edited$Date, '%Y-%m-%d') > ",as.Date(as.character(Sys.Date()-number_of_days), '%Y-%m-%d')," &  as.Date(summary_edited$Date, '%Y-%m-%d') <= ",as.Date(as.character(Sys.Date()), '%Y-%m-%d'),"]")


#recent = summary_edited$Raw_file[as.Date(summary_edited$Date, '%Y-%m-%d') > as.Date(as.character(Sys.Date()-30), '%Y-%m-%d')]

summary_edited = summary_edited[order(summary_edited$Date),]
head(summary_edited)
number_of_references = 15
recent_tail = tail(summary_edited[!is.na(summary_edited$Date) &  as.Date(summary_edited$Date, '%Y-%m-%d') <= as.Date(as.character(Sys.Date()), '%Y-%m-%d'),],number_of_references)$Raw_file
recent_tail[!is.na(recent_tail)]

recent = recent_days # choose the type of selection for recent
recent_cmd = recent_days_cmd
recent = recent[!is.na(recent)]
recent # list of the most recent raw files
length(recent)

recent_mean_TIC = summary_edited$mean_TIC[summary_edited$Raw_file %in% recent]
recent_mean_TIC
boxplot(recent_mean_TIC)


TIC_per_increase = 10
min_mean_TIC = min(recent_mean_TIC) - (min(recent_mean_TIC)*TIC_per_increase/100)
min_mean_TIC
max_mean_TIC = max(recent_mean_TIC) + (max(recent_mean_TIC)*TIC_per_increase/100)
max_mean_TIC

recent_max_TIC = summary_edited$max_TIC[summary_edited$Raw_file %in% recent]
recent_max_TIC
boxplot(recent_max_TIC)

min_max_TIC = min(recent_max_TIC) - (min(recent_max_TIC)*TIC_per_increase/100)
min_max_TIC
max_max_TIC = max(recent_max_TIC) + (max(recent_max_TIC)*TIC_per_increase/100)
max_max_TIC

recent_max_RT_1e9 = summary_edited$max_RT_1e8[summary_edited$Raw_file %in% recent]
min_RT = min(recent_max_RT_1e9) - (min(recent_max_RT_1e9)*TIC_per_increase/100)
min_RT
max_RT = max(recent_max_RT_1e9) + (max(recent_max_RT_1e9)*TIC_per_increase/100)
max_RT


pep_ids = summary_edited$Peptide_Sequences[summary_edited$Raw_file %in% recent]
pep_ids
boxplot(recent_mean_TIC)

pep_per_increase = 5
min_pep = min(pep_ids) - (min(pep_ids)*pep_per_increase/100)
min_pep
max_pep = max(pep_ids) + (max(pep_ids)*pep_per_increase/100)
max_pep

#best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences >= min_pep & summary_edited$Peptide_Sequences <= max_pep & summary_edited$mean_TIC >= min_mean_TIC & summary_edited$mean_TIC >= max_mean_TIC & summary_edited$Gradient == '70']
#best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences >= min_pep & summary_edited$Peptide_Sequences <= max_pep & summary_edited$max_TIC >= min_max_TIC & summary_edited$max_TIC >= max_max_TIC & summary_edited$Gradient == '70']
best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences >= min_pep & summary_edited$Peptide_Sequences <= max_pep & summary_edited$max_TIC >= min_max_TIC & summary_edited$max_TIC >= max_max_TIC & summary_edited$max_RT_1e9 < 95]
best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences >= min_pep & summary_edited$Peptide_Sequences <= max_pep & summary_edited$max_TIC >= min_max_TIC & summary_edited$max_TIC >= max_max_TIC]

unique(best_ids[!is.na(best_ids)])
best_ids_cmd = "best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences >= min_pep & summary_edited$Peptide_Sequences <= max_pep & summary_edited$max_TIC >= min_max_TIC & summary_edited$max_TIC >= max_max_TIC & summary_edited$Gradient == '70']"


#cmd = paste("select * from evidence WHERE Raw_file in ('",paste(recent,collapse = "' ,'"),"');",sep='')

#best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences > 10000 & summary_edited$Gradient == "60"  & summary_edited$Loading == "600ng" & summary_edited$Column == 'C1']
#best_ids = summary_edited$Raw_file[summary_edited$Peptide_Sequences > 13000 & $Peptide_Sequences < 14000 & $Gradient == "70" & $Loading == "1000ng"]

#best_ids # list of the best raw file 60min gradient, 600ng on C1

#cmd = paste("select * from evidence WHERE Raw_file in ('",paste(best_ids,collapse = "' ,'"),"');",sep='')

# Previously USED
# [1] "141110_SH-Ref_70min_default_4-30_1ug"   
# [2] "141110_SH-Ref_70min_default_4-35_1ug"   
# [3] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [4] "151109_SH_Ref_G70_8_39_1ug_151110195723"
# [5] "151109_SH_Ref_G70_8_39_1ug_151110233125"
# [6] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [7] "151109_SH_Ref_G70_8_39_1ug_151111231140"
# [8] "151109_SH_Ref_G70_8_39_1ug_151112061155"
# [9] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [10] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [11] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [12] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [13] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [14] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [15] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [16] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [17] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [18] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [19] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [20] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [21] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [22] "151109_SH_Ref_G70_8_39_1ug_151111030159"
# [23] "151109_SH_Ref_G70_8_39_1ug_151111030159"

ideal_list = c("160414_C1_Ref_600ng_40C_400_8-30","160414_C2_Ref_600ng_40C_400_8-30")
ideal_list
best_ids = unique(best_ids[!is.na(best_ids)])
best_ids

best_ids_cmd = ''
best_ids =c()
best_and_recent = c(best_ids,recent,ideal_list)
best_and_recent


dups = unique(best_and_recent[duplicated(best_and_recent)])
dups
single_ref = best_and_recent[!best_and_recent %in% dups]
single_ref

unique_ref = unique(best_and_recent)


ref_list = unique_ref
ref_list
scans_cmd = paste("select * from scans WHERE Raw_file in ('",paste(ref_list,collapse = "' ,'"),"');",sep='')
print(scans_cmd)
scans = dbGetQuery(con,scans_cmd)   # scan for the raw file, can be plotted as a chromatogram
dim(scans)
colnames(scans)

scans$Retention_time = as.numeric(scans$Retention_time)
scans$Total_ion_current = as.numeric(scans$Total_ion_current)

scans$shift_TIC = scans$Total_ion_current
scans = transform(scans, shift_TIC = c(NA,shift_TIC[-nrow(scans)]))
scans$TIC_variance = ((scans$Total_ion_current-scans$shift_TIC)/scans$shift_TIC) * 100

# ggplot(data = scans, aes(x=Retention_time,y=Total_ion_current,colour=Raw_file)) +
#   ylim(1e8,1e10) +
#   xlim(10,80) +
#   geom_line(size = 0.3, alpha = 1)



evidence_cmd = paste("select * from evidence WHERE Raw_file in ('",paste(ref_list,collapse = "' ,'"),"');",sep='')
print(evidence_cmd)
evidence = dbGetQuery(con,evidence_cmd)   # extract the evidence for the selected list of raw files
dim(evidence)
colnames(evidence)
#evidence = evidence_query







# remove NA values and intensities below 1e5
evidence$Intensity = as.numeric(evidence$Intensity)
#evidence$Intensity
evidence = evidence[!is.na(evidence$Intensity),]
dim(evidence)
#evidence = evidence[as.numeric(evidence$Intensity) > 1e5,]
#dim(evidence)

evidence = numeric_columns(evidence,c(4:7))

# num_list = colnames(evidence)[c(3,4,5,6)]
# num_list
# for(col_entry in num_list){
#   print(col_entry)
#   evidence[,col_entry] = as.numeric(evidence[,col_entry])
# }

seq_evidence = evidence[,c("Raw_file","Sequence","Intensity")]
seq_evidence$Intensity = as.numeric(seq_evidence$Intensity)
head(seq_evidence)

seq_max = cast(seq_evidence,Sequence~Raw_file, function(x) max(x,na.rm=TRUE))

head(seq_max)
evidence[evidence$Sequence =='AAAAAAAAAAAAAAAGAGAGAK',]
do.call(data.frame,lapply(seq_max, function(x) replace(x, is.infinite(x),NA)))
rownames(seq_max) = seq_max[,1]
colnames(seq_max)

seq_max[,1] = NULL



dump(list = c('alltables','recent','best_ids','ideal_list','recent_cmd','summary_cmd','summary_edited_cmd','scans_cmd','evidence_cmd'), file = "/mnt/BLACKBURNLAB/QC/Reference/summary/QC_db_cmd.R")
save(summary,file = "/mnt/BLACKBURNLAB/QC/Reference/summary/summary_db.rda")
save(summary_edited,file = "/mnt/BLACKBURNLAB/QC/Reference/summary/summary_edited_db.rda")
save(scans,file = "/mnt/BLACKBURNLAB/QC/Reference/summary/scans_db.rda")
save(evidence,file = "/mnt/BLACKBURNLAB/QC/Reference/summary/evidence_db.rda")
save(seq_max,file = "/mnt/BLACKBURNLAB/QC/Reference/summary/seq_max_db.rda")


save.image('/mnt/BLACKBURNLAB/QC/Reference/summary/QC_db_sim.RData')

