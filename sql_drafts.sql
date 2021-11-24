CREATE OR REPLACE VIEW public.vw_target_details AS
	SELECT targets.target_name,
		positions.position_name,
		positions.position_notes,
		status_log.status_date,
		statuses.status
	FROM targets
	LEFT JOIN positions ON targets.target_id = positions.target_id
	LEFT JOIN status_log ON positions.position_id = status_log.position_id
	LEFT JOIN statuses ON status_log.status_id = statuses.status_id;

CREATE OR REPLACE VIEW public.vw_target_latest_status AS
	SELECT targets.target_id as target, targets.target_name as name, MAX(status_log.status_date) as last_date
	FROM targets
	LEFT JOIN positions ON targets.target_id = positions.target_id
	LEFT JOIN status_log ON positions.position_id = status_log.position_id
	GROUP BY target, name
	ORDER BY last_date ASC;

CREATE OR REPLACE VIEW public.vw_position_info AS
	SELECT p.target_id, p.position_id, p.position_name, p.position_link, p.position_tier, t.tier_name, p.position_notes
	FROM positions p, tiers t
	WHERE p.position_tier = t.tier_id
	ORDER BY p.position_id;

CREATE OR REPLACE VIEW public.vw_position_status_log AS
	SELECT status_log.position_id, status_log.status_date, status_log.status_note, status_log.status_id, statuses.status
	FROM status_log, statuses
	WHERE status_log.status_id = statuses.status_id
	ORDER BY status_date ASC;

-- list all job boards and recruiters, the related link, and date of last status update
CREATE OR REPLACE VIEW public.vw_jobboards_and_recruiters AS
	SELECT positions.target_id AS target_id, target_name, positions.position_id AS position_id, position_name, position_link, status, last_update
	FROM positions, targets, statuses,
		(
		SELECT DISTINCT ON (position_id)
		position_id, status_id, status_date as last_update
		FROM status_log
		ORDER BY position_id, status_date DESC
		) AS tmp_position_last_status
	WHERE position_tier = 0
	AND lower(status) not like '%dead%'
	AND positions.target_id = targets.target_id
	AND positions.position_id = tmp_position_last_status.position_id
	AND tmp_position_last_status.status_id = statuses.status_id
	ORDER BY target_id, position_id;


-- list of targets, positions, and current status, in alphabetical order
SELECT targets.target_id, targets.target_name, positions.position_id, positions.position_name, positions.position_notes, status_log.status_id
FROM targets
LEFT JOIN positions on targets.target_id = positions.target_id
LEFT JOIN status_log on positions.position_id = status_log.position_id
WHERE positions.position_id IN (
	SELECT position_id
	FROM status_log
	WHERE status_id = 12
)
ORDER BY target_name, position_name, status_id;

-- list of targets, positions, and current status, in activity chrono order, for recruiters and job-boards
{
	SELECT targets.target_id, targets.target_name, positions.position_id, positions.position_name, positions.position_notes, status_log.status_date, status_log.status_id, statuses.status
	FROM targets
	LEFT JOIN positions on targets.target_id = positions.target_id
	LEFT JOIN status_log on positions.position_id = status_log.position_id
	LEFT JOIN statuses on status_log.status_id = statuses.status_id
	WHERE positions.position_tier = 0
	ORDER BY target_id, position_id, status_date;
}

SELECT * 
FROM (
	SELECT DISTINCT ON (position_id)
	position_id , status_log.status_id as status_id, status, status_date as last_update
	FROM status_log, statuses
	WHERE status_log.status_id = statuses.status_id
	ORDER BY position_id, status_date DESC
) AS tmp_position_last_status
LIMIT 10;




-- add a new column to the status log table
ALTER TABLE status_log
ADD COLUMN status_note TEXT;





-- insert new Target company
-- INSERT INTO targets (target_name, target_link, target_description, target_location) VALUES ('aaa','bbb','ccc', 'p,o');
-- INSERT INTO targets (target_name, target_link, target_description, target_location)", ({targetName}, {targetLink}, {targetDesc}, {targetLoc}






-- change datatype of tier name from varchar to text
-- first we need to delete the view that depends on the field, change the data type, and then re-create the field

-- DROP VIEW public.vw_position_info;

-- ALTER TABLE tiers
-- 	ALTER tier_name TYPE text,
-- 	ALTER tier_name SET NOT NULL;

-- CREATE OR REPLACE VIEW public.vw_position_info AS
--  SELECT p.target_id,
--     p.position_id,
--     p.position_name,
--     p.position_link,
--     p.position_tier,
--     t.tier_name,
--     p.position_notes
--    FROM positions p,
--     tiers t
--   WHERE p.position_tier = t.tier_id
--   ORDER BY p.position_id;