-- Keeping some useful DB requests
SELECT operator.name AS operator_name, bool_or(position.has_2g) AS bool_or_1, bool_or(position.has_3g) AS bool_or_2, bool_or(position.has_4g) AS bool_or_3
FROM operator, position
WHERE operator.mcc_mnc = position.operator_code
AND ST_DWithin(CAST(position.location AS geography(GEOMETRY,4326)), ST_GeomFromText('POINT(1.08771 49.433075)'), 1000)
GROUP BY operator.name;


SELECT operator.name, position.location, position.has_2g, position.has_3g, position.has_4g
FROM operator, position
WHERE operator.mcc_mnc = position.operator_code
AND ST_DWithin(CAST(position.location AS geography(GEOMETRY,4326)), ST_GeomFromText('POINT(-1.49487 43.4746985)'), 1000);

SELECT operator.name AS operator_name, bool_or(position.has_2g) AS bool_or_1, bool_or(position.has_3g) AS bool_or_2, bool_or(position.has_4g) AS bool_or_3
FROM operator, position
WHERE operator.mcc_mnc = position.operator_code
AND ST_DWithin(CAST(position.location AS geography(GEOMETRY,4326)), ST_GeomFromText('POINT(2.380383 48.860248)'), 1000) GROUP BY operator.name;

SELECT * from position;