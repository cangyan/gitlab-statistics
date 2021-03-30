#!/usr/bin/python
 
import gitlab
import xlwt
import os
 
#用户git账户的token
private_token = os.environ['token']
#git地址
private_host = os.environ['host']
#提交代码的域账户名称1
author_email = os.environ['author_email'].split(',')

start_time = os.environ['start_time']
end_time = os.environ['end_time']

filter_project = os.environ['project'].split(',')
filter_branch = os.environ['branch'].split(',')
 
def getAllProjects():
    client = gitlab.Gitlab(private_host,private_token=private_token)
    projects = client.projects.list(membership=True,all=True)
    return projects
 
def getAllBranchByProject(project):
    branches = project.branches.list(all=True)
    return branches
 
def getCommitByBranch(project,branch):
    author_commits=[]
    commits = project.commits.list(all=True,query_parameters={'since': start_time,'until':end_time, 'ref_name': branch.name})
    for commit in commits:
        committer_email = commit.committer_email
        title = commit.title
        message = commit.message
        if ('Merge' in message) or ('Merge' in title):
            print('Merge跳过')
            continue
        else:
            for email in author_email :
                if (str(email) and committer_email.find(email) >= 0) :
                    author_commits.append(commit)
            
    return author_commits
 
def getCodeByCommit(commit,project):
    commit_info = project.commits.get(commit.id)
    code =commit_info.stats
    return code
 
def getAuthorCode():
    data=[]
    projects = getAllProjects()
    for project in projects:
        if len(filter_project) == 0 or project.name in filter_project :
            branches = getAllBranchByProject(project)
            for branch in branches:
                if  len(filter_branch) == 0 or branch.name in filter_branch :
                    print('获取工程',project.name,'分支',branch.name,"的提交记录")
                    branchdata = {}
                    branchdata['projectname'] = project.name
                    branchdata['branchename'] = branch.name
                    author_commits = getCommitByBranch(project,branch)
                    codes = []
                    for commit in author_commits:
                        print('获取提交',commit.id,"的代码量")
                        code = getCodeByCommit(commit,project)
                        codes.append(code)
                    record=calculate(codes)
                    branchdata['commitcount'] = len(author_commits)
                    branchdata['codecount'] = record
                    data.append(branchdata)
        
    return data
 
def writeExcel(excelPath,data):
    workbook = xlwt.Workbook()
    #获取第一个sheet页
    sheet = workbook.add_sheet('git')
    row0=['工程名称','分支名称','提交次数','新增代码','删除代码','总计代码']
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i])
    addcount = 0
    delcount =0
    totalcount = 0
    commitcount = 0
    for i in range(0,len(data)):
        recode = data[i]
        j=0
        sheet.write(i+1,j,recode['projectname'])
        sheet.write(i+1,j+1,recode['branchename'])
        commitcount +=(int)(recode['commitcount'])
        sheet.write(i+1,j+2,recode['commitcount'])
        addcount += (int)(recode['codecount']['additions'])
        sheet.write(i+1,j+3,recode['codecount']['additions'])
        delcount +=(int)(recode['codecount']['deletions'])
        sheet.write(i+1,j+4,recode['codecount']['deletions'])
        totalcount +=(int)(recode['codecount']['total'])
        sheet.write(i+1,j+5,recode['codecount']['total'])
    sheet.write(len(data)+1,2,commitcount)
    sheet.write(len(data)+1,3,addcount)
    sheet.write(len(data)+1,4,delcount)
    sheet.write(len(data)+1,5,totalcount)
    workbook.save(excelPath)
 
def calculate(data):
    record ={}
    addacount =0
    deletecount =0
    totaolcount =0
    for i in data:
        addacount+= int(i['additions'])
        deletecount+= int(i['deletions'])
        totaolcount+= int(i['total'])
    record['additions'] = addacount
    record['deletions'] = deletecount
    record['total'] = totaolcount
    return record
 
if __name__ == '__main__':
    data = getAuthorCode()
    print('result',data)
    writeExcel('/output/result.xls',data)