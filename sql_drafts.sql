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

CREATE OR REPLACE VIEW public.vw_position_status_log AS
	SELECT status_log.position_id, statuses.status, status_log.status_note, status_log.status_date
	FROM status_log, statuses
	WHERE status_log.status_id = statuses.status_id
	ORDER BY status_date ASC;

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


-- add a new column to the status log table
ALTER TABLE status_log
ADD COLUMN status_note TEXT;