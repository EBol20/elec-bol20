- downloaded from here  
[here](https://drive.google.com/file/d/1rMMl-lcRZptbhUGbe2g6ZdDREbNPh3Nd/view)
2020-10-17_13-58-02_

I matched the OEP's Padrón (See: https://www.oep.org.bo/elecciones-generales-2020/) against GeoElectoral's maps (See #1: https://geoelectoral.oep.org.bo/tse/home) (See #2: https://geoelectoral.oep.org.bo/oep/rest/services). GeoElectoral's Bolivia map matched well, except for a few precincts not included in the padrón, but the Exterior maps are a problem. There are a number of precincts which don't match the padrón, and they keep posting updates of these maps as polling places change. (Thus the '8ok' suffix.) A few points to be mindful of:

* The tables like 'reci_interior' or 'reci_exterior' are the OEP Padrón matched against GeoElectoral's maps and so include both voter data and geographic coordinates. Any entries in the GeoElectoral maps that don't match the OEP Padrón are not included in those tables. If there were any precincts included in the OEP Padrón but not in the GeoElectoral map, I tried to find the coordinates via GoogleMaps. The other tables labeled with the suffix 'geo' represent the GeoElectoral data and so don't have OEP padrón data like the number of voters, etc.

* There are differences between these two data sets. Most place names will match exactly, but not all. There are issues with inconsistent use of accents and the OEP Padrón data has some entries with a bunch of whitespace for some reason. I've retained it because it accurately reflects what was in the OEP's padrón data.

* There are some places where there are two precincts in a single location, sometimes even with the same named geographic identifiers. (This seems to be especially true in LP/El Alto.) In these cases, I had to guess at which FID value to assign to which entry in the OEP Padrón data.

* In some places overseas citizens will not be able to vote, for public health reasons. As of right now (10/16/2019), I think it's: Panamá, all of Chile except for Santiago, and Mendoza in Argentina. This might change.

* 'tipo_de_area' comes from matching coordinates against 'Categoria de accesibilidad de comunidades a centros poblados, 2013' (See: https://geo.gob.bo/geonetwork/srv/spa/catalog.search#/metadata/ba74ed29-8015-4b62-bd9c-3f6c9dbaab55). Results are mostly OK, but not always, and some areas are unmapped. Usually these are isolated rural areas, but not always! You could resolve these by finding closest polygon, rather than enclosing one.

* The 'denspop' field comes from matching coordinates against 'Densidad de población por comunidad en km2, 2001'. (See: https://geo.gob.bo/geonetwork/srv/spa/catalog.search#/metadata/83408d25-6384-4668-8359-fbd01a7728ba) I looked for a similar national population density map based on 2012, but didn't find one.




EXTRA INFO: 

I just wanted to clarify, since I'm not sure I explained it well: Those tables ('reci_interior', 'reci_exterior') were just the padrón data the OEP released on the 8th, then I found coordinates for all of them, in nearly all cases from GeoElectoral. The ones like 'reci_interior_geo' and 'reci_exterior_geo' are GeoElectoral's maps but not combined with any padrón data. The GeoElectoral maps are probably more reliable for where the polling places will be, but there isn't padrón data for all of them. In those '*_geo' tables, there's a column at the end like 'in_padron' which tells you if that entry was in the padrón data or not. And you can match entries from both types of tables against each other based on 'RECI_GEO_FID'.