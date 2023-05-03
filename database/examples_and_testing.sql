/*
 These are examples of various types of queries that can be performed
 Ty Garber 4/28/2023
 */


-- parent and child example common table expressions
-- parent
with parent as(
    insert into catch_area_lut(catch_area_code, catch_area_description,
                               created_by, created_datetime)
    values
        ('804', 'Puyallup River', 'garber', now())
    returning catch_area_id, created_datetime, created_by
) --children
insert into catch_area_lut(parent_catch_area_id, catch_area_code, catch_area_description,
                           created_by, created_datetime)
select
    catch_area_id::uuid as parent_catch_area_id,
    '804' as catch_area_code,
    E'From the 11th St. Bridge to 400\' downstream of Clark\'s Creek' as catch_area_description,
    created_by,
    created_datetime
from parent
union all
select
    catch_area_id::uuid as parent_catch_area_id,
    '804' as catch_area_code,
    E'From 400\' downstream of Clark\'s Creek to 400\' upstream of Clark\'s Creek' as catch_area_description,
    created_by,
    created_datetime
from parent
union all
select
    catch_area_id::uuid as parent_catch_area_id,
    '804' as catch_area_code,
    E'From 400\' upstream of Clark\'s Creek to East Main Bridge' as catch_area_description,
    created_by,
    created_datetime
from parent
union all
select
    catch_area_id::uuid as parent_catch_area_id,
    '804' as catch_area_code,
    E'From East Main Bridge to Carbon River' as catch_area_description,
    created_by,
    created_datetime
from parent
union all
select
    catch_area_id::uuid as parent_catch_area_id,
    '804' as catch_area_code,
    E'From Carbon River upstream' as catch_area_description,
    created_by,
    created_datetime
from parent;

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
) select * from catch_areas;

/*
 insert some data
 */

-- Puyallup river has some pretty gnarly regulations / mixed bag and regulation

-- insert some 'fisheries'
-- insert into fishery(fishery_type_id, fishery_management_year_id, catch_area_id, fishery_description,
--                     regulation_authority_id, created_by, created_datetime)
-- values
--     ('ff2076b7-7f01-4938-bb77-73a8f16d8c84', '40b5fe35-e081-482e-a4ee-ac053537a425', '8663998c-7364-4ce2-9c42-2c3dbd647194', 'Lower Pullayup River',
--         '148567df-d135-465c-bd7a-5476960cd520', 'garber', now()),
--     ('ff2076b7-7f01-4938-bb77-73a8f16d8c84', '40b5fe35-e081-482e-a4ee-ac053537a425', '0d1a0915-caba-40d9-8aac-ec927ecb47ff', 'Upstream of Clarks Creek',
--         '148567df-d135-465c-bd7a-5476960cd520', 'garber', now());

-- insert some times/dates associated with those fisheries
with fish as (
    insert into fishery_regulation (fishery_id, fishery_regulation_type_id,
                                    start_datetime, end_datetime,
                                    gear_type_id, created_by, created_datetime)
        values ('691cab30-dc51-4835-98e4-ed4ab19c6244', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-01-01'::timestamp at time zone 'US/Pacific', '2022-12-31 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now())
)


-- load some species groups into the species group table
insert into species_group(species_id,  species_group_type_id)
values
    ('bad26e7e-ec39-478d-92b5-eb13b0032603', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('b4416acc-2dce-4a14-a518-931eb45edbb1', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('18ee22d5-8eed-46cf-9193-a5c767f1c965', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('418ec7c4-1743-405c-86f6-e2307fe4615d', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('a6d2c39b-281e-4817-ab4c-b50f93c89504', 'b455cd3f-f578-4fae-af90-2238bd225d75');

-- parent bag limit (daily)
insert into bag_limit(
                       fishery_regulation_id, regulation_age_id, species_group_type_id,
                       regulation_type_id, bag_limit_type_id, maximum_size_limit_centimeters,
                        bag_limit_angler_resident_status_id,
                      minimum_size_limit_centimeters, bag_limit_total, created_by, created_datetime)
values (
        '3932dc50-b870-46c1-b568-116a893afbe6', '5c29ce48-ff99-41e3-9381-93b2564df906', '47db089c-5756-4fe4-bee2-e6cd76e9b88b',
        '4556aaa7-6f1d-4e73-ae29-cc6780098dcd', 'feea8f55-a695-4171-b3fd-642f2af4081b', NULL,
        '6ecc5341-1325-43b5-8ce2-87c0ae51cb66',
        28 * 2.54, 3, 'garber', now()
       );

-- child bag limit
insert into bag_limit( -- this will need resident status
                       parent_bag_limit_id, fishery_regulation_id, regulation_age_id, species_group_type_id,
                       regulation_type_id, bag_limit_type_id, maximum_size_limit_centimeters,
                      minimum_size_limit_centimeters, bag_limit_total, created_by, created_datetime)
values (
        '0373c9af-025e-42fc-95cc-058c5a80c75e','4341be73-00db-4e94-b7ed-3383a360465c', '850a2137-43ab-4327-8f49-3b50ca8b6dbc', '216ee679-e466-41ca-8cb4-590cc3f7709e',
        'ab43a5b2-34a0-41ee-8063-9250162cad67', 'cb489ec8-c153-4b86-a395-bc1169390f9b', NULL, 12 * 2.54, 2,
        'garber', now()
       );

-- Give a shot Yakutat in Alaska

-- insert some 'fisheries'
insert into fishery(fishery_type_id, fishery_management_year_id, catch_area_id, fishery_description,
                    regulation_authority_id, created_by, created_datetime)
values
    ('ff2076b7-7f01-4938-bb77-73a8f16d8c84', '40b5fe35-e081-482e-a4ee-ac053537a425', 'a4cc93a0-bf8a-4564-b482-3c8b415f1550', 'Yakutat',
        '7a325360-faab-46ba-bfe9-19d7cd6991b6', 'garber', now())

-- insert some times/dates associated with those fisheries
with fish as (
    insert into fishery_regulation (fishery_id, fishery_regulation_type_id,
                                    start_datetime, end_datetime,
                                    gear_type_id, created_by, created_datetime)
        values ('691cab30-dc51-4835-98e4-ed4ab19c6244', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-08-16'::timestamp at time zone 'US/Pacific', '2022-08-20 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
               ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-08-22'::timestamp at time zone 'US/Pacific', '2022-08-27 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
                ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-08-29'::timestamp at time zone 'US/Pacific', '2022-09-03 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
                ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-09-07'::timestamp at time zone 'US/Pacific', '2022-09-10 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
                ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-09-14'::timestamp at time zone 'US/Pacific', '2022-09-17 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
                ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-09-21'::timestamp at time zone 'US/Pacific', '2022-09-24 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now()),
                ('dc820f06-8451-4830-b9c0-6e59574323d7', 'd1aa8518-ffcf-4e70-a7b9-32874f916681',
                '2022-09-28'::timestamp at time zone 'US/Pacific', '2022-09-30 23:59'::timestamp at time zone 'US/Pacific',
                '73ade5d3-180a-4136-b430-f593a2853c91', 'garber', now())
)

update fishery_regulation
    set start_datetime = '2022-01-01'::timestamp at time zone 'America/Anchorage',
        end_datetime = '2022-12-31 23:59'::timestamp at time zone 'America/Anchorage'
where fishery_regulation_id = '3932dc50-b870-46c1-b568-116a893afbe6'


-- select * from fishery_regulation
set timezone = 'UTC'
-- load some species groups into the species group table
insert into species_group(species_id,  species_group_type_id)
values
    ('bad26e7e-ec39-478d-92b5-eb13b0032603', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('b4416acc-2dce-4a14-a518-931eb45edbb1', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('18ee22d5-8eed-46cf-9193-a5c767f1c965', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('418ec7c4-1743-405c-86f6-e2307fe4615d', 'b455cd3f-f578-4fae-af90-2238bd225d75'),
    ('a6d2c39b-281e-4817-ab4c-b50f93c89504', 'b455cd3f-f578-4fae-af90-2238bd225d75');

-- parent bag limit (daily)
insert into bag_limit(
                       fishery_regulation_id, regulation_age_id, species_group_type_id,
                       regulation_type_id, bag_limit_type_id, maximum_size_limit_centimeters,
                      minimum_size_limit_centimeters, bag_limit_total, created_by, created_datetime)
values (
        '4341be73-00db-4e94-b7ed-3383a360465c', '5c29ce48-ff99-41e3-9381-93b2564df906', 'b455cd3f-f578-4fae-af90-2238bd225d75',
        '4556aaa7-6f1d-4e73-ae29-cc6780098dcd', '99116fee-7807-4473-9912-575fa52263e9', NULL, 12 * 2.54, 6,
        'garber', now()
       );

-- child bag limit
insert into bag_limit( -- this will need resident status
                       parent_bag_limit_id, fishery_regulation_id, regulation_age_id, species_group_type_id,
                       regulation_type_id, bag_limit_type_id, maximum_size_limit_centimeters,
                      minimum_size_limit_centimeters, bag_limit_total, created_by, created_datetime)
values (
        '0373c9af-025e-42fc-95cc-058c5a80c75e','4341be73-00db-4e94-b7ed-3383a360465c', '850a2137-43ab-4327-8f49-3b50ca8b6dbc', '216ee679-e466-41ca-8cb4-590cc3f7709e',
        'ab43a5b2-34a0-41ee-8063-9250162cad67', 'cb489ec8-c153-4b86-a395-bc1169390f9b', NULL, 12 * 2.54, 2,
        'garber', now()
       );

-- query to get stuff out
set timezone = 'America/Anchorage'
select
    f.fishery_description,
    fr.start_datetime,
    fr.end_datetime,
    cal.catch_area_description,
    sl.species_group_type_description,
    rtl.regulation_type_code,
    ral.regulation_authority_code,
    ra.regulation_age_description,
    bl.minimum_size_limit_centimeters,
    bl.maximum_size_limit_centimeters,
    bltl.big_limit_type_description,
    blarsl.bag_limit_angler_resident_status_description,
    bl.bag_limit_total
from
    fishery f
join fishery_regulation fr on f.fishery_id = fr.fishery_id
join bag_limit bl on fr.fishery_regulation_id = bl.fishery_regulation_id
join catch_area_lut cal on f.catch_area_id = cal.catch_area_id
join species_group_type_lut sl on bl.species_group_type_id = sl.species_group_type_id
join regulation_authority_lut ral on f.regulation_authority_id = ral.regulation_authority_id
join regulation_type_lut rtl on bl.regulation_type_id = rtl.regulation_type_id
join regulation_age_lut ra on bl.regulation_age_id = ra.regulation_age_id
join bag_limit_type_lut bltl on bl.bag_limit_type_id = bltl.bag_limit_type_id
join bag_limit_angler_resident_status_lut blarsl on bl.bag_limit_angler_resident_status_id = blarsl.bag_limit_angler_resident_status_id
where
    regulation_authority_code= 'ADFG'
