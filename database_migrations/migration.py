import csv 
import psycopg

conn = psycopg.connect("dbname=scouting user=postgres host=localhost password=postgres port=5432")
cursor = conn.cursor()

with open('./scouting_data.csv') as scouting_data:
    reader = csv.reader(scouting_data)
    cols = reader.__next__()

    for row in reader:
        row.pop(7)
        cursor.execute(
            """INSERT INTO stand_scouting (automobile, card, comments, coop, defended, dies, end_position, initals, no_show, spotlight, start_position, tipped, auto_amp, auto_amp_miss, auto_note_score, auto_pieces, auto_speaker, auto_speaker_miss, defense, foul, harmony, match_number, offense, teamnum, tele_amp, tele_amp_miss, tele_note_score, tele_pieces, tele_speaker, tele_speaker_miss, trap
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )""", row 
        )

        conn.commit()

