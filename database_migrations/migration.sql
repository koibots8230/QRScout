CREATE DATABASE scouting;

CREATE TYPE CARD AS ENUM ('None', 'Yellow', 'Red');
CREATE TYPE END_POSITION AS ENUM ('None', 'Wing', 'Climb');
CREATE TYPE START_POSITION AS ENUM ('Blue 1', 'Blue 2', 'Blue 3', 'Red 1', 'Red 2', 'Red 3');

CREATE TABLE IF NOT EXISTS stand_scouting (
  id SERIAL PRIMARY KEY,
  automobile BOOLEAN,
  card CARD,
  comments VARCHAR(255),
  coop BOOLEAN,
  defended BOOLEAN,
  dies BOOLEAN,
  initals VARCHAR(5),
  no_show BOOLEAN,
  spotlight SMALLINT,
  start_position START_POSITION,
  tipped BOOLEAN,
  auto_amp SMALLINT,
  auto_amp_miss SMALLINT,
  auto_note_score SMALLINT,
  auto_pieces SMALLINT,
  auto_speaker SMALLINT,
  defense SMALLINT,
  foul SMALLINT,
  harmony SMALLINT,
  match_number SMALLINT,
  offense SMALLINT,
  teamnum INT,
  tele_amp SMALLINT,
  tele_amp_miss SMALLINT,
  tele_note_score SMALLINT,
  tele_pieces SMALLINT,
  tele_speaker SMALLINT,
  tele_speaker_miss SMALLINT,
  trap SMALLINT
);

CREATE TYPE PIT_STARTING_POSITION AS ENUM ('Left', 'Center', 'Right');
CREATE TYPE MEASURE_WITH_OR_WITHOUT_BUMPERS AS ENUM ('With Bumpers', 'Without Bumpers');
CREATE TYPE CAN_SHOOT_AMP_OR_SPEAKER AS ENUM ('Amp', 'Speaker', 'Both');
CREATE TYPE PREFERS_AMP_OR_SPEAKER AS ENUM ('Amp', 'Speaker', 'Both');
CREATE TYPE PREFERRED_PICKUP_LOCATION AS ENUM ('Ground', 'Source', 'None');
CREATE TYPE DRIVETRAIN_TYPE AS ENUM ('Swerve', 'Tank', 'Mechanum');
CREATE TYPE WHERE_CAN_ROBOT_CLIMB_A_CHAIN AS ENUM ('Side', 'Middle');


CREATE TABLE IF NOT EXISTS pit_scouting (
  id SERIAL PRIMARY KEY,
  other_info VARCHAR(255),
  initals VARCHAR(5),
  starting_position PIT_STARTING_POSITION,
  teamnum INT,
  dimensions VARCHAR(50),
  measured_with_or_without_bumpers MEASURE_WITH_OR_WITHOUT_BUMPERS,
  can_shoot_amp_or_speaker CAN_SHOOT_AMP_OR_SPEAKER,
  prefers_amp_or_speaker PREFERS_AMP_OR_SPEAKER,
  preferred_pickup_location PREFERRED_PICKUP_LOCATION,
  shooting_distance SMALLINT,
  autos SMALLINT,
  defense_experience SMALLINT,
  drivetrain_type DRIVETRAIN_TYPE,
  estimated_speed SMALLINT,
  where_can_robot_climb_a_chain WHERE_CAN_ROBOT_CLIMB_A_CHAIN,
  robot_climbed_differently VARCHAR(255),
  drive_motors SMALLINT,
  gear_ratios VARCHAR(255)
);
