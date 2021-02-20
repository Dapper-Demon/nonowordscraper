# Written by pantherrr in 1 hour to show RGL how easy it is to do this shit

import urllib.request
import datetime
import json
import os.path

def scrapePlayer(steamID64, steam3ID, words):
    # Make the URL for the search for log IDs limiting the search to the 20 most recent logs
    allOfPlayersLogs = "http://logs.tf/api/v1/log?player=" + steamID64 + "&limit=20"

    # Output file. If it doesn't exist then it makes one
    out = open("./out.txt", "a")

    # Ask logs.tf for all of the logs for a person
    with urllib.request.urlopen(allOfPlayersLogs) as allLogs:
        allLogsData = json.loads(allLogs.read().decode())

        # Loop over all of the logs so that we can get to each one
        for log in allLogsData["logs"]:
            # Make the URL for the individual log request
            individualLogURL = "http://logs.tf/api/v1/log/" + str(log["id"])

            # Get into the individual log
            with urllib.request.urlopen(individualLogURL) as individualLog:
                logData = json.loads(individualLog.read().decode())

                # Go through all of the chats in the log
                for msg in logData["chat"]:
                    
                    # Check for people that we are scraping
                    if msg["steamid"] == steam3ID:
                        
                        # Make sure that none of the no no words are in the message
                        for word in words:
                            
                            # If we find a no no word then we output the log and message to the output file
                            if word in msg["msg"]:
                                outData = msg["name"] + ": " + msg["msg"] + "\n" + "http://logs.tf/" + str(log["id"]) + "#" + str(steamID64) + "\n\n"
                                out.write(outData)

    # Close the output file
    out.close()

def main():
    # Check that the IDs and badwords text files exist
    if not os.path.exists("./ids.txt"):
        print("Missing ids.txt to read steam IDs from")
        return
    if not os.path.exists("./badwords.txt"):
        print("Missing badwords.txt to read no no words from")
        return
    
    # Get the players we are scraping and the no no words
    playerIDs = open("./ids.txt", "r").readlines()
    words = open("./badwords.txt", "r").readline().split(" ")

    # Write the current date and time in output.txt
    dateString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
    open("./out.txt", "a").write(dateString)

    # Go through every player one at a time
    for IDs in playerIDs:
        currentPlayer = IDs.replace("\n", "").split(" ")
        scrapePlayer(currentPlayer[0], currentPlayer[1], words)

    open("./out.txt", "a").write("-------------------------------------------------------------\n")

if __name__ == "__main__":
    main()