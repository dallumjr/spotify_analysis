import csv
from collections import OrderedDict

def get_email_from_input():
    return input("Enter Spotify username: ")

def get_details_for_saved_tracks(spot_obj, func):
    '''
    add option to map_genres_to_track_id or to create_feature_dict_row
    '''
    track_arr = []
    results = spot_obj.current_user_saved_tracks()
    while results['next']:
        track_arr = func(results, spot_obj, track_arr, results['offset'], results['total'])
        results = spot_obj.next(results)
    # edge case:
    # if (results['offset']-results['total'])%20 != 0:
    results = spot_obj.current_user_saved_tracks(offset=results['offset']+1)
    track_arr = func(results, spot_obj, track_arr ,results['offset'],results['total'])
    return track_arr

def create_feature_dict_row(results, spot_obj, track_f, offset, size):

    for item in results['items']:
        print(str(offset/size*100//1) + '% Completed', end="\r")
        feature_dict = OrderedDict()
        feature_dict['id'] = item['track']['id']
        feature_dict['name'] = item['track']['name']
        feature_dict['added_at'] = item['added_at']
        feature_dict.update(spot_obj.audio_features(item['track']['id'])[0])
        track_f.append(feature_dict)
    return track_f


def map_genres_to_track_id(results, spot_obj, track_g, offset, size):

    for item in results['items']:
        print(str(offset/size*100//1) + '% Completed', end="\r")
        track_genres = set()
        # loop through artists on a track
        for artist in item['track']['artists']:

            for genre in (spot_obj.artist(artist['id'])['genres']):
                genre_map = OrderedDict()
                if genre not in track_genres:
                    genre_map['id'] = item['track']['id']
                    genre_map['genre'] = genre
                    track_g.append(genre_map)
                    track_genres.add(genre)
    return track_g


# Create a CSV file for each metric, so that it can be analyzed with Pandas
def create_analysis_csv(saved_tracks,file_name):
	'''
	Takes in an array of dictionaries then creates a csv file with the features as headers
	@source: root of xml tree element
	'''
	new_csv = open(file_name + '.csv', 'w', newline='', encoding='utf-8')
	# Make a csv writer instance for the new file
	csvwriter = csv.writer(new_csv)
	# Write the data
	write_csv_rows(saved_tracks, csvwriter)
	# Close the file
	new_csv.close()



def write_csv_rows(saved_tracks, writer):
	'''
	Takes in a csvwriter and creates the appropriate headers and inputs data row by row.
    @saved_tracks: list of OrderedDicts containing track features
	@writer: csvwriter
	'''
	# create an array for the column names serve as headers for the csv
	col_names = []
	# iterate through all the saved tracks
	for track in saved_tracks:
		# create new row each time
		new_row = []
			# check to see if there are headers
		if len(col_names) == 0:
			# if not, go through the keys of the tag we are at that matches our tag_attr, and add the keys to the header
			for key in track:
				col_names.append(key)
			# write the new row
			writer.writerow(col_names)
		# always add the data that is available
		for key in col_names:
			new_row.append(track[key])
		# write the new row to the file
		writer.writerow(new_row)
