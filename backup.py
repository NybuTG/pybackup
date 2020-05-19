import os
import argparse
import csv


important = "/home/nybu/important.csv"
home = "/home/nybu/"
exclude = "/home/nybu/exclude.csv"
nas = "/mnt/nas/home/nybu/"

# Detect if the "important.csv" exists.
if os.path.isfile(important) is True and os.path.isfile(exclude) is True:

    # If the file exists, open it.
    with open(important) as f:
        reader_imp = csv.reader(f)
        data_imp = list(reader_imp)

    # Make the lists in lists into a single flat list.
    important_list = []
    for sublist in data_imp:
        for item in sublist:
            important_list.append(item)

    # Open the Exclude file
    with open(exclude) as f:
        reader_exc = csv.reader(f)
        data_exc = list(reader_exc)

    # Make the multi list into a flat list
    exclude_list = []
    for sublist in data_exc:
        for item in sublist:
            exclude_list.append(item)

    # Add a bunch of arguments to determine which files to backup, which are used like "command --argument"
    parser = argparse.ArgumentParser()

    parser.add_argument("--important", "-i", help="Send all important files to the Pi-NAS", action="store_true")
    parser.add_argument("--all", "-a", help="Send whole \"~\" folder to NAS - Takes the Longest", action="store_true")
    parser.add_argument("--development", "-d", help="Send the whole \"~/development\" folder to the Pi-NAS",
                        action="store_true")

    args = parser.parse_args()

    # Check which files to use,
    # determined by which argument was used
    if args.all is True:
        if os.path.isfile(exclude) is True:
            print("Copying files to \"~\" directory...")
            os.system("rsync -a " + home + " " + nas + " " + str(exclude_list).replace
            ("[", "").replace("]", "").replace(",", "").replace("'", ""))
            print("Backup finished!")

        else:
            print("First time time launch detected. Making \"exclude.csv\" in your home directory")
            file = open(exclude, "w")

    elif args.important is True:
        backed_up_files = str(important_list)
        print("Backing up {}...".format(backed_up_files.replace("[", "")).replace("]", ""))
        os.system("cp -r -a " + str(important_list).replace("[", "").replace
        ("]", "").replace(",", "").replace("'", "") + " " + nas)
        print("Backup finished!")

    elif args.development is True:
        print("Backing up development files...")
        os.system("cp -r /home/nybu/development " + nas + "development")
        print("Backup finished!")

# Make the "important.csv" file if it doesnt exist at the given location
else:
    print("First time time launch detected. Making \"important.csv\" and \"exclude.csv\" in your home directory")
    file = open(important, "w")
    file2 = open(exclude, "w")
