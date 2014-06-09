/*Find unique dataid values from table*/
/*SELECT distinct dataid from "PecanStreet_RawData".egauge_minutes_2014 order by dataid asc;*/
/*SELECT distinct dataid from "PecanStreet_RawData".participant_survey_2013 order by dataid asc;*/
/*SELECT count(distinct dataid) from "PecanStreet_RawData".participant_survey_2013;*/

/*Select Unique dataids between egauge2013 and patientsurvey2013*/

/*SELECT count(distinct "PecanStreet_RawData".egauge_minutes_2013.dataid)
FROM "PecanStreet_RawData".egauge_minutes_2013
INNER JOIN "PecanStreet_RawData".participant_survey_2013
ON "PecanStreet_RawData".egauge_minutes_2013.dataid="PecanStreet_RawData".participant_survey_2013.dataid; 

output(houses with minutes and survey data): count=152*/

/*
SELECT count(distinct "PecanStreet_RawData".egauge_minutes_2013.dataid)
FROM "PecanStreet_RawData".egauge_minutes_2013
INNER JOIN "PecanStreet_RawData".audits_2011
ON "PecanStreet_RawData".egauge_minutes_2013.dataid="PecanStreet_RawData".audits_2011.dataid; 

output(houses with minutes and audit data): count=111*/


SELECT distinct "PecanStreet_RawData".egauge_minutes_2013.dataid
FROM "PecanStreet_RawData".egauge_minutes_2013
INNER JOIN "PecanStreet_RawData".participant_survey_2013
ON "PecanStreet_RawData".egauge_minutes_2013.dataid="PecanStreet_RawData".participant_survey_2013.dataid
INNER JOIN "PecanStreet_RawData".audits_2011
ON "PecanStreet_RawData".egauge_minutes_2013.dataid="PecanStreet_RawData".audits_2011.dataid;

/*output(houses with minutes, audit, and survey data): count=42*/

/*
SELECT count(distinct "PecanStreet_CuratedSets".group2_disaggregated_2013_02.dataid)
FROM "PecanStreet_CuratedSets".group2_disaggregated_2013_02
INNER JOIN "PecanStreet_CuratedSets".group3_disaggregated_2013_05
ON "PecanStreet_CuratedSets".group2_disaggregated_2013_02.dataid="PecanStreet_CuratedSets".group3_disaggregated_2013_05.dataid

output(curated sets):group1, group2, group3 are distinct groups*/
/*
SELECT distinct "PecanStreet_CuratedSets".group1_disaggregated_2013_12.dataid
FROM "PecanStreet_CuratedSets".group1_disaggregated_2013_12 order by dataid;*/

