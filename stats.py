# Python script that extract basic stats about bug reports
# Reports must be in json format

import json
import sys
import os
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

if len(sys.argv) < 2:
	print 'Error: missing json files'
	print 'Usage: python stats.py [report.json]'
	sys.exit()

files = sys.argv[1:]
for f in files:
	try:
		path = os.getcwd() + '/Data/' + f
		print path
		raw_json_data = open(path)
		data = json.load(raw_json_data)
		print 'Extracting data from ', f, '...'
		print 'Stats:'
		# number of bugs
		print 'Number of bugs:', numberOfBugs(data)
		# number of bugs with patch:
		print 'Number of bugs with patch:', numberOfBugsWithPatch(data)
		# average number of comments
		print 'Average number of comments per bug:', avg_comments(data)
		# max number of comments
		print 'Max number of comments per bug:', max_comments(data)
		# average number of patches
		print 'Average number of patches per bug:', avg_patches(data)
		# max number of patches
		print 'Max number of patches per bug:', max_patches(data)
		# average number of developers
		print 'Average number of developers per bug:', avg_developers(data)
		# max number of developers
		print 'Max number of developers per bug:', max_developers(data)
		# average number of lines added per bug
		print 'Average lines of code added per bug:', avg_code_added_per_bug(data)
		# average number of lines added per bug with patch
		print 'Average lines of code added for patched bugs:', avg_code_added_per_bug_with_patch(data)
		# average number of lines deleted per bug
		print 'Average lines of code deleted per bug:', avg_code_deleted_per_bug(data)
		# average number of lines deleted per bug
		print 'Average lines of code deleted for patched bugs:', avg_code_deleted_per_bug_with_patch(data)
		# average time per bug
		print 'Average time per bug:', avg_time_per_bug(data)
	except Exception, e:
		raise e
