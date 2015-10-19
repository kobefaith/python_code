#!/usr/bin/python
#-*-encoding: UTF-8 -*-
import os,sys,re
'''
   This script can find the line which violate the EDKII coding standards.
   You may run this script on Python version 2.7 .The input format of path is like this "c:/your code folder".
   The output may be like this:
   "EDKII Coding Standards violation :c:/d/1/CryptoPkg\Library\OpensslLib\openssl-0.9.8l\apps\ca.c line 2818	if (i == 0)
   This line contain Tab !" (It means the line 2818 in c:/d/1/CryptoPkg\Library\OpensslLib\openssl-0.9.8l\apps\ca.c contain 'TAB'.)
'''
def VisitDir(path):
    for root,dirs,files in os.walk(path,True):
        for filepath in files:            
            pa=[]
            pa=filepath
            if (pa[-1]=='h'and pa[-2]=='.'):                
                fp=os.path.join(root, filepath)                
                fd=open(fp,"r")
                line_num=0               
                lines=fd.readlines()
                fd.close()
                li_num=0
                flg_comment=0
                flg_def=0
                flg_start=2
                for line in lines:
                    line_num+=1                    
                    if(comment_start_check(line)==True):
                        flg_start=0;
                    if((flg_start==0)and(comment_end_check(line)==True)):
                        flg_def=0
                        flg_start+=1
                    if((comment_check(line)==False)and (line_check(line)==True)and(flg_start!=0)):
                        flg_def+=1
                    if((flg_start==1)and(comment_check(line)==False)and(line_check(line)==True)and(flg_def==1)and(ifndef_check(line)==2)):
                        print "EDKII Coding Standards  violation :{0} line {1} have no #ifndef #endif on the first line!".format(fp,line_num) 
                    include_check(line,line_num,fp)                              
            elif (pa[-1]=='c'and pa[-2]=='.'):                
                fp=os.path.join(root, filepath)                
                fd=open(fp,"r")
                line_num=0
                flg_tab=0                
                lines=fd.readlines()
                fd.close()
                for line in lines:
                    line_num+=1
                    tab_check(line,line_num,fp)
                    define_check(line,line_num,fp)
                    efi_check(line,line_num,fp)
                    asm_check(line,line_num,fp)
                    statement_check(line,line_num,fp)
                    equal_check(line,line_num,fp)
                    declar_check(line,line_num,fp)
'''
    This function check the #ifndef and #endf
'''
def ifndef_check(line1):
    if(re.search(r"[#]+\b(ifndef)\b",line1)!=None):
        return 1    
    else:
        return 2   
def comment_start_check(line1):
    if(re.search(r"^[/][*]",line1)!=None):
        return True    
    else:
        return False
def comment_check(line1):
    if(re.search(r"^[/][/]",line1)!=None):
        return True    
    else:
        return False
def comment_end_check(line1):
    if(re.search(r"^[*][*][/]",line1)!=None):
        return True    
    else:
        return False
def line_check(line1):
    if(re.search(r"\b(\w+)\b",line1)!=None):
        return True    
    else:
        return False
def tab_check(line2,line_num1,fp1):
    if(re.search(r"\t",line2)!=None):
        print "EDKII Coding Standards violation :{0} line {1}{2} This line contain Tab !".format(fp1,line_num1,line2)
    else:
        return False
def define_check(line2,line_num1,fp1):
    if((re.search(r"\b(define)\b",line2)!=None)or(re.search(r"\b(typedef)\b",line2)!=None)):
        print "EDKII Coding Standards violation :{0} line {1}{2} This line contain #define or typedef!".format(fp1,line_num1,line2)
    else:
        return False
def efi_check(line1,line_num1,fp1):
    if(re.search(r"\b(int|unsigned|char|void|static|long)\b",line1)!=None):
        print "EDKII Coding Standards violation :{0} line {1}{2} This line contain Non-EFI data type!".format(fp1,line_num1,line1)  
    else:
        return False
def asm_check(line2,line_num1,fp1):
    if(re.search(r"\b(_asm)\b",line2)!=None):
        print "EDKII Coding Standards violation :{0} line {1}{2} This line contain  _ASM !".format(fp1,line_num1,line2)
    else:
        return False
def statement_check(line2,line_num1,fp1):
    if((re.search(r"\b(for)\b",line2)!=None)or(re.search(r"\b(if)\b",line2)!=None)or(re.search(r"\b(while)\b",line2)!=None)):
        if(re.search(r".*({).*(\w+)",line2)!=None):
            print "EDKII Coding Standards violation :{0} line {1}{2} There are one more statements on one line !".format(fp1,line_num1,line2)        
    elif(re.search(r".*(;).*(\w+)",line2)!=None):
        if((re.search(r".*[/][/].*(\w+)",line2)==None)and(re.search(r".(/*)(/)[*].*(\w+).*(/*)(/)",line2)==None)):
            print "EDKII Coding Standards violation :{0} line {1}{2} There are one more statements on one line !".format(fp1,line_num1,line2)
    else:
        return False
def include_check(line2,line_num1,fp1):
    if(re.search(r"\b(include)\b",line2)!=None):
        print "EDKII Coding Standards violation :{0} line {1}{2} This line contain #include<> in head file!".format(fp1,line_num1,line2)       
    else:
        return False
    
def equal_check(line2,line_num1,fp1):
    if((re.search(r"\b(if)\b\s*(\().*(\)).*({)",line2)!=None)or(re.search(r"\b(while)\b\s*(\().*(\)).*({)",line2)!=None)):
       if(re.search(r"(.*\b(=)\b\s*[0-9]+\b(\())",line2)!=None):
           print "Tips :{0} line {1}{2} May be this is '==' not '='!".format(fp1,line_num1,line2)
       else:
           return 1
    else:
        return 3
def declar_check(line2,line_num1,fp1):
    if(re.search(r"\b(BOOLEAN|INTN|UINTN|INT8|UINT8|INT16|UINT16|INT32|UINT32|INT64|UINT64|CHAR8|CHAR16|VOID|EFI_GUID|EFI_STATUS|EFI_HANDLE|EFI_EVENT|EFI_LBA|EFI_TPL)\b\s*.*(,).*(;)",line2)!=None):
        if(re.search(r".*(,).*(\)|\})(;)",line2)==None):
            print "EDKII Coding Standards violation :{0} line {1}{2} There are more than one declaration per line!  ".format(fp1,line_num1,line2)
        else:
            return 1
    else:
        return 2

if __name__=="__main__":
    path=raw_input("enter a path:")
    VisitDir(path)
    


