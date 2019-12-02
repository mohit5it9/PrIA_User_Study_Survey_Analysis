import csv
import sys

arr = list()
filename = sys.argv[1]
with open(filename, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        arr.append(row["Results"])
        line_count += 1


# initialize constants
NUM_ROWS = 6
NUM_COLS = 5
NEGATIVE = 0
SLIGHTLY_NEGATIVE = 1
NEUTRAL = 2
SLIGHTLY_POSITIVE = 3
POSITIVE = 4
DONT_CARE = 5

# initialize Mappings Hash Map
hashMap = {0: "`Negative`",
1: "`Slightly Negative`",
2: "`Neutral`",
3: "`Slightly Positive`",
4: "`Positive`",
5: "`Do not Care`"}

# initialize confident Matrix
confidentMatrix = [[0 for j in range(5)] for i in range(6)]

print "======================================================="
print "Total number of Users (not unique) Responded: ", line_count
print "======================================================="
print

surveys_filled = 0
for response in arr:
	for res in response.split(","):
		if res == "" or len(res) < 2:
			continue
		splitedResponse = res.split("-")
		predicted = int(splitedResponse[0]) - 1
		actual = splitedResponse[1]
		if actual[0] == "x" and len(actual) != 1:
			actual = int(actual[1:]) - 1
		elif actual[0] == "x" and len(actual) == 1:
			actual = DONT_CARE
		else:
			actual = int(actual) - 1
		surveys_filled += 1
		confidentMatrix[actual][predicted] += 1

print "======================================================="
print "Total number of Surveys Recorded by those users: ", surveys_filled
print "======================================================="
print

true_positives = confidentMatrix[0][0] + confidentMatrix[1][1] + confidentMatrix[2][2] + confidentMatrix[3][3] + confidentMatrix[4][4]

false_positives = 0
TP = [confidentMatrix[0][0], confidentMatrix[1][1], confidentMatrix[2][2], confidentMatrix[3][3], confidentMatrix[4][4]]
FP = list()
FN = list()
TN = list()
for row in range(NUM_COLS):
	false_positives = 0
	for col in range(NUM_COLS):
		false_positives += confidentMatrix[row][col]
	false_positives -= confidentMatrix[row][row]
	FP.append(false_positives)

false_negatives = 0
for col in range(NUM_COLS):
	false_negatives = 0
	for row in range(NUM_ROWS):
		false_negatives += confidentMatrix[row][col]

	false_negatives -= confidentMatrix[col][col]
	FN.append(false_negatives)

true_negatives = 0
for i in range(NUM_COLS):
	true_negatives = 0
	for l in range(NUM_COLS):
		for k in range(NUM_COLS):
			true_negatives += confidentMatrix[l][k]
	true_negatives -= (TP[i] + FP[i] + FN[i])
	TN.append(true_negatives)

print "============================================================================================================================="
print "The confidentMatrix for filename: "+ filename + " is given below"
print confidentMatrix
print "============================================================================================================================="
print

print "======================================================="
print "True Positives are: ", TP
print "True Negatives are:", TN
print "False Positives are:", FP
print "False Negatives are:", FN
print "======================================================="

for idx in range(5):
	print "For class", hashMap[idx], "precision is",
	precision = float(confidentMatrix[idx][idx])/float((confidentMatrix[idx][idx]+FP[idx]))
	print precision,
	print "and recall is",
	recall = float(TP[idx])/float((TP[idx]+FN[idx]))
	print recall,
	print "and accuracy is",
	accuracy = float(TP[idx]+TN[idx])/float((TP[idx]+FN[idx]+FP[idx]+TN[idx]))
	print accuracy,
	print "and F-1 Score is",
	f1 = float(2*precision*recall)/(float(recall+precision))
	print f1
	print "============================================================================================================================================="
