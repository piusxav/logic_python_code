import sys
import re
import logging

if len (sys.argv) != 2 :
    print ("Usage: python script.py inputfile")
    sys.exit (1)
	
program_name = sys.argv[0]
input_file = sys.argv[1]

pattern_list = ['*','.']
outline_list = []
subline_list = []
outline_count_list = []
subline_count_list = []

with open(input_file) as fp:
	line = fp.readline()
	while line:
		line_content_list = []
		pattern = line[0]	
		count = line.count(pattern)
		if pattern == '*':
			outline_count_list.append(count)
			line_content_list = line.split(pattern)	
			extracted_line = line_content_list[-1]
			outline_list.append(extracted_line)
		if pattern == '.':
			subline_count_list.append(count)
			line_content_list = line.split(pattern)	
			extracted_line = line_content_list[-1]
			subline_list.append(extracted_line)
		line = fp.readline()

				
logging.debug (outline_list)
logging.debug (subline_list)


def return_outline_index(prev_index,count,occurance,prev_count):
	logging.debug("{} {} {} {}".format(prev_index,count,occurance,prev_count))
	index_string = str(prev_index)
	if (count < 2 and occurance >= 1):
		num_last = index_string.split(".")
		index_string = str(int(num_last[0]) + 1)
	elif (count < prev_count and occurance == 1):
		num_last = index_string.split(".")
		for i in range(0,(prev_count-count)):
			del num_last[-1]
		num = int(num_last[-1]) + 1
		index_string = '.'.join(num_last[0:-1]) + "." + str(num)
	elif (count > 1 and occurance == 1):
		index_string = index_string + "." + str(occurance)
	else:
		num_last = index_string.split(".")
		num = int(num_last[-1]) + 1
		index_string = '.'.join(num_last[0:-1]) + "." + str(num)
	return index_string

index = 0
occurance = 1
prev_index = 0
prev_count = outline_count_list[0]
outline_indexed_list = []
for items in outline_list:
	prev_index = return_outline_index(prev_index,outline_count_list[index],occurance,prev_count)
	outline_indexed_list.append("{}{}".format(prev_index,outline_list[index]))
	prev_count = outline_count_list[index]
	if  outline_count_list[index] != outline_count_list[-1]:
		if outline_count_list[index] == outline_count_list[index+1]:
			occurance += 1
		else:
			occurance = 1
	index+=1

# To insert + or - based on count of the dots
# TODO: Need to fix the ordering of the  +/- logic. is broken for now
def return_subline_index(count,occurance,prev_count):
	logging.debug("{} {} {}".format(count,occurance,prev_count))
	tab_string = ""
	for index in range(0,count):
		tab_string += " "
	if count > prev_count:
		tab_string += "+"
	elif occurance == 1 or count == prev_count:
		tab_string += "-"
	return tab_string	

index = 0
occurance = 1
prev_count = subline_count_list[0]
subline_indexed_list = []
for items in subline_list:
	tab_string = return_subline_index(subline_count_list[index],occurance,prev_count)
	subline_indexed_list.append("{}{}".format(tab_string, subline_list[index]))
	prev_count = subline_count_list[index]
	if  subline_count_list[index] != subline_count_list[-1]:
		if subline_count_list[index] == subline_count_list[index+1]:
			occurance += 1
		else:
			occurance = 1
	index+=1

# final crude multiplexing logic
with open(input_file) as fp:
	line = fp.readline()
	while line:
		out_index = 0
		sub_index = 0
		for item in outline_list:
			if re.search(r"%s"%item,line):
				print(outline_indexed_list[out_index])
			out_index +=1
		for item in subline_list:
			if re.search(r"%s"%item,line):
				print(subline_indexed_list[sub_index])
			sub_index +=1
		line = fp.readline()
		


	
