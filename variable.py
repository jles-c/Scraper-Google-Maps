## 2.1) Keywords & locations

FR_paris = [
    "75000","75001","75002","75003","75004","75005","75006","75007","75008","75009",
    "75010","75011","75012","75013","75014","75015","75016","75017","75018","75019","75020",
    ]
FR_test = [
    "75000"
    ]
ES_test = [
    "Barcelone"
    ]

FR_cities = [
    "Paris","Marseille","Lyon",
    "Toulouse","Nice","Nantes","Montpellier","Strasbourg","Bordeaux","Lille",
    "Rennes","Reims","Toulon","Saint-Étienne","Le Havre","Grenoble","Dijon","Angers","Villeurbanne","Saint-Denis","Nîmes",
    "Clermont-Ferrand","Le Mans","Aix-en-Provence","Brest","Tours","Amiens","Limoges","Annecy","Boulogne-Billancourt",
    "Perpignan","Besançon","Metz","Orléans","Saint-Denis","Rouen","Argenteuil","Montreuil","Mulhouse","Caen","Nancy",
    "Saint-Paul","Roubaix","Tourcoing","Nanterre","Vitry-sur-Seine","Créteil","Avignon","Poitiers","Aubervilliers"
    ]

ES_cities = [
    'Albacete','Alcalá de Guadaíra','Alcalá de Henares','Alcobendas','Alcorcón','Alcoy','Algésiras','Alicante','Almería',
    'Arganda del Rey','Arona','Arrecife','Avilés','Badajoz','Badalona','Barakaldo','Barcelone','Benalmádena','Benidorm','Bilbao','Burgos','Cadix',
    'Carthagène','Castellón de la Plana','Ceuta','Chiclana de la Frontera','Ciudad Real','Collado Villalba','Cordoue','Cornellà de Llobregat',
    'Coslada','Cuenca','Cáceres','Dos Hermanas','El Ejido','El Prat de Llobregat','El Puerto de Santa María','Elche','Estepona','Ferrol',
    'Fuengirola','Fuenlabrada','Gandie','Getafe','Getxo','Gijón','Granollers','Grenade','Guadalajara','Gérone','Huelva','Huesca',
    'Irun','Jaén','Jerez de la Frontera',"L'Hospitalet de Llobregat",'La Corogne','La Línea de la Concepción','Las Palmas de Gran Canaria',
    'Las Rozas de Madrid', 'Leganés','León','Linares','Logrogne','Lorca','Lugo','Lérida','Madrid','Majadahonda','Malaga','Manresa',
    'Marbella','Mataró','Melilla','Mijas', 'Molina de Segura','Mollet del Vallès','Motril','Murcie','Mérida','Móstoles','Orense','Orihuela',
    'Oviedo','Palma de Majorque','Pampelune','Parla','Paterna','Pinto','Ponferrada','Pontevedra','Pozuelo de Alarcón','Rivas-Vaciamadrid',
    'Roquetas de Mar','Rubí','Sabadell','Sagonte','Saint-Jacques-de-Compostelle','Saint-Sébastien','Salamanque','San Bartolomé de Tirajana',
    'San Cristóbal de La Laguna','San Fernando','San Sebastián de los Reyes','San Vicente del Raspeig','Sanlúcar de Barrameda','Sant Boi de Llobregat',
    'Sant Cugat del Vallès','Santa Coloma de Gramenet','Santa Cruz de Tenerife','Santa Lucía de Tirajana','Santander','Saragosse','Siero',
    'Ségovie','Séville','Talavera de la Reina','Tarragone','Telde','Terrassa','Toledo','Torrejón de Ardoz','Torrelavega','Torremolinos',
    'Torrent','Torrevieja','Utrera','Valdemoro','Valence','Valladolid','Vigo','Viladecans','Vilanova i la Geltrú','Vitoria-Gasteiz','Vélez-Málaga','Zamora'
    ]

IT_cities = ['']

UK_cities = [
    "Aberdeen","Armagh","Bangor","Bath","Belfast","Birmingham","Bradford","Brighton and Hove","Bristol","Cambridge","Canterbury",
    "Cardiff","Carlisle","Chelmsford","Chester","Chichester","Coventry","Derby","Dundee","Durham","Edinburgh","Ely","Exeter",
    "Glasgow","Gloucester","Hereford","Inverness","Kingston upon Hull","Lancaster","Leeds","Leicester","Lichfield","Lincoln",
    "Lisburn","Liverpool","London","Londonderry","Manchester","Newcastle upon Tyne","Newport","Newry","Norwich","Nottingham",
    "Oxford","Perth","Peterborough","Plymouth","Portsmouth","Preston","Ripon","Salford","Salisbury","Sheffield","Southampton",
    "St Albans","St Asaph","St Davids","Stirling","Stoke on Trent","Sunderland","Swansea","Truro","Wakefield","Wells","Westminster",
    "Winchester","Wolverhampton","Worcester","York"
    ]

MX_cities = [
    "Mexico City","Tijuana","Ecatepec","León","Puebla","Ciudad Juárez","Guadalajara","Zapopan","Monterrey",
    "Ciudad Nezahualcóyotl","Chihuahua","Mérida","Naucalpan","Cancún","Saltillo","Aguascalientes","Hermosillo","Mexicali",
    "San Luis Potosí","Culiacán","Querétaro","Morelia","Chimalhuacán","Reynosa","Torreón","Tlalnepantla","Acapulco","Tlaquepaque",
    "Guadalupe","Durango","Tuxtla Gutiérrez","Veracruz","Ciudad Apodaca","Ciudad López Mateos","Cuautitlán Izcalli","Matamoros",
    "General Escobedo","Irapuato","Xalapa","Tonalá","Mazatlán","Nuevo Laredo","San Nicolás de los Garza","Ojo de Agua","Xico",
    "Celaya","Tepic","Ixtapaluca","Cuernavaca","Villahermosa"
    ]

custom_cities = [
    'Bandol',
    'Saint-Cyr-sur-mer',
    'Six-Fours-Les-Plages',
    'Toulon',
    'Ollioules',
    'La Seyne sur mer',
]

Input_city_dict = {
    1:FR_cities,
    2:ES_cities,
    3:IT_cities,
    4:UK_cities,
    5:MX_cities,
    6:FR_paris,
    7:FR_test,
    8:ES_test,
    9:custom_cities,
    }

countries_dict = {
    1:"France",
    2:"España",
    3:"Italie",
    4:"United Kingdom",
    5:"Mexico",
    6:"France",
    7:"France",
    8:"España",
    9:"France",
    }