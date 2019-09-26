# Import all the needed things
import os
import json
import csv
from itertools import chain, combinations

# Set it up with my basic info for a storage variable
people = {"ethan": ["my life - billy joel"]}

# Get the name of the .json file (database) to load
filename = input("Enter the database (.json file) to load or create: ")

# Make sure the file has the extension ".json"
if filename[-5:] != ".json":
    print("Database MUST be a .json file")
    print("Instead got file type: {}".format(filename[-5:]))
    exit(1)

# Make sure the file actually exists, otherwise we can't load
if os.path.exists(filename) is True:
    print("Found it! Reading now...")
    with open(filename, 'r') as file_bytes:
        people = json.load(file_bytes)
        print("Database loaded")

# Open the .json file or create it if it doesn't exist
with open(filename, "w+") as file_bytes:
    # There are no do-while loops in python, so do forever, unless we break w/ ## flag
    while True:
        human_name = input("What is your name? (or ## to exit or $$ to analyze) ").lower()
        if human_name == "##":
            break

        if human_name == "$$":
            # Get all of the possible groups (superset w/o sets of length 0 and 1)
            all_people = list(people.keys())
            all_groups = list(chain.from_iterable(combinations(all_people, r) for r in range(2, len(all_people) + 1)))
            # Reverse so that we do the bigger ones first
            all_groups.reverse()

            # Storage variable that hold groups where people have at least 1 shared song
            working_groups = {}

            # Iterate over all of the sets in the superset looking for music commonalities
            for group in all_groups:
                duplicate = False
                # Since it is impossible for 1,2 to not be a working group when 1,2,3 is, ignore the smaller ones
                for wg in list(working_groups.keys()):
                    if set(group).issubset(set(wg)):
                        duplicate = True
                        break
                if not duplicate:
                    # Get all of the songs from the first person for a starting place
                    remaining_songs = people[group[0]]
                    # For each of the rest of the people, look for commonalities in the songs shared by others in the group
                    for num in range(1, len(group)):
                        # Keep only the songs that were in the songs everyone else liked, and this person liked
                        remaining_songs = list(set(remaining_songs).intersection(people[group[num]]))
                        # If we hit 0 songs, yeet out of the loop immediately
                        if remaining_songs == 0:
                            break
                    # If there were any songs the whole group liked, add to list of working groups
                    if len(remaining_songs) > 0:
                        working_groups[group] = len(remaining_songs)

            # Get the average group size and all the group sizes
            average_group_size = 0
            all_the_numbers = []
            for wg in list(working_groups.keys()):
                average_group_size += len(wg)
                all_the_numbers.append(len(wg))

            # Sanity check (you might have just created the database)
            if len(working_groups) > 0:
                average_group_size /= len(working_groups)
            else:
                average_group_size = 1

            print("\nThe average group size for the population '{}' is {} \n".format(filename[:-5], average_group_size))

            # if the user wants it, dump all the numbers into a CSV file
            print_all_data_q = input("Do you want me to print all the group sizes for further analysis? (Y/n) ").lower()
            if print_all_data_q == "y":
                with open("results.csv", "w+") as results_file:
                    writer = csv.writer(results_file)
                    for num in all_the_numbers:
                        writer.writerow([num])

        # If the entered name already exists in the database, display existing data
        elif human_name in people.keys():
            # Show all the songs in this person's list
            print("Got it! You like...")
            humans_songs = people[human_name]
            for song in humans_songs:
                print("\t" + song)

            # Show the songs that are in other people's lists, but not this person's list
            print("Here are songs other people like (in order of popularity): ")
            # Take all of the songs from all of the people and turn it into a single list
            flat_list = [item for sublist in list(people.values()) for item in sublist]
            # Remove all of the songs that this person already likes and all of the duplicates
            others_list = list(set(flat_list) - set(humans_songs))
            sortable_list = []

            # Add a tuple to the list with the song name and # of times it appears, then sort by that number
            for song in others_list:
                sortable_list.append((song, flat_list.count(song)))
            sortable_list.sort(key=lambda tup: tup[1], reverse=True)

            # Print all the songs from most popular to least
            for song in sortable_list:
                print("\t" + song[0])

            # Get the user's input on what song they would like to add
            print("Feel free to copypaste one in or enter a new song in the format "
                  "'song name - artist' or leave blank to continue")
            new_song = input().lower()
            # If the new song isn't blank, add it to their list
            if len(new_song) != 0:
                people[human_name].append(new_song)
        # If this is a new person, get at least one song from them that they like
        else:
            # Show all of the songs in everyone else's lists
            print("Ah, you're new here?")
            print("Here are songs other people like (in order of popularity): ")

            # Take all of the songs from all of the people and turn it into a single list
            flat_list = [item for sublist in list(people.values()) for item in sublist]
            # Remove all of the duplicates
            simple_list = list(set(flat_list))
            sortable_list = []

            # Add a tuple to the list with the song name and # of times it appears, then sort by that number
            for song in simple_list:
                sortable_list.append((song, flat_list.count(song)))
            sortable_list.sort(key=lambda tup: tup[1], reverse=True)

            # Print all the songs from most popular to least
            for song in sortable_list:
                print("\t" + song[0])

            # Get the new user's input on what song to add
            print("Copypaste one in or, if you don't like any, enter a new song in the format 'song name - artist'")
            new_song = input().lower()
            if len(new_song) != 0:
                people[human_name] = [new_song]

    json.dump(people, file_bytes)



# get user name
# look for name in all lists
# if found:
#   give list of liked songs
# else:
#   give list of popular songs
# get name of song from user
# add user's name to list of that song