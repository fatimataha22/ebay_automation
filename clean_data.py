import pandas as pd
df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df = df[~df["Title"].isin(["", " ", "NA", "N/A"])]
df = df.dropna(subset=["Title"])

def clean_price(value):
    if pd.isna(value):
        return None
    value = value.replace("US", "").replace("$", "").replace(",", "").strip()
    return value if value else None

df["Discounted Price"] = df["Discounted Price"].apply(clean_price)
df["Original Price"] = df["Original Price"].apply(clean_price)

df["Original Price"] = df["Original Price"].fillna(df["Discounted Price"])

df["Shipping Details"] = df["Shipping Details"].replace(
    to_replace=[None, "N/A", "", " ", "NA"], value="Shipping info unavailable"
)

df["Discounted Price"] = pd.to_numeric(df["Discounted Price"], errors="coerce")
df["Original Price"] = pd.to_numeric(df["Original Price"], errors="coerce")

df["Discount Percentage"] = round((1 - (df["Discounted Price"] / df["Original Price"])) * 100, 2)
df["Discount Percentage"] = df["Discount Percentage"].fillna(0)

df.to_csv("cleaned_ebay_deals.csv", index=False)

