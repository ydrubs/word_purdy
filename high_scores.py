def load_high_scores():
    scores = []
    names = []
    count = 0
    # Open the file in read mode
    with open('high_score_data.txt', 'r') as file:
        # Create an empty list to store the lines
        # Iterate over the lines of the file
        for score in file:
            # Remove the newline character at the end of the line
            score = score.strip()
            # line = line.rstrip(':').split(':')
            if count < 5:
                # print(re.split(':|\n', line))

                # Append the line to the list
                scores.append(int(score))
                count += 1

            if count > 4:
                count += 1
                # print(re.split(':|\n', line))

                # Append the line to the list
                names.append(score)
    del names[0]
    scores.sort(reverse=True)
    return scores,names


# new_var = 40

# if new_var > min(scores):
#     scores.remove(min(scores))
#     scores.append(new_var)
#
# scores.sort()
# print(scores)

def write_data(scores, names):
    # open file in write mode
    with open('high_score_data.txt', 'w') as file:
        for item in scores:
            # write each item on a new line
            file.write("%s\n" % item)

        for item in names:
            # write each item on a new line
            file.write("%s\n" % item)
        # print('Done')


