import csv 
import sqlite3

conn = sqlite3.connect(database="scouting")
cursor = conn.cursor()

with open("/Users/ACCKo/QRScout/database_migrations/reefscape_data.csv") as reefscape_scouting_data:
    reader = csv.reader(reefscape_scouting_data)
    cols = reader.__next__()

    for row in reader:
        row.pop()
        cursor.execute(
            """
            INSERT INTO stand_scouting 
            (
            initals,
            match_number,
            teamnum,
            start_position,
            no_show,
            cage_position,
            automobile,
            auto_l1,
            auto_l2,
            auto_l3,
            auto_l4,
            auto_algae_barge,
            auto_algae_processor,
            auto_algae_dislodged,
            auto_foul,
            tele_algae_dislodged,
            coral_intake,
            algae_intake,
            tele_l1,
            tele_l2,
            tele_l3,
            tele_l4,
            tele_algae_barge,
            tele_algae_processor,
            end_position,
            touched_opps_cage,
            coral_RP,
            barge_RP,
            auto_RP,
            offense,
            defense,
            was_defended,
            died,
            tipped,
            card,
            comments
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, row 
        )

        conn.commit()

