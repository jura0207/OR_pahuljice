# OR_pahuljice

This dataset represent various cereals and information about them

## Dataset description
Title - Pahuljice (eng. cereals)  
Keywords - Cereal, food  
License - CC0-1.0  
Author - Jura Vuković <jura.vukovic@fer.hr>  
Version - 1.0  
Language - English  

## CSV Distribution
Title - naziv_skupa.csv  
Description - CSV distribution of the popular cereals  
Media type - text/csv  
Licence - CC0-1.0  
Publication date - 2022-11-02  
Last modification - 2022-11-02  

## JSON Distribution
Title - naziv_skupa.json  
Description - JSON distribution of the popular cereals  
Media type - application/json  
Licence - CC0-1.0  
Publication date - 2022-11-02  
Last modification - 2022-11-02  

## Structural metadata
|Field | Datatype | Description | Primary key|
|---|---|---|---|
|id_manufacturer | integer | Unique manufacturer ID of the cereal|True|
|id_store | integer | Unique store ID that sells the cereal|True|
|id_cereal | integer | Unique cereal ID|True|
|cereal_name | string | Name of the cereal||
|type | string | Type of the cereal||
|number_of_calories | integer | Number of the calories /100g of the cereal||
|price | numeric | Price of the cereals /1kg||
|ingredients | integer[] | An array of the ingredients keys that are in the cereals||
|store_name | string | Name of the store that sells the cereals||
|store_country_iso | string | ISO of the country where the cereal is sold||
|manufacturer_name | string | Name of the manufacturer that creates the cereal||
|manufacturer_country_iso | string | ISO of the country where the cereal is manufactured||
|id_ingredients | integer | Unique ingredient ID that the cereals contain|True|
|ingredient_name | string | Name of the ingredient that the cereals contain||
|is_vegan | boolean | Is the ingridient vegan?||
|is_gluten_free | boolean | Is the ingridient gluten free?||
|is_allergens_free | boolean | Is the ingridient allergen free?||
