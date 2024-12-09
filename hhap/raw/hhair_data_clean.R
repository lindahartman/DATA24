#https://www.who.int/data/gho/data/themes/air-pollution

library(tidyverse)

# Household air pollution attributable deaths (individuals)
death_df <- read_csv("hhap/raw/deaths_data.csv") |> 
  select(
    region=ParentLocation,
    country_code=SpatialDimValueCode,
    country=Location,
    year=Period,
    cause_of_death=Dim2,
    deaths=FactValueNumeric
  )|>
  arrange(year)

write_csv(death_df, "hhap/raw/hhap_deaths.csv")

#Population with primary reliance on clean fuels and technologies for cooking (in millions)
pop_clean_fuels_df <- read_csv("hhap/raw/pop_data.csv")|> 
  select(
    region=ParentLocation,
    country_code=SpatialDimValueCode,
    country=Location,
    year=Period,
    pop_clean_fuels_cooking_mln=FactValueNumeric
  )
nrow(pop_clean_fuels_df)

prop_clean_fuels_df <- read_csv("hhap/raw/prop_data.csv")|>
    select(
      region=ParentLocation,
      country_code=SpatialDimValueCode,
      country=Location,
      year=Period,
      prop_clean_fuels_cooking_pct=FactValueNumeric
    )
nrow(prop_clean_fuels_df)

clean_fuels_df <- pop_clean_fuels_df|>
  left_join(prop_clean_fuels_df,
    by = join_by(region, country_code, country, year))

write_csv(clean_fuels_df, "hhap/raw/clean_fuels_cooking.csv")

#Population with primary reliance on fuels and technologies for cooking, by fuel type (in millions)

pop_cooking_by_fuel_type_df <- read_csv("hhap/raw/pop_cooking_by_fuel_type_data.csv")|> 
      select(
        region=ParentLocation,
        country_code=SpatialDimValueCode,
        country=Location,
        year=Period,
        fuel_type=Dim2,
        pop_cooking_mln=FactValueNumeric
      )
nrow(pop_cooking_by_fuel_type_df)

prop_cooking_by_fuel_type_df <- read_csv("hhap/raw/prop_cooking_by_fuel_type_data.csv")|>
        select(
          region=ParentLocation,
          country_code=SpatialDimValueCode,
          country=Location,
          year=Period,
          fuel_type=Dim2,
          prop_cooking_pct=FactValueNumeric
        )
nrow(prop_cooking_by_fuel_type_df)

cooking_by_fuel_type_df <- pop_cooking_by_fuel_type_df |>
  left_join(prop_cooking_by_fuel_type_df, 
    by=join_by(region, country_code, country, year, fuel_type))

write_csv(cooking_by_fuel_type_df, "hhap/raw/cooking_by_fuel_type.csv")