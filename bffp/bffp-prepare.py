
from tidytuesday import TidyTuesday
import polars as pl
import polars.selectors as cs

# plastic pollution
tt = TidyTuesday('2021-01-26', mod=pl, kwargs={"null_values": ["NA", "null"]})
#tt.data
plastics_df = tt.data['plastics']
# %view dt
(plastics_df.describe())


# identify countries that do not match
tmp1_df=(plastics_df.select(pl.col("country").str.to_titlecase()).unique()
    .join(country_regions,
    on="country", how="anti")
)
tmp1_df

plastics_df.filter(pl.col("country").str.contains("aiwan"))

country_regions_plus = (country_regions
    .vstack(pl.DataFrame({
        "region": ["Eastern Mediterranean", "Europe", "Western Pacific", "Western Pacific"],
        "country_code": ["TUR", "BGR", "HKG", "TWN"],
        "country": ["Turkey", "Bulgaria", "Hong Kong", "Taiwan (Province of China)"]
    }))
)

(plastics_df
    .with_columns(pl.col("country").str.to_titlecase())
    .with_columns(pl.col("country").replace({
        "Vietnam": "Viet Nam",
        "United States Of America": "United States of America",
        "Taiwan_ Republic Of China (Roc)": "Taiwan (Province of China)",
        "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
        "United Kingdom Of Great Britain & Northern Ireland": "United Kingdom of Great Britain and Northern Ireland",
        "Cote D_Ivoire": "Cote d'Ivoire",
        "Netherlands": "Netherlands (Kingdom of the)",
        "Tanzania": "United Republic of Tanzania",
        "Empty": None,
        "Korea": "Republic of Korea"
    }))
    .join(country_regions_plus, on="country", how="left") 
    .select("region", "country_code", cs.all().exclude("region", "country_code"))
    ).write_csv("bffp/BFFplastics.csv")
