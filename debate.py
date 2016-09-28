import nltk, time, operator

def main():

	# Start timer
	t = time.time()

	# Open up debate transcript
	# Source is Fortune Magazine
	transcript = open('debate.txt', 'r').readlines()

	input_length = sum(1 for line in transcript if line.strip())
	print "Total lines:", input_length

	# Divide up the transcript by speaker
	trump, clinton = divide(transcript)
	print 'Trump spoke ' + str(len(trump)) + ' times\n' + 'Clinton spoke ' + str(len(clinton)) + ' times\n'

	# Count pronouns for each speaker
	trump_ct = pro_count(trump)
	clinton_ct = pro_count(clinton)

	# Output results
	print 'Trump said:'
	pretty_print(trump_ct)

	print '\nClinton said:'
	pretty_print(clinton_ct)

	# Analytics lol
	print "\nThis took ", '%.5s' % (time.time()-t), "seconds"

# Print the dict output
def pretty_print(ct):
	sorted_ct = sorted(ct.items(), key=lambda x: x[1])
	sorted_ct.reverse()

	for k, v in sorted_ct:
		# arbitrary right aligning at 12 chars
		width = 12-len(k)
		print ' ', k ,'%s' % (str(v).rjust(width))

# TODO - just using split windows for now
def pretty_print2(c,t):
	sorted_trump = sorted(t.items(), key=lambda x: x[1])
	sorted_clinton = sorted(c.items(), key=lambda x: x[1])

	for k, v in sorted_trump:
		width = 12-len(k)
		print ' ', k ,'%s' % (str(v).rjust(width)), '\t'

# Divide up speaking by speaker
def divide(transcript):

	trump = []
	clinton = []
	else_ct = 0

	# 0 indicates not set, 1 indicates trump, 2 indicates clinton
	baton = 0

	# Look at each line
	for i in transcript:
		line = i.split()

		# Get the first word of the line
		candidate = line[0]

		# Cut off the first word if it's speaker
		says = line[1:len(line)-1]

		if candidate == 'TRUMP:':
			
			trump.append(says)

			baton = 1

		elif candidate == 'CLINTON:':
			clinton.append(says)
			baton = 2

		# Eliminate Lester and commentary
		else:
			if candidate == 'HOLT:' or candidate[0] == '(':
				else_ct = else_ct + 1
				baton = 0
			# If neither the first word begins a paragraph that trump or clinton is saying
			# Check the baton for attribution
			else:
				if baton == 1:
					trump.append(line)
				elif baton == 2:
					clinton.append(line)
				else:
					continue

	return trump, clinton

# Pulled from big_head
def pro_count(candidate):

	countDict = {"me":0, "my":0, "i":0, "mine":0, "myself":0,
             "she":0, "her":0, "hers":0, "herself":0,
             "he":0, "him":0, "his":0, "himself":0,
             "they":0, "them":0, "their":0, "themselves":0,
             "we":0, "us":0, "our":0, "ours":0, "ourselves":0,
             "you":0, "your":0, "yours":0, "yourself":0, "y'all":0}
	
	# Count pronouns
	for line in candidate:
		for word in line:
			word = word.lower()

			# Deal with abbreviations
			if "'" in word:
				word = word[:word.index("'")]

			# Increment pronouns in the dict
			if word in countDict:
				countDict[word] = countDict[word] + 1
	     
	# Todo - this is interesting but there's definitely a better way to do it   
	first_person = countDict["me"] + countDict["my"] + countDict["i"] + countDict["mine"] + countDict["myself"]
	first_person_plural = countDict["we"] + countDict["us"] + countDict["our"] + countDict["ours"] + countDict["ourselves"]
	second_person = countDict["you"] + countDict["your"] + countDict["yours"] + countDict["yourself"] + countDict["y'all"]
	third_person_f = countDict["she"] + countDict["her"] + countDict["hers"] + countDict["herself"]
	third_person_m = countDict["he"] + countDict["him"] + countDict["his"] + countDict["himself"]
	third_person_plural = countDict["they"] + countDict["them"] + countDict["their"] + countDict["themselves"]

	return countDict
	
main()
