import requests
import csv
import sys

# Global functions
def read_csv_into_list(filename):
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Assuming there is only one row in the CSV file
        for row in csv_reader:
            return row

def write_list_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

def find_matching_items(list1, list2):
    return list(set(list1) & set(list2))

def remove_matching_items(list1, list2):
    return [item for item in list1 if item not in list2]

def submit_creator(input_csv):
    url = "https://dev.creatordb.app/v2/submitCreators"

    payload = {
        "platform": "youtube",
        "platformUserIds": read_csv_into_list(input_csv)
    }

    headers = {
        "apiId": sys.argv[1],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print("Submitting creators to DB...")
    response = requests.post(url, json=payload, headers=headers)
    api_output = response.json()

    return api_output, payload

def find_yt_creator_in_db(creator):
    url = "https://dev.creatordb.app/v2/youtubeBasic"

    querystring = {"youtubeId": creator}

    headers = {
        "apiId": sys.argv[1],
        "Accept": "application/json"
    }

    print("Checking if {} is in DB...".format(creator))
    response = requests.get(url, headers=headers, params=querystring)
    api_output = response.json()

    return api_output

def separate_creators():
    # Initialise list of creators already in DB and list of invalid IDs
    list_of_creators_in_db = []
    list_of_invalid_ids = []

    for creator in submit_creator_payload['platformUserIds']:
        api_output = find_yt_creator_in_db(creator)

        # If the creator in the list is not in DB, append to list_of_invalid_ids
        if api_output['success'] == False:
            list_of_invalid_ids.append(creator)
        # If the creator in the list is in the DB, append to list_of_creators_in_dv
        else:
            list_of_creators_in_db.append(creator)

    return list_of_creators_in_db, list_of_invalid_ids

# Submit a creator and get payload which contains list of people to add
submit_creator_api_output, submit_creator_payload = submit_creator('input.csv')

# Get separated lists
list_of_creators_in_db, list_of_invalid_ids = separate_creators()

# Get list of IDs added succesfully
list_of_ids_added_successfully = find_matching_items(submit_creator_payload['platformUserIds'], submit_creator_api_output['data'])

# Get list of invalid IDs
list_of_invalid_ids = remove_matching_items(list_of_invalid_ids, list_of_ids_added_successfully)

# Show which data has been successfully added
print("\nIDs successfully added to DB: " + str(list_of_ids_added_successfully))
print("No. of IDs successfully added to DB: " + str(len(list_of_ids_added_successfully)) + "\n")
print("IDs already in DB: " + str(list_of_creators_in_db))
print("No. of IDs already in DB: " + str(len(list_of_creators_in_db)) + "\n")
print("Invalid IDs: " + str(list_of_invalid_ids))
print("No. of invalid IDs: " + str(len(list_of_invalid_ids)))

# Writing the matching_items list to a CSV file
write_list_to_csv(list_of_ids_added_successfully, 'ids_added_successfully.csv')

# Writing the matching_items list to a CSV file
write_list_to_csv(list_of_creators_in_db, 'creators_in_db.csv')

# Writing the matching_items list to a CSV file
write_list_to_csv(list_of_invalid_ids, 'invalid_ids.csv')
