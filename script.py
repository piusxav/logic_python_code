import sys
import re
import logging

if len (sys.argv) != 2 :
    print ("Usage: python script.py inputfile")
    sys.exit (1)
	
print ("testing")
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

				
print (outline_list)
print (subline_list)


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
 
print (outline_indexed_list)
# to insert + or - based on count of the dots


	
