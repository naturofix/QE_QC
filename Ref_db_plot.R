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

summary = dbGetQuery( con,"select * from summary_RAW WHERE Date != ''" ) # upload the table summary as a data frame
head(summary)
dim(summary)
colnames(summary)

num_list = colnames(summary)[c(3:13)]
num_list
for(col_entry in num_list){
  print(col_entry)
  summary[,col_entry] = as.numeric(summary[,col_entry])
}

summary$Date = as.Date(summary$Date, '%Y-%m-%d')

recent = summary$Raw_file[as.Date(summary$Date, '%Y-%m-%d') > as.Date('2017-05-15', '%Y-%m-%d') &  as.Date(summary$Date, '%Y-%m-%d') < as.Date('2017-06-01', '%Y-%m-%d')]
recent # list of the most recent raw files
length(recent)

cmd = paste("select * from evidence WHERE Raw_file in ('",paste(recent,collapse = "' ,'"),"');",sep='')

best_ids = summary$Raw_file[summary$Peptide_Sequences > 10000 & summary$Gradient == "60"  & summary$Loading == "600ng" & summary$Column == 'C1']
best_ids = summary$Raw_file[summary$Peptide_Sequences > 13000 & summary$Peptide_Sequences < 14000 summary$Gradient == "70" & summary$Loading == "1000ng"]

best_ids # list of the best raw file 60min gradient, 600ng on C1

cmd = paste("select * from evidence WHERE Raw_file in ('",paste(best_ids,collapse = "' ,'"),"');",sep='')

best_and_recent = c(best_ids,recent)
best_and_recent


cmd = paste("select * from scans WHERE Raw_file in ('",paste(best_and_recent,collapse = "' ,'"),"');",sep='')
print(cmd)
scans = dbGetQuery(con,cmd)   # scan for the raw file, can be plotted as a chromatogram
dim(scans)
colnames(scans)

scans$Retention_time = as.numeric(scans$Retention_time)
scans$Total_ion_current = as.numeric(scans$Total_ion_current)

# ggplot(data = scans, aes(x=Retention_time,y=Total_ion_current,colour=Raw_file)) +
#   ylim(1e8,1e10) +
#   xlim(10,80) +
#   geom_line(size = 0.3, alpha = 1)



cmd = paste("select * from evidence WHERE Raw_file in ('",paste(best_and_recent,collapse = "' ,'"),"');",sep='')
print(cmd)
evidence = dbGetQuery(con,cmd)   # extract the evidence for the selected list of raw files
dim(evidence)
colnames(evidence)
#evidence = evidence_query







# remove NA values and intensities below 1e5
evidence$Intensity = as.numeric(evidence$Intensity)
evidence$Intensity
evidence = evidence[!is.na(evidence$Intensity),]
dim(evidence)
evidence = evidence[as.numeric(evidence$Intensity) > 1e5,]
dim(evidence)

num_list = colnames(evidence)[c(3,4,5,6)]
num_list
for(col_entry in num_list){
  print(col_entry)
  evidence[,col_entry] = as.numeric(evidence[,col_entry])
}








save.image('/mnt/BLACKBURNLAB/QC/Reference/summary/QC_db.RData')



########### VENN ##############
library(VennDiagram)
raw_list = unique(evidence$Raw_file)
raw_list

setA = unique(evidence$Sequence[evidence$Raw_file == raw_list[1]])
setB = unique(evidence$Sequence[evidence$Raw_file == raw_list[2]])
setC = unique(evidence$Sequence[evidence$Raw_file == raw_list[3]])

#plot triple Venn

draw.triple.venn(length(setA),
                 length(setB), 
                 length(setC), 
                 n12 = length(intersect(setA,setB)), #overlap between A & B
                 n23 = length(intersect(setB,setC)), #overlap between B & C
                 n13 = length(intersect(setA,setC)), #overlap between A & C
                 n123 = length(intersect(intersect(setA,setB), intersect(setB,setC))), #overlap between all 3
                 category = c("setA", "setB", "setC"),
                 #rotation = 1, #default, indicates clockwise rotation of the sets
                 #reverse = TRUE, #binary: should diagram be mirrored along vertical axis
                 euler.d = TRUE, #binary: draw Euler diagrams (Venns with moveable circles) when conditions are met?
                 scaled = TRUE, #binary: scale circles according to set size? (requires euler.d=T) 
                 overrideTriple = 1, #assign any value to re-enable general scaling for three-set Venns (may be visually misleading)
                 lwd = rep(0, 3), #width of circumferences
                 lty = rep("blank", 3), #dash pattern of circumference outline
                 #col = c("cadetblue2","thistle","khaki3"), #colour of circumferences
                 fill = c("#66C2A5","#3288BD","#5E4FA2"), #fill colours (can also specify as rep("colourname",3) or as c("colourname1","colourname2","colourname3"))
                 alpha = rep(0.5, 3), #transparency
                 label.col = rep("black", 7), #area label colour 
                 cex = rep(1, 7), #area label size
                 fontface = rep("plain", 7),
                 fontfamily = rep("serif", 7), 
                 cat.pos = c(-40, 40, 180), #position (in degrees of circle) of category names
                 cat.dist = c(0.05, 0.05, 0.025), #distance of category names from edges of circle
                 cat.col = rep("black", 3), #colours of cat names
                 cat.cex = rep(1, 3), #size of cat names
                 cat.fontface = rep("plain", 3),
                 cat.fontfamily = rep("serif", 3),
                 cat.just = list(c(0.5, 1), c(0.5, 1), c(0.5, 0)), #horizontal and vertical justification of each category name
                 cat.default.pos = "outer", #default location of category names
                 cat.prompts = FALSE, 
                 rotation.degree = 0, #no. degrees to rotate entire diagram
                 rotation.centre = c(0.5, 0.5), #indicates rotation centre
                 ind = TRUE, #binary: first draw diagram, then return gList object?
                 sep.dist = 0.05, #distance between circles if sets mutually exclusive
                 offset = 0) #offset from centre if inclusive sets







# select sequences from a specific retention time
Retention_time_start = 20
Retention_time_windown = 5
Retention_time_stop = Retention_time_start+Retention_time_windown
sequences = evidence$Sequence[evidence$Retention_time > Retention_time_start & evidence$Retention_time < Retention_time_stop]
length(sequences)

# arrange sequences with those found most often at the top
# sequences seem to be present multiple times per sample : need to work out why
seq_num = table(sequences)
head(seq_num)
seq_num = seq_num[rev(order(seq_num))]
head(seq_num)
#plot(seq_num)


a = 20
b = 3
# boxplot of sequence intensites coloured by raw file
# running the section below allows you to move slowly through differen peptides
c = a+b
top_seq = evidence[evidence$Sequence %in% names(seq_num)[c(a:c)],]
ggplot(data = top_seq, aes(x=Sequence,y=Intensity,colour=Raw_file)) +
  geom_boxplot(size = 0.75, alpha = 1)+ geom_point()
a = c






###### Everything below here is chaos ###################

ev_var = aggregate(Intensity ~ Sequence + Raw_file, data = evidence, function(x) c(mean = mean(x), counts = length(x), var = var(x), sd = sd(x)))
plot(ev_var$Intensity[,'var'])
ev = as.matrix(ev_var)
ev_var$var = ev_var$Intensity[,'var']
ggplot(data = ev_var, aes(x=Sequence,y=var,colour=Raw_file)) +
  geom_point(size = 0.75, alpha = 1)+ geom_line()
theme(legend.text=element_text(size=0.2))





top_seq = evidence[evidence$Sequence %in% names(seq_num[seq_num > 100]),]
ggplot(data = top_seq, aes(x=Sequence,y=Intensity,colour=Raw_file)) +
  geom_boxplot(size = 0.75, alpha = 1)+
  ylim(1e8,1e10) +
  ylim(1e8,1e9) +
  theme(legend.text=element_text(size=X))



plot(top_seq$Retention_time,top_seq$Intensity,type='l')

a = 50
b = 10
c = a+b
top_seq = evidence[evidence$Sequence %in% names(seq_num)[c(a:c)],]
ggplot(data = top_seq, aes(x=Sequence,y=Intensity,colour=Raw_file)) +
  geom_boxplot(size = 0.75, alpha = 1) +
 theme(legend.text=element_text(size=0.2))
  ylim(1e8,1e9)
a = c

a = 50
b = 0.1
c = a+b
top_seq = evidence[evidence$Retention_time >a & evidence$Retention_time < c,]

dim(top_seq)
ggplot(data = top_seq, aes(x=Sequence,y=Intensity,colour=Raw_file)) +
  geom_boxplot(size = 0.75, alpha = 1) +
  theme(legend.text=element_text(size=0.2))
ylim(1e8,1e9)
a = c

#geom_line(data = scans[scans$Raw.file %in% #raw_list[input$file_range[1]:input$file_range[2]],],
geom_line(data = scans[scans$Raw.file %in% input$file,],
          aes(x=Retention.time,y=Total.ion.current,colour=Raw.file),size = 0.3)


cmd = "select Sequence from evidence"
sequences = dbGetQuery(con,cmd)
sequences = evidence$Sequence
dim(sequences)
length(sequences)
seq_num = table(sequences)
head(seq_num)
seq_num = seq_num[rev(order(seq_num))]
head(seq_num)
plot(seq_num)

cmd = "select Intensity from evidence WHERE Sequence == 'AGLQFPVGR' and Intensity > 5000"
intensity = dbGetQuery(con,cmd)
length(intensity)
plot(intensity)
intensity = (as.numeric(as.matrix(intensity)))
intensity = intensity[!is.na(intensity)]
intensity = intensity[intensity > 1e8]
hist(intensity,breaks = 100)
evidence = as.matrix(evidence)
for(entry in names(seq_num[c(1:10)])){
  ref = evidence$Raw_file[evidence$Sequence == entry]
  plot(as.numeric(evidence$Intensity[evidence$Sequence == entry]),main=entry)
}

