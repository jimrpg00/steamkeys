# Steam Keys

Steam Keys is a game key exchange application. It operates on users donating and taking spare cdkeys in good faith. 

# Intro

Built using Python 3 programming language, using Discord/Discord Bot API as the medium for users to interact and FireStore (Google) as the realtime database/persistent store for the keys. The application is designed around these platforms (free to use) with the exception of FireStore which charges based on usage. If you're a developer consider to build logic or enforce database rules to avoid these additional charges. In this project, a limit of 5 keys is place per user per day.

Feel free to modify, share, improve this script.

# Accompanying Tools
Under the tools folder, use the `addKeys.py` or `deleteKeys.py`. Use these tools once you've set up the Firestore database and setup your credentials

Adding keys usses the keys.txt file with the following format. Please organise your keys in the same manner delimited by the pipe character `|`.

    Abyss Odyssey|VPHIY-8KWJK-0AFI3			
    Age of Wonders III|8BHRP-N523T-PNIFQ			
    A Good Snowman Is Hard To Build|A9A2E-PA2FR-8LAC6			
    Alien Spidy|982JQ-803I1-IL0MG			
    All You Can Eat|BDHLG-ANK3A-0AVQV			
    A Mortician's Tale|9P0HQ-VI3AA-8EE2F

