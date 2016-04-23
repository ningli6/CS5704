# Python script that extract basic stats about bug reports
# Reports must be in json format

import json
import sys
import os
import glob
#excel python model
import xlsxwriter

from datetime import datetime

# Usage: python stats.py [report.json]

# len
def numberOfBugs(data):
	return len(data)

def numberOfBugsWithPatch(data):
	count = 0
	for d in data:
		if d['NumberOfPatches']:
			count += 1
	return count

# comments
def max_comments(data):
	max_comments = 0
	for d in data:
		max_comments = max(d['NumberOfComments'], max_comments)
	return max_comments

def avg_comments(data):
	comments = 0
	for d in data:
		comments += d['NumberOfComments']
	return comments / float(len(data))

# patches
def max_patches(data):
	max_patches = 0
	for d in data:
		max_patches = max(d['NumberOfPatches'], max_patches)
	return max_patches

def avg_patches(data):
	patches = 0
	for d in data:
		patches += d['NumberOfPatches']
	return patches / float(len(data))

# developers
def max_developers(data):
	max_developers = 0
	for d in data:
		max_developers = max(d['NumberOfDevelopers'], max_developers)
	return max_developers

def avg_developers(data):
	developers = 0
	for d in data:
		developers += d['NumberOfDevelopers']
	return developers / float(len(data))


# code changes
# for each bug, average lines of code added per bug
def avg_code_added_per_bug(data):
	added = 0
	for d in data:
		for p in d['Patches']:
			for change in p['Changes']:
				if change.get('Added'):
					added += int(change.get('Added'))
	return added / float(len(data))

# for each bug, average lines of code added per bug with patch
def avg_code_added_per_bug_with_patch(data):
	added = 0
	count = float(numberOfBugsWithPatch(data))
	for d in data:
		for p in d['Patches']:
			for change in p['Changes']:
				if change.get('Added'):
					added += int(change.get('Added'))
	return added / count

# for each bug, average lines of code deleted per bug
def avg_code_deleted_per_bug(data):
	deleted = 0
	for d in data:
		for p in d['Patches']:
			for change in p['Changes']:
				if change.get('Deleted'):
					deleted += int(change.get('Deleted'))
	return deleted / float(len(data))

# for each bug, average lines of code deleted per bug with patch
def avg_code_deleted_per_bug_with_patch(data):
	deleted = 0
	count = float(numberOfBugsWithPatch(data))
	for d in data:
		for p in d['Patches']:
			for change in p['Changes']:
				if change.get('Deleted'):
					deleted += int(change.get('Deleted'))
	return deleted / count

# time, ignore those don't have patches
def avg_time_per_bug(data):
	mins = 0
	count = float(numberOfBugsWithPatch(data))
	for d in data:
		if d['NumberOfPatches'] == 0:
			continue
		start_time = datetime.strptime(d['ReportTime'][:-4], '%Y-%m-%d %H:%M')
		last_patch_time = datetime.strptime(d['Patches'][d['NumberOfPatches'] - 1]['PatchTime'][:-4], '%Y-%m-%d %H:%M')
		diff = last_patch_time - start_time
		mins += (diff.days * 24 * 60 + diff.seconds / 60) / count
	return str(mins / 1440) + ' Days, ' + str(mins % 1440 / 60) + ' Hours, ' + str((mins % 1440) % 60) + ' Minutes'

def generate_stats():
    workbook = xlsxwriter.Workbook('Stats.xlsx')
    worksheet = workbook.add_worksheet()
    tags=['Number of bugs:','Number of bugs with patch:','Average number of comments per bug:','Max number of comments per bug:','Average number of patches per bug:','Max number of patches per bug:', 'Average number of developers per bug:','Max number of developers per bug:','Average lines of code added per bug:', 'Average lines of code added for patched bugs:', 'Average lines of code deleted per bug:', 'Average lines of code deleted for patched bugs:', 'Average time per bug:' ]
    row = 1
    col = 0
    for tag in tags:
        worksheet.write(row, col,tag)
        row+=1
    col+=1
    
    for filename in glob.glob('Data/*.json'):
        row=0
        r=[None]*14;
        r[13]=filename[5:-5]
        
        raw_json_data = open(filename)
        data = json.load(raw_json_data)
        # print 'Number of bugs:', 
        r[0]=numberOfBugs(data)
		# print 'Number of bugs with patch:', 
        r[1]=numberOfBugsWithPatch(data)
		# print 'Average number of comments per bug:', 
        r[2]=avg_comments(data)
		# print 'Max number of comments per bug:', 
        r[3]=max_comments(data)
		# print 'Average number of patches per bug:', 
        r[4]=avg_patches(data)
		# print 'Max number of patches per bug:', 
        r[5]=max_patches(data)
		# print 'Average number of developers per bug:', 
        r[6]=avg_developers(data)
		# print 'Max number of developers per bug:', 
        r[7]=max_developers(data)
		# print 'Average lines of code added per bug:', 
        r[8]=avg_code_added_per_bug(data)
		# print 'Average lines of code added for patched bugs:', 
        r[9]=avg_code_added_per_bug_with_patch(data)
		# print 'Average lines of code deleted per bug:', 
        r[10]=avg_code_deleted_per_bug(data)
		# print 'Average lines of code deleted for patched bugs:', 
        r[11]=avg_code_deleted_per_bug_with_patch(data)
		# print 'Average time per bug:', 
        r[12]=avg_time_per_bug(data)
        
        for i in range(len(r)):
            worksheet.write(row,col,r[(i-1)%14])
            row+=1
        col+=1
        
        
        
    workbook.close()
        
generate_stats()

 

    
    
# if len(sys.argv) < 2:
	# print 'Error: missing json files'
	# print 'Usage: python stats.py [report.json]'
	# sys.exit()

# files = sys.argv[1:]
# for f in files:
	# try:
		# path = os.getcwd() + '/Data/' + f
		# print path
		# raw_json_data = open(path)
		# data = json.load(raw_json_data)
		# print 'Extracting data from ', f, '...'
		# print 'Stats:'
		# print 'Number of bugs:', numberOfBugs(data)
		# print 'Number of bugs with patch:', numberOfBugsWithPatch(data)
		# print 'Average number of comments per bug:', avg_comments(data)
		# print 'Max number of comments per bug:', max_comments(data)
		# print 'Average number of patches per bug:', avg_patches(data)
		# print 'Max number of patches per bug:', max_patches(data)
		# print 'Average number of developers per bug:', avg_developers(data)
		# print 'Max number of developers per bug:', max_developers(data)
		# print 'Average lines of code added per bug:', avg_code_added_per_bug(data)
		# print 'Average lines of code added for patched bugs:', avg_code_added_per_bug_with_patch(data)
		# print 'Average lines of code deleted per bug:', avg_code_deleted_per_bug(data)
		# print 'Average lines of code deleted for patched bugs:', avg_code_deleted_per_ bug_with_patch(data)
		# print 'Average time per bug:', avg_time_per_bug(data)
	# except Exception, e:
		# raise e
