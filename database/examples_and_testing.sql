/*
 These are examples of various types of queries that can be performed
 Ty Garber 4/28/2023
 */

-- example of a normal query, showing children
-- levels are dependent on the number of aliased tables
-- and joins. one join = one level down
select cal.catch_area_description parent_catch_area,
       cal2.catch_area_description children_catch_areas
from catch_area_lut cal
join catch_area_lut cal2 on cal.catch_area_id = cal2.parent_catch_area_id;

-- recursive query
with recursive catch_areas as (
select cal.catch_area_description as parent_catch_area,
       null as children_catch_areas
from catch_area_lut cal
where parent_catch_area_id is null
union all
select cal.catch_area_description
    parent_catch_area,
    cal2.catch_area_description children_catch_areas
                               from catch_area_lut cal
                                        join catch_area_lut cal2 on cal.catch_area_id = cal2.parent_catch_area_id
) select * from catch_areas

