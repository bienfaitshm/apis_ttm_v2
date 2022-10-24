
orgine_sql = """
WITH RECURSIVE template as (
	SELECT 
		id, 
		whereFrom_id,
		node_id
	FROM dash_routing WHERE id=?
	UNION ALL
	SELECT 
		dr.id, 
		dr.whereFrom_id,
		dr.node_id
	FROM dash_routing dr , template tmp
	WHERE dr.id = tmp.whereFrom_id
),  origine as (
		SELECT dash_covercity.town FROM template 
		INNER JOIN dash_covercity ON template.node_id = dash_covercity.id
		WHERE template.whereFrom_id IS NULL
)

SELECT town FROM origine
"""
