WITH RECURSIVE template as (
	SELECT 
		id, 
		whereFrom_id 
	FROM dash_routing WHERE id=9
	UNION ALL
	SELECT 
		dr.id, 
		dr.whereFrom_id 
	FROM dash_routing dr , template tmp
	WHERE dr.id = tmp.whereFrom_id
),  origine as (
		SELECT id FROM template WHERE template.whereFrom_id IS NULL
), routes as (
	SELECT 
		dr.id, 
		0 as level, dr.whereFrom_id, 
		dr.whereTo_id, 
		dr.node_id, 
		dc.town,
		dc.code,
		dc.latitude,
		dc.longitude,
		dc.image,
		dc.company_id
	FROM dash_routing dr , origine 
		INNER JOIN dash_covercity dc ON (dc.id = dr.node_id)
	WHERE  origine.id = dr.id 
	UNION ALL
	SELECT 
		dr.id, 
		routes.level+1, 
		dr.whereFrom_id, 
		dr.whereTo_id, 
		dr.node_id, 
		dc.town,
		dc.code,
		dc.latitude,
		dc.longitude,
		dc.image,
		dc.company_id
	FROM dash_routing dr , routes 
		INNER JOIN dash_covercity dc ON (dc.id = dr.node_id)		
	WHERE  routes.id = dr.whereFrom_id
	
)

SELECT * FROM routes
