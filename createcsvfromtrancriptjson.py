""" Produce CSV Document from AWS Transcribe JSON - ONLY SUPPORTS MULTI SPEAKER. """

import json, datetime
import statistics
import csv
import sys
import os
from pathlib import Path
from time import perf_counter

def convert_time_stamp(n):
    """ Function to help convert timestamps from s to H:M:S """
    ts = datetime.timedelta(seconds=float(n))
    ts = ts - datetime.timedelta(microseconds=ts.microseconds)
    return str(ts)


""" Write a transcript from the .json transcription file. """

file = sys.argv[1]

start = perf_counter()

# Load Transcription output
json_filepath = Path(file)
assert json_filepath.is_file(), "JSON file does not exist"
data = json.load(open(json_filepath.absolute(), "r", encoding="utf-8"))
assert data["status"] == "COMPLETED", "JSON file not shown as completed."


# Save
filename = f"{data['jobName']}.csv"
with open(filename, 'w', newline='') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(["Time In", "Time Out", "Duration", "Speaker", "Content"])


	# If speaker identification
	if "speaker_labels" in data["results"].keys():

		# A segment is a blob of pronounciation and punctuation by an individual speaker
		for segment in data["results"]["speaker_labels"]["segments"]:
			Cells = ["", "", "", "", ""]

			# If there is content in the segment, add a row, write the time and speaker
			if len(segment["items"]) > 0:
				Cells[0] = convert_time_stamp(segment["start_time"])
				Cells[1] = convert_time_stamp(segment["end_time"])
				Cells[2] = convert_time_stamp(float(segment["end_time"]) - float(segment["start_time"]))
				Cells[3] = str(segment["speaker_label"])

				# For each word in the segment...
				for word in segment["items"]:

					# Get the word with the highest confidence
					pronunciations = list(filter(lambda x: x["type"] == "pronunciation", data["results"]["items"]))
					word_result = list(filter(lambda x: x["start_time"] == word["start_time"] and x["end_time"] == word["end_time"], pronunciations))
					result = sorted(word_result[-1]["alternatives"], key=lambda x: x["confidence"])[-1]

					# Write the word
					Cells[4] = Cells[4] + (" " + result["content"])

					# If the next item is punctuation, write it
					try:
						word_result_index = data["results"]["items"].index(word_result[0])
						next_item = data["results"]["items"][word_result_index + 1]
						if next_item["type"] == "punctuation":
							Cells[4] = Cells[4] + (next_item["alternatives"][0]["content"])
					except IndexError:
						pass
				
				csvwriter.writerow(Cells)


# # Else no speaker identification
# else:

#     # Start the first row
#     row_cells = table.add_row().cells

#     # Add words
#     for word in data["results"]["items"]:

#         # Get the word with the highest confidence
#         result = sorted(word["alternatives"], key=lambda x: x["confidence"])[-1]

#         # Write the word
#         run = row_cells[2].paragraphs[0].add_run(" " + result["content"])
#         if float(result["confidence"]) < threshold_for_grey:
#         	font = run.font
#         	font.color.rgb = RGBColor(204, 204, 204)

#         # If the next item is punctuation, write it
#         try:
#         	word_result_index = data["results"]["items"].index(word)
#         	next_item = data["results"]["items"][word_result_index + 1]
#         	if next_item["type"] == "punctuation":
#         		run = row_cells[2].paragraphs[0].add_run(next_item["alternatives"][0]["content"])
#         	except IndexError:
#         		pass


finish = perf_counter()
duration = round(finish - start, 2)

print(f"Transcript {filename} writen in {duration} seconds.")
