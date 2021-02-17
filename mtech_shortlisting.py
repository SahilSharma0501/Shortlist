from zipfile import ZipFile
from pathlib import Path
import os
import sys
import datetime
x=datetime.datetime.now()
yearGiven=sys.argv[1]
current_year = int(yearGiven)
from csv import DictReader,DictWriter
validDegree=[]
validSubject=[]
remarks_list=[]

with open('Test/Include/'+'MTech_137_n_degree_or_examination.csv','r',encoding='utf-8') as rf:
    read=DictReader(rf)
    for row in read:
        isValid=row['Valid'].lower()
        degree=row['137_n_degree_or_examination'].lower()
        if isValid=='y':
            validDegree.append(degree)
with open('Test/Include/'+'MTech_137_n_subjects_taken.csv','r',encoding='utf-8') as rf:
    read=DictReader(rf)
    for row in read:
        isValid=row['Valid'].lower()
        subject=row['137_n_subjects_taken'].lower()
        if isValid=='y':
            validSubject.append(subject)
with open('mtech_file.csv','r',encoding='utf-8') as rf:
    with open('shortlisted.csv','w',newline='') as wf:
        with open('not-shortlisted.csv','w',newline='') as wf1:
            csv_reader=DictReader(rf)
            csv_writer=DictWriter(wf,fieldnames=csv_reader.fieldnames)
            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames+['remarks'])
            csv_writer.writeheader()
            csv_writer1.writeheader()
            for row in csv_reader:
                selected=0
                qualifiedDeg=0
                qualifiedSub=0
                reason=""
                qfd=row['137_n_degree_or_examination'].lower()
                qdis=row['137_n_subjects_taken'].lower()
                qfc=row['137_y_name_of_institution_or_university'].lower()
                unwanted_string=["indian",'institute',' of ','technology','.',',',' ']
                replaced_string=['i','i',' ','t','','','']
                index=0
                for i in unwanted_string :
                    qfc=qfc.replace(i,replaced_string[index])
                    index=index+1
                qfc=qfc[:3]
                gate_exam=row['215_n_have_you_written_the_gate_examination'].lower()
                # string=row['140_o_valid_upto']
                string = row['140_r_exam_passing_year']
                
                # string = "2022"
                # string=(string[len(string)-2:len(string)])
                gate_valid_year=0
                if len(string)==4:
                    gate_valid_year=int(string)+2
                gate_valid=0
                if gate_valid_year>=current_year and gate_exam=="yes":
                    gate_valid=1
                else :
                    reason+="Gate validity year exceeded , "
                gaters=(row['140_k_gate_rank'])
                gate_rank =1
                if len(gaters)>0:
                    gate_rank=int(gaters)
                else:
                    gate_rank=100000000000000
                qcpi=float(row['137_e_percentage_of_marks_or_final_grade_point_average'])
                hscpi=float(row['135_e_percentage_of_marks_or_final_grade_point_average'])
                imcpi=float(row['190_e_percentage_of_marks_or_final_grade_point_average'])
                pd=(row['134_d_physically_handicapped']).lower()
                category=(row['134_y_category']).lower()
                if qfd in validDegree:
                    qualifiedDeg=1
                else:
                    reason+="Degree is not valid , "
                    # csv_writer1.writerow(row)
                    # continue
                if qdis in validSubject:
                    qualifiedSub=1
                else:
                    reason+="Stream is not valid(main stream must be CSE ) ,"
                    # csv_writer1.writerow(row)
                    # continue
                marks=1
                if category=="general" or category=="ews"  or category=="obc non creamy layer":
                    if not ((qcpi>=6.5 and qcpi<=10) or qcpi>=60) :
                        marks=0
                        reason+="Qualifictation cpi is not valid , "
                    if not ((hscpi>=6.5 and hscpi<=10) or hscpi>=60):
                        marks=0
                        reason+="High school(tenth) cpi is not valid , "

                    if not ((imcpi>=6.5 and imcpi<=10) or imcpi>=60):
                        marks=0
                        reason+="Intermediate (12th) cpi is not valid , "

                if category=="sc" or category=="st":
                    if not ((qcpi>=6 and qcpi<=10) or qcpi>=55):
                        marks=0
                        reason+="Qualifictation cpi is not valid , "
                    if not ((hscpi>=6 and hscpi<=10) or hscpi>=55):
                        marks=0
                        reason+="High school(tenth) cpi is not valid , "

                    if not ((imcpi>=6 and imcpi<=10) or imcpi>=55):
                        marks=0
                        reason+="Intermediate (12th) cpi is not valid , "
                if category=="general" and gate_rank>1400 :
                    reason+= "Gate rank is above 1400 , "

                if (category=="ews" or category=="obc non creamy layer") and gate_rank>2200 :
                    reason +="Gate rank is above 2200 ,"

                if category=="sc" and gate_rank>12000 :
                    reason +="Gate rank is above 12000 ,"


                if gate_valid==1 and qualifiedDeg==1 and qualifiedSub==1:
                    if category=="general" and marks==1 and (gate_rank<=1400 or pd=="yes"):
                        csv_writer.writerow(row)
                        selected=1
                    elif category=="ews" and marks==1 and (gate_rank<=2200 or pd=="yes"):
                        csv_writer.writerow(row)
                        selected=1
                    elif category=="obc non creamy layer" and marks==1  and (gate_rank<=2200 or pd=="yes"):
                        csv_writer.writerow(row)
                        selected=1
                    elif category=='sc' and marks==1 and (gate_rank<=12000 or pd=="yes"):
                        csv_writer.writerow(row)
                        selected=1
                    elif category=='st' and marks==1 :
                        csv_writer.writerow(row)
                        selected=1
                if selected==0 :
                    if qualifiedDeg==1 and qualifiedSub==1 and (qcpi>=8 and ((hscpi>=6.5 and hscpi<=10) or hscpi>=60) and ((imcpi>=6.5 and imcpi<=10) or imcpi>=60) and qfc=="iit"):
                        csv_writer.writerow(row)
                    else :
                        row.update({'remarks': reason})
                        csv_writer1.writerow(row)
                        print(reason)
                        # csv_writer1.writerow({'remarks':'Marks not valid'})        
with open('not-shortlisted.csv','r') as rf:
    with open('ns_general.csv','w',newline='') as wf1:
        with open('ns_obc.csv','w',newline='') as wf2:
            with open('ns_ews.csv','w',newline='') as wf3:
                with open('ns_sc.csv','w',newline='') as wf4:
                    with open ('ns_st.csv','w',newline='') as wf5:
                        with open ('ns_pwd.csv','w',newline='') as wf6:
                            csv_reader=DictReader(rf)
                            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames)
                            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames)
                            csv_writer2=DictWriter(wf2,fieldnames=csv_reader.fieldnames)
                            csv_writer3=DictWriter(wf3,fieldnames=csv_reader.fieldnames)
                            csv_writer4=DictWriter(wf4,fieldnames=csv_reader.fieldnames)
                            csv_writer5=DictWriter(wf5,fieldnames=csv_reader.fieldnames)
                            csv_writer6=DictWriter(wf6,fieldnames=csv_reader.fieldnames)
                            csv_writer1.writeheader()
                            csv_writer2.writeheader()
                            csv_writer3.writeheader()
                            csv_writer4.writeheader()
                            csv_writer5.writeheader()
                            csv_writer6.writeheader()
                            for row in csv_reader:
                                if(row['134_d_physically_handicapped']=='Yes'):
                                    csv_writer6.writerow(row)
                                elif(row['134_y_category'].lower()=='general'):
                                    csv_writer1.writerow(row)
                                elif(row['134_y_category'].lower()=='obc non creamy layer'):
                                    csv_writer2.writerow(row)
                                elif(row['134_y_category'].lower()=='ews'):
                                    csv_writer3.writerow(row)
                                elif(row['134_y_category'].lower()=='sc'):
                                    csv_writer4.writerow(row)
                                elif(row['134_y_category'].lower()=='st'):
                                    csv_writer5.writerow(row)
with open('shortlisted.csv','r') as rf:
    with open('general.csv','w',newline='') as wf1:
        with open('obc.csv','w',newline='') as wf2:
            with open('ews.csv','w',newline='') as wf3:
                with open('sc.csv','w',newline='') as wf4:
                    with open ('st.csv','w',newline='') as wf5:
                        with open ('pwd.csv','w',newline='') as wf6:
                            csv_reader=DictReader(rf)
                            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames)
                            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames)
                            csv_writer2=DictWriter(wf2,fieldnames=csv_reader.fieldnames)
                            csv_writer3=DictWriter(wf3,fieldnames=csv_reader.fieldnames)
                            csv_writer4=DictWriter(wf4,fieldnames=csv_reader.fieldnames)
                            csv_writer5=DictWriter(wf5,fieldnames=csv_reader.fieldnames)
                            csv_writer6=DictWriter(wf6,fieldnames=csv_reader.fieldnames)
                            csv_writer1.writeheader()
                            csv_writer2.writeheader()
                            csv_writer3.writeheader()
                            csv_writer4.writeheader()
                            csv_writer5.writeheader()
                            csv_writer6.writeheader()
                            for row in csv_reader:
                                if(row['134_d_physically_handicapped']=='Yes'):
                                    csv_writer6.writerow(row)
                                elif(row['134_y_category'].lower()=='general'):
                                    csv_writer1.writerow(row)
                                elif(row['134_y_category'].lower()=='obc non creamy layer'):
                                    csv_writer2.writerow(row)
                                elif(row['134_y_category'].lower()=='ews'):
                                    csv_writer3.writerow(row)
                                elif(row['134_y_category'].lower()=='sc'):
                                    csv_writer4.writerow(row)
                                elif(row['134_y_category'].lower()=='st'):
                                    csv_writer5.writerow(row)
with ZipFile('Mtech_shortlisted.zip', 'w') as zipObj2:
   zipObj2.write('shortlisted.csv')
   zipObj2.write('not-shortlisted.csv')
   zipObj2.write('general.csv')
   zipObj2.write('ews.csv')
   zipObj2.write('obc.csv')
   zipObj2.write('sc.csv')
   zipObj2.write('st.csv')
   zipObj2.write('pwd.csv')
   zipObj2.write('ns_general.csv')
   zipObj2.write('ns_ews.csv')
   zipObj2.write('ns_obc.csv')
   zipObj2.write('ns_sc.csv')
   zipObj2.write('ns_st.csv')
   zipObj2.write('ns_pwd.csv')

os.remove("shortlisted.csv")
os.remove("not-shortlisted.csv")
os.remove("sc.csv")
os.remove("st.csv")
os.remove("ews.csv")
os.remove("general.csv")
os.remove("obc.csv")
os.remove("pwd.csv")
os.remove("ns_sc.csv")
os.remove("ns_st.csv")
os.remove("ns_ews.csv")
os.remove("ns_general.csv")
os.remove("ns_obc.csv")
os.remove("ns_pwd.csv")
# os.remove("mtech_file.csv")

Path("Test/Yearwise/" + yearGiven + "/mtech").mkdir(parents=True, exist_ok=True)
Path("mtech_file.csv").rename("Test/Yearwise/" + yearGiven + "/mtech/mtech_file.csv")