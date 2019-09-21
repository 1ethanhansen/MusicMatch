import os
import json
import random
from itertools import chain, combinations

people = {"ethan": ["my life - billy joel"]}

filename = input("Enter the database (.json file) to load or create: ")

if filename[-5:] != ".json":
    print("Database MUST be a .json file")
    print("Instead got file type: {}".format(filename[-5:]))
    exit(1)

if os.path.exists(filename) is True:
    print("Found it! Reading now...")
    with open(filename, 'r') as file_bytes:
        people = json.load(file_bytes)
        print("Database loaded")
else:
    print("That's a bummer! {} doesn't exist. Check for typos? IDK".format(filename))
    exit(2)

with open(filename, "w+") as file_bytes:
    while True:
        human_name = input("What is your name? (or ## to exit) ").lower()
        if human_name == "##":
            break

        if human_name in people.keys():
            print("Got it! You like...")
            humans_songs = people[human_name]
            for song in humans_songs:
                print("\t" + song)
            print("Here are songs other people like: ")
            others_list = list(set([item for sublist in list(people.values()) for item in sublist]) - set(humans_songs))
            for song in others_list:
                print("\t" + song)
            print("Feel free to copypaste one in or enter a new song in the format "
                  "'song name - artist' or leave blank to continue")
            new_song = input().lower()
            if len(new_song) != 0:
                people[human_name].append(new_song)
        else:
            random_song_choice = random.choice(random.choice(list(people.values())))
            print("Ah, you're new here?")
            print("Here are songs other people like: ")
            simple_list = list(set([item for sublist in list(people.values()) for item in sublist]))
            for song in simple_list:
                print("\t" + song)

            print("Feel free to copypaste one in or enter a new song in the format 'song name - artist'")
            new_song = input().lower()
            if len(new_song) != 0:
                people[human_name] = new_song

        all_people = list(people.keys())
        all_groups = list(chain.from_iterable(combinations(all_people, r) for r in range(2, len(all_people) + 1)))
        all_groups.reverse()

        working_groups = {}

        for group in all_groups:
            remaining_songs = people[group[0]]
            for num in range(1, len(group)):
                remaining_songs = list(set(remaining_songs).intersection(people[group[num]]))
            if len(remaining_songs) > 0:
                original = True
                for wg in list(working_groups.keys()):
                    if set(group).issubset(set(wg)):
                        original = False
                if original:
                    working_groups[group] = len(remaining_songs)

        average_group_size = 0
        for wg in list(working_groups.keys()):
            average_group_size += len(wg)
        average_group_size /= len(working_groups)

        print("\nThe average group size for the population '{}' is {} \n".format(filename[:-5], average_group_size))

    json.dump(people, file_bytes)
