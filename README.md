# README 
---
A repo for our scouting application(s).
 > note: this is code edited/adapted from FRC team #2713's original QRScout
 ---
 <h1>IF THIS BLOWS UP, IT'S NOT MY FAULT.</h1>



HOW TO USE:



<h1> Head Scouter: </h1>

1. open 'DB Browser (SQLCipher)'
2. open the 'scouting' database under this pc >> users >> AccKo >> QRScout
note: the database is 'scouting', not 'scouting.db'. don't ask why, it just is 'cause I said so.
3. open the 'scouting_data' table under the 'browse data' tab
4. open visual studio code (on our laptop, open the explorer and type in wpilib and the wpilib vscode will pop up)
5. navigate (in)to the 'QRScout' folder
6. press ctrl+shift+p to open the command palette
7. type in view: toggle terminal to open the terminal at the bottom of the screen
8. in the terminal, type:
    - .venv\Scripts\activate
    - python .\src\scouting.py
9. wait for the 'tk' window to pop up. it may take ~15 seconds. you might have to search through windows to find it
10. press 'space' to scan a QR code, and q to quit the program and close the window
11. after scanning QR codes, go back to the DB Browser and hit the refresh button (located near the 'edit pragmas' tab) (or ctrl+r)

<h2>Moving data to Tableau</h2>

1. login to Tableau (I will give you the login. do not share it. duh)
2. in DB Browser, go to file >> export >> table(s) as JSON
3. export the 'stand_scouting' table
4. in Tableau, click connect to a JSON file
5. click 'stand_scouting.json' under QRScout
6. profit