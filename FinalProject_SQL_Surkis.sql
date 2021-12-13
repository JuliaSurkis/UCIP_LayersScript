create table final_county (
countyName varchar(30) not null,
countyArea float,
constraint finalCountyPK primary key (countyName)
);

create table final_municipality(
muniName varchar(25) not null,
muniArea float,
muniCounty varchar (25),
constraint finalMuniPK primary key(muniName),
constraint finalMuniFK foreign key (muniCounty)
references final_county(countyname));

create table final_assessor (
assessorName varchar(30) not null,
contactNum varchar(12),
contactEmail varchar(60),
contactTitle varchar(30),
constraint finalAssessorPK primary key(assessorName)
);

create table muniAssessor(
assessorNameMuni varchar(30) not null,
jurisdiction varchar(30) not null,
view_edit char(4) not null,
assessorCounty varchar(30),
assessMuniArea float,
constraint finalNameMuniPK primary key(assessorNameMuni,jurisdiction),
constraint finalAssessMuniCountyFK foreign key(assessorCounty)
references final_county(countyname),
constraint finalassessNameFK foreign key(assessorNameMuni)
references final_assessor(assessorName)
);

create table final_asset (
assetID int not null,
asset_assessor varchar(30),
asset_name varchar(60),
asset_type varchar(20),
asset_location float,
asset_jurisdiction varchar(30),
constraint assetPK primary key(assetID),
constraint assessorFK foreign key(asset_assessor)
references final_assessor(assessorname),
constraint assetjurisFK foreign key(asset_jurisdiction)
references final_municipality(muniname)
	);

alter table final_assessor add column firstname varchar(15);
alter table final_assessor add column lastname varchar(20);
alter table final_municipality add column geom geometry;
alter table final_municipality drop column geom;
alter table final_municipality add column geom geometry(MultiPolygon,4326);

create table final_munis(
name varchar not null,
geom geometry(Multipolygon),
id integer
constraint munisPK primary key);

insert into final_munis
select "NAME",geom,id
from "JustCounties";

alter table final_asset add column point_geom geometry(point);

insert into final_asset(asset_jurisdiction)
select m.muniname
from final_munis m
left join final_asset
on st_contains(m.geom, final_asset.point_geom);



	
-- Not Used!!!
create table final_asset_editor(
asset_editID int not null,
asset_editor varchar(30),
edit_jurisdiction varchar(30),
constraint assetEditorPK primary key(asset_editID, asset_editor),
constraint assetEditFK foreign key(asset_editID)
references final_asset(assetID),
constraint assessorEditFK foreign key(asset_editor)
references muniassessor(assessornamemuni,jurisdi),
constraint editJurisFK foreign key(edit_jurisdiction)
references muniassessor(jurisdiction)
);


INSERT INTO final_municipality ( muniname, geom ) 
VALUES ( '{"name":"Argentina"}', 
  (ST_DUMP(
    ST_SetSRID( 
        ST_GeomFromGeoJSON('{...}'),
    4326)
  )).geom  
);

WITH data AS (SELECT '{ "type": "FeatureCollection",
    "features": [
	{ "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         },
         "properties": {
           "prop0": "value0",
           "prop1": {"this": "that"}
           }
         }
       ]
     }'::json AS fc)

SELECT
  row_number() OVER () AS gid,
  ST_AsText(ST_GeomFromGeoJSON(feat->>'geometry')) AS geom,
  feat->'properties' AS properties
FROM (
  SELECT json_array_elements(fc->'features') AS feat
  FROM data
) AS f;