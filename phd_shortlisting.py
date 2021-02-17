# import datetime
from pathlib import Path
from datetime import date
from datetime import datetime
from zipfile import ZipFile
import os
import sys
x=date.today()
yearGiven=sys.argv[1]
# yearGiven = "2020"
current_year = int(yearGiven)
this_date = int(x.strftime("%d"))
this_month = int(x.strftime("%m"))
from csv import DictReader,DictWriter
validSubject=[]
validDegree=[]
degShort=[]
with open('Test/Include/'+'Phd_101_e_discipline.csv','r',encoding='utf-8') as rf:
    csv_reader=DictReader(rf)
    for row in csv_reader:
        if row['Valid'].lower()=='y':
            validSubject.append(row['101_e_discipline'].lower())
with open('Test/Include/'+'Phd_101_e_qualification_degree.csv','r',encoding='utf-8') as rf:
    csv_reader=DictReader(rf)
    for row in csv_reader:
        validDegree.append(row['101_e_qualification_degree'].lower())
        degShort.append(row['Deg'].lower())
# print(validDegree)
with open('phd_file.csv','r',encoding='utf-8') as rf:
    with open('shortlisted.csv','w',newline='') as wf:
        with open('not-shortlisted.csv','w',newline='') as wf1:
            csv_reader=DictReader(rf)
            # csv_writer=DictWriter(wf,fieldnames=['name']) 
            csv_writer=DictWriter(wf,fieldnames=csv_reader.fieldnames + ['remarks']) 
            csv_writer1=DictWriter(wf1,fieldnames=csv_reader.fieldnames+['remarks']) 
            csv_writer.writeheader()
            csv_writer1.writeheader() 
            for row in csv_reader:
                selected=0
                qualifyingDegree=row['101_e_qualification_degree'].lower()
                ind = validDegree.index(qualifyingDegree)
                qfd = degShort[ind].lower()
                qdis=row['101_e_discipline'].lower()
                qfc=row['101_y_name_and_place_of_institution_or_university'].lower()
                unwanted_string=['indian','institute',' of ','technology','.',',',' ','school','mines','science','statistical']
                replaced_string=['i','i',' ','t','','','','s','m','sc','s']
                index=0
                for i in unwanted_string :
                    qfc=qfc.replace(i,replaced_string[index])
                    index=index+1
                qfc=qfc[:3]
                examType2 = row['105_e_exam_name'].lower().find('jrf')
                examType = row['109_e_exam_name'].lower()
                gate_exam=row['215_n_have_you_written_the_gate_examination'].lower()
                string=row['109_o_valid_upto'].replace('-','')
                gate_valid_year=0
                if len(string)>0:
                    gate_valid_year=int(string)
                gate_valid=0
                jrf_valid=0
                # gate_valid_year>=current_year and 
                gaters=(row['109_k_exam_rank'])
                gate_rank =1
                if len(gaters)>0:
                    gate_rank=int(gaters)
                else:
                    gate_rank=1000000
                if (gate_exam=="yes"and examType=='gate'):
                    gate_valid=1
                if examType2!=-1:
                    jrf_valid=1
                
                ugcpi=float(row['104_e_percentage_of_marks_or_final_grade_point_average'])
                hscpi=float(row['102_e_percentage_of_marks_or_final_grade_point_average'])
                imcpi=float(row['103_e_percentage_of_marks_or_final_grade_point_average'])
                qcpis=row['101_e_overall_percentage_of_marks_or_final_grade_point_average']
                qcpi=0
                if len(qcpis)>0 :
                    qcpi=float(qcpis)
                pd=(row['159_d_physically_handicapped']).lower()
                category=(row['159_y_category']).lower()
                if len(category)>=3 :
                    category=category[:3] 
                gender = row['159_r_gender'].lower()
                birth = row['159_h_date_of_birth']
                birth=birth.replace('/','').replace('-','')
                birth_year = int(birth[4:8])
                birth_month = int(birth[2:4])
                birth_date = int(birth[:2])
                age=0
                this_month = 11
                this_date = 7 
                if this_month > birth_month:
                    age = current_year - birth_year + 1
                elif this_month == birth_month:
                    if this_date > birth_date:
                        age = current_year - birth_year + 1
                    else:
                        age = current_year - birth_year
                else:
                    age = current_year - birth_year 
                reason = ''
                reason1 = ''
                isDegree=0
                if row['UserId']=='24021':
                    print(age)
                if qdis not in validSubject:
                    reason += 'Invalid subject, '
                else:
                    if (qfd=='mtech' or qfd=='ms' or qfd=='me'): 
                        isDegree=1
                        validCPI=0
                        validAge=0
                        if not ((qcpi>=6.5 and qcpi<=10) or qcpi>=60):
                            reason += 'Invalid qualifying degree CPI, '
                            validCPI=1
                        if not ((hscpi>=6.5 and hscpi<=10) or hscpi>=60):
                            reason += 'Invalid 10th class CPI, '
                            validCPI = 1
                        if not ((imcpi>=6.5 and imcpi<=10) or imcpi>=60):
                            reason += 'Invalid 12th class CPI, '
                            validCPI = 1 
                        if not ((ugcpi>=6.5 and ugcpi<=10) or ugcpi>=60):
                            reason += 'Invalid undergraduate CPI, '
                            validCPI = 1
                        if not (gate_valid==1 or jrf_valid==1):
                            reason += 'Gate exam not attempted, '
                            validCPI = 1
                        if not ((category=='gen' and age<=32) or (age<=37 and (category=='obc' or category=='ews' or gender=='female'))):
                            reason += 'Age limit exceeded, '
                            validAge = 1
                        if (validCPI==0 and validAge==0):
                            reason1 += 'Mtech/ms/me qualifying all criteria'
                            row.update({'remarks': reason1})
                            csv_writer.writerow(row)
                            selected=1
                        elif (((qcpi>=7.5 and qcpi<=10) or qcpi>=70) and (((hscpi>=6 and hscpi<=10) or hscpi>=55) or ((imcpi>=6 and imcpi<=10) or imcpi>=55)) and (((hscpi>=5.5 and hscpi<=10) or hscpi>=50) and ((imcpi>=5.5 and imcpi<=10) or imcpi>=50))):
                            if (gate_valid==1 or jrf_valid==1) and validAge==0:
                                reason1 = 'M.Tech or M.E. or M.S.>=70% or 7.5 CPI then X>=55 or XII>=55'
                                row.update({'remarks': reason1})
                                csv_writer.writerow(row)
                                selected=1
                            else:
                                reason = 'Gate not valid'

                    elif (qfd=='btech' or qfd=='mca' or qfd=='msc' or qfd=='be'):
                        isDegree=1
                        validCPI=0
                        validAge=0
                        if not ((qcpi>=8 and qcpi<=10) or qcpi>=75):
                            reason += 'Invalid qualifying degree CPI, '
                            validCPI=1
                        if not ((hscpi>=6.5 and hscpi<=10) or hscpi>=60):
                            reason += 'Invalid 10th class CPI, '
                            validCPI = 1
                        if not ((imcpi>=6.5 and imcpi<=10) or imcpi>=60):
                            reason += 'Invalid 12th class CPI, '
                            validCPI = 1 
                        if not ((ugcpi>=6.5 and ugcpi<=10) or ugcpi>=60):
                            reason += 'Invalid undergraduate CPI, '
                            validCPI = 1
                        if not (gate_valid==1 or jrf_valid==1):
                            reason += 'Gate exam not attempted, '
                            validCPI = 1
                        if gate_rank>5000 and jrf_valid==0:
                            reason += 'Gate rank>5000, '
                            validCPI = 1
                        if not ((category=='gen' and age<=28) or (age<=33 and (category=='obc' or category=='ews' or gender=='female'))):
                            reason += 'Age limit exceeded, '
                            validAge = 1
                        if validAge==0 and validCPI==0:
                            reason1 += 'btech/mca/msc/be qualifying all criteria'
                            row.update({'remarks': reason1})
                            csv_writer.writerow(row)
                            selected=1
                    if category=='sc' or category=='st' or pd=='yes'and selected==0:
                        reason = ''
                        if (qfd=='mtech' or qfd=='ms' or qfd=='me'):
                            isDegree=1
                            validCPI=0
                            validAge=0
                            if not ((qcpi>=6.5 and qcpi<=10) or qcpi>=60):
                                reason += 'Invalid qualifying degree CPI, '
                                validCPI=1
                            if not ((hscpi>=6.5 and hscpi<=10) or hscpi>=60):
                                reason += 'Invalid 10th class CPI, '
                                validCPI = 1
                            if not ((imcpi>=6.5 and imcpi<=10) or imcpi>=60):
                                reason += 'Invalid 12th class CPI, '
                                validCPI = 1 
                            if not ((ugcpi>=6.0 and ugcpi<=10) or ugcpi>=55):
                                reason += 'Invalid undergraduate CPI, '
                                validCPI = 1
                            if not (gate_valid==1 or jrf_valid==1) :
                                reason += 'Gate exam not attempted, '
                                validCPI = 1
                            if age>37:
                                reason += 'age limit exceeded, '
                                validAge = 1
                            if validAge==0 and validCPI==0:
                                reason1 += 'sc/st/pd and mtech/ms/me qualifying all criteria, '
                                row.update({'remarks': reason1})
                                csv_writer.writerow(row)
                                selected=1
                            elif (((qcpi>=7.5 and qcpi<=10) or qcpi>=70) and (((hscpi>=6 and hscpi<=10) or hscpi>=55) or ((imcpi>=6 and imcpi<=10) or imcpi>=55)) and (((hscpi>=5.5 and hscpi<=10) or hscpi>=50) and ((imcpi>=5.5 and imcpi<=10) or imcpi>=50))):
                                if (gate_valid==1 or jrf_valid==1) and validAge==0:
                                    reason1 = 'M.Tech or M.E. or M.S.>=70% or 7.5 CPI then X>=55 or XII>=55'
                                    row.update({'remarks': reason1})
                                    csv_writer.writerow(row)
                                    selected=1
                                else:
                                    reason = 'Gate not valid'
                        elif (qfd=='btech' or qfd=='mca' or qfd=='msc' or qfd=='be'):
                            isDegree=1
                            validCPI=0
                            validAge=0
                            if not ((qcpi>=8 and qcpi<=10) or qcpi>=75):
                                reason += 'Invalid qualifying degree CPI, '
                                validCPI=1
                            if not ((hscpi>=6.5 and hscpi<=10) or hscpi>=60):
                                reason += 'Invalid 10th class CPI, '
                                validCPI = 1
                            if not ((imcpi>=6.5 and imcpi<=10) or imcpi>=60):
                                reason += 'Invalid 12th class CPI, '
                                validCPI = 1 
                            if not ((ugcpi>=6 and ugcpi<=10) or ugcpi>=55):
                                reason += 'Invalid undergraduate CPI, '
                                validCPI = 1
                            if not (gate_valid==1 or jrf_valid==1):
                                reason += 'Gate exam not attempted, '
                                validCPI = 1
                            if gate_rank>6000 and jrf_valid==0:
                                reason += 'Gate rank>6000, '
                                validCPI = 1
                            if age>33:
                                reason += 'Age limit exceeded, '
                            if validAge==0 and validCPI==0:
                                if jrf_valid==1:
                                    reason1 += "JRF qualified, "
                                reason1 += 'sc/st/pd with btech/be/msc/mca qualifying all criteria, '
                                row.update({'remarks': reason1})
                                csv_writer.writerow(row)
                                selected=1
                if selected==0:
                    findInvalid = reason.find("Invalid")
                    flag=0
                    if row['159_y_seeking_phd_admission_under_category'] == 'Employed and Part Time' and findInvalid==-1:
                        startDate1 = row['106_k_start_date_of_work']
                        endDate1 = row['106_k_end_date_of_work']
                        startDate2 = row['161_k_start_date_of_work']
                        endDate2 = row['161_k_end_date_of_work']
                        if len(endDate1) == 0:
                            endDate1 = yearGiven + "-11" + "-07"
                        else:
                            d1 = endDate1[3:5]
                            m1 = endDate1[:2]
                            y1 = endDate1[6:]
                            endDate1 = y1 + "-" + m1 + "-" + d1  
                        endDate1 = datetime.strptime(endDate1,"%Y-%m-%d")
                        if len(startDate1) == 0:
                            endDate1 = datetime.strptime("1950-02-19","%Y-%m-%d")
                            startDate1 = endDate1
                        else:
                            d1 = startDate1[3:5]
                            m1= startDate1[:2]
                            y1 = startDate1[6:]
                            startDate1 = y1 + "-" + m1 + "-" + d1  
                            startDate1 = datetime.strptime(startDate1,"%Y-%m-%d") 

                        experience = ((endDate1-startDate1).days)/365
                        
                        if len(endDate2) == 0:
                            endDate2 = yearGiven + "-11" + "-07" 
                        else:
                            d1 = endDate2[3:5]
                            m1 = endDate2[:2]
                            y1 = endDate2[6:]
                            endDate2 = y1 + "-" + m1 + "-" + d1  
                        endDate2 = datetime.strptime(endDate2,"%Y-%m-%d")

                        if len(startDate2) == 0:
                            startDate2 = startDate1
                            endDate2 = startDate1
                        else:
                            d1 = startDate2[3:5]
                            m1 = startDate2[:2]
                            y1 = startDate2[6:]
                            startDate2 = y1 + "-" + m1 + "-" + d1  
                            startDate2 = datetime.strptime(startDate2,"%Y-%m-%d")
                        
                        if startDate1 >= endDate2 and ((endDate1-startDate1).days)/365 >= 2:
                            flag = 1
                            reason1 += 'Employed for greater than 2 years'
                        
                        elif startDate2 >= endDate1 and ((endDate2-startDate2).days)/365 >= 2:
                            flag = 1
                            reason1 += 'Employed for greater than 2 years'
                        else:
                            reason += 'Less than 2 years experience in job'

                    if ((qfc=='iit' or qfc=='iis' or qfc=='isi' or qfc=='ism') and ((ugcpi>=6 and ugcpi<=10) or ugcpi>=55) and qfd[0]=='m') and gate_valid==1 and ((category=='gen' and age<=32) or (age<=37 and (category=='obc' or category=='ews' or gender=='female'))):
                        flag=1
                        reason1 += 'Masters from IIT/IISc/ISI ugper>=55 or 6.0 '
                    # if (qfd=='mtech' or qfd=='ms' or qfd=='me') and ((qcpi>=7.5 and qcpi<=10) or qcpi>=70) and (((hscpi>=6 and hscpi<=10) or hscpi>=55) or ((imcpi>=6 and imcpi<=10) or imcpi>=55)) and (((hscpi>=5.5 and hscpi<=10) or hscpi>=50) and ((imcpi>=5.5 and imcpi<=10) or imcpi>=50)) and ((category=='gen' and age<=32) or (age<=37 and (category=='obc' or category=='ews' or gender=='female'))) and gate_valid==1:
                    #     flag=1
                    #     reason1 += 'M.Tech or M.E. or M.S.>=70% or 7.5 CPI then X>=55 or XII>=55'
                    if qfc=='iit' and (((hscpi>=6 and hscpi<=10) or hscpi>=55) or ((imcpi>=6 and imcpi<=10) or imcpi>=55)) and qfd=='btech' and ((category=='gen' and age<=28) or (age<=33 and (category=='obc' or category=='ews' or gender=='female'))):
                        flag=1
                        reason1 += 'B.Tech from IITs with CGPA>=8.0 then no gate required and X>=55% or XII>=55% ' 
                    if flag==1:
                        row.update({'remarks': reason1})
                        csv_writer.writerow(row)
                    else:
                        if isDegree==0:
                            reason += 'Invalid Degree, '
                        row.update({'remarks': reason})
                        csv_writer1.writerow(row)
                        
with open('shortlisted.csv','r') as rf:
    with open('general.csv','w',newline='') as wf1:
        with open('obc.csv','w',newline='') as wf2:
            with open('ews.csv','w',newline='') as wf3:
                with open('sc.csv','w',newline='') as wf4:
                    with open ('st.csv','w',newline='') as wf5:
                        with open('pd.csv','w', newline='') as wf6:
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
                                if(row['159_y_category'].lower()=='general'):
                                    csv_writer1.writerow(row) 
                                elif(row['159_y_category'].lower()=='obc non creamy layer'):
                                    csv_writer2.writerow(row)
                                elif(row['159_y_category'].lower()=='ews'):
                                    csv_writer3.writerow(row)
                                elif(row['159_y_category'].lower()=='sc'):
                                    csv_writer4.writerow(row)
                                elif(row['159_y_category'].lower()=='st'):
                                    csv_writer5.writerow(row)      
                                elif(row['159_d_physically_handicapped'].lower()=='yes'):
                                    csv_writer6.writerow(row)
with open('not-shortlisted.csv','r') as rf:
    with open('ns_general.csv','w',newline='') as wf1:
        with open('ns_obc.csv','w',newline='') as wf2:
            with open('ns_ews.csv','w',newline='') as wf3:
                with open('ns_sc.csv','w',newline='') as wf4:
                    with open ('ns_st.csv','w',newline='') as wf5:
                        with open('ns_pd.csv','w', newline='') as wf6:
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
                                if(row['159_y_category'].lower()=='general'):
                                    csv_writer1.writerow(row) 
                                elif(row['159_y_category'].lower()=='obc non creamy layer'):
                                    csv_writer2.writerow(row)
                                elif(row['159_y_category'].lower()=='ews'):
                                    csv_writer3.writerow(row)
                                elif(row['159_y_category'].lower()=='sc'):
                                    csv_writer4.writerow(row)
                                elif(row['159_y_category'].lower()=='st'):
                                    csv_writer5.writerow(row)      
                                elif(row['159_d_physically_handicapped'].lower()=='yes'):
                                    csv_writer6.writerow(row)


with ZipFile('PhD_shortlisted.zip', 'w') as zipObj2:
   zipObj2.write('shortlisted.csv')
   zipObj2.write('not-shortlisted.csv')
   zipObj2.write('general.csv')
   zipObj2.write('ews.csv')
   zipObj2.write('obc.csv')
   zipObj2.write('sc.csv')
   zipObj2.write('st.csv')
   zipObj2.write('pd.csv')
   zipObj2.write('ns_general.csv')
   zipObj2.write('ns_ews.csv')
   zipObj2.write('ns_obc.csv')
   zipObj2.write('ns_sc.csv')
   zipObj2.write('ns_st.csv')
   zipObj2.write('ns_pd.csv')

os.remove("shortlisted.csv")
os.remove("not-shortlisted.csv")
os.remove("sc.csv")
os.remove("st.csv")
os.remove("ews.csv")
os.remove("general.csv")
os.remove("obc.csv")
os.remove("pd.csv")
os.remove("ns_sc.csv")
os.remove("ns_st.csv")
os.remove("ns_ews.csv")
os.remove("ns_general.csv")
os.remove("ns_obc.csv")
os.remove("ns_pd.csv")
# os.remove("phd_file.csv")                    

Path("Test/Yearwise/" + yearGiven + "/phd").mkdir(parents=True, exist_ok=True)
Path("phd_file.csv").rename("Test/Yearwise/" + yearGiven + "/phd/phd_file.csv")










               