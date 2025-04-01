import polars as pl

EU = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]
EEA = ["Iceland", "Norway", "Liechtenstein"]
EFTA = ["Switzerland", "Iceland", "Norway", "Liechtenstein"]
NC = ["Norway", "Iceland", "Sweden", "Denmark", "Finland"]

country_codes = pl.read_csv("cia/0_Country_Data_Codes.csv", null_values="NA")

#country_codes.filter(pl.col("Name").is_in(EU))
#country_codes.filter(pl.col("Name").is_in(EEA))
#country_codes.filter(pl.col("Name").is_in(EFTA))
#country_codes.filter(pl.col("Name").is_in(NC))
#country_codes.filter(pl.col("Name").str.contains("Li"))

    
fact_area_df = pl.read_csv("cia/factbook_area_2024.csv", null_values="NA")
fact_comm_df = pl.read_csv("cia/factbook_comm_transport_2024.csv", null_values="NA")
fact_econ_df = pl.read_csv("cia/factbook_economy_security_2024.csv", null_values="NA")
fact_energy_df = pl.read_csv("cia/factbook_energy_environment_2024.csv", null_values="NA")
fact_ppl_df = pl.read_csv("cia/factbook_people_society_2024.csv", null_values="NA")


nordic_council = (fact_ppl_df
    .filter(pl.col("name").is_in(NC))
    .select("name", "slug", "region", "population_total")
    .join(fact_area_df, on=["name", "slug", "region"], how="left")
    .with_columns(population_total=pl.col("population_total")/1e6)
    .rename({"population_total": "population_mln",
            "name":"country_name"})
    .drop("slug", "region")
    )

nordic_council.write_csv("cia/nordic_council.csv")

import polars as pl

import polars as pl

nordic_council = pl.DataFrame({
    "country_name": ["Denmark", "Finland", "Iceland", "Sweden", "Norway"],
    "population_mln": [5.973136, 5.626414, 0.364036, 10.589835, 5.509733],
    "area_sqkm": [43094, 338145, 103000, 450295, 323802]
})


efta_countries = pl.DataFrame({
    "country_name": ["Norway", "Switzerland", "Iceland", "Liechtenstein"],
    "exports_bln": [228.625, 661.628, 13.49, 3.217],
    "imports_bln": [157.032, 554.358, 13.484, 2.23],
    "gdp_bln": [499.528, 733.779, 26.155, 4.978]
})


efta_countries = (fact_econ_df
    .filter(pl.col("name").is_in(EFTA))
    .select("name", "slug", "region", "exports", "imports", "real_gdp_purchasing_power_parity")
    .rename({"real_gdp_purchasing_power_parity": "gdp",
            "name":"country_name"})
    .with_columns((cs.numeric()/1e9).name.suffix("_bln"))
    .select("country_name", "exports_bln", "imports_bln", "gdp_bln")
    )

efta_countries.write_csv("cia/efta_countries.csv")

