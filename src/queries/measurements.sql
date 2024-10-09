SELECT 
    tn.bwf_node_id,
    tn.bwf_object_id,
    co.bwf_name         AS system_name, 
    mo.bwf_name         AS measurement_name,
    so.bwf_name         AS archive_name,
    mo.bwf_meas_date    AS measurement_date,
    pt.bwf_depth        AS depth,
    pt.bwf_pos_id       AS position_id,
    pt.bwf_min_land     AS min_land, 
    pt.bwf_limit_land   AS max_land, 
    pt.bwf_min_groove   AS min_groove, 
    pt.bwf_limit_groove AS max_groove, 
    rd.bwf_file_name    AS data_file
FROM (((((bwf_tree_node AS tn
    INNER JOIN bwf_b280_config_object AS co ON tn.bwf_object_id   = co.bwf_object_id)
    INNER JOIN bwf_b280_meas_object   AS mo ON tn.bwf_object_id   = mo.bwf_object_id)
    INNER JOIN bwf_b280_spec_object   AS so ON mo.bwf_spec_id     = so.bwf_object_id)
    INNER JOIN bwf_b280_rough_data    AS rd ON mo.bwf_row_data_id = rd.bwf_object_id)
    INNER JOIN bwf_position_table     AS pt ON mo.bwf_object_id   = pt.bwf_object_id)
WHERE tn.bwf_presentation_id = 'b280_measurement_pres'


