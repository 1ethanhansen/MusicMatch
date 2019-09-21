import os
import json
import random

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
        # print(people)

with open(filename, "w+") as file_bytes:
    human_name = input("What is your name? ")
    if human_name in people.keys():
        print("Got it! You like...")
        for song in people[human_name]:
            print(song)
    else:
        random_song_choice = random.choice(list(people.values()))
        print("Ah, you're new here? Please give a song you enjoy in the format 'song name - artist'")
        song = input("Here's an example: {} ".format(random_song_choice))
        people[human_name] = [song]

    json.dump(people, file_bytes)
