import pandas as pd
import operator
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def check_orders(df, threshold, operator):
  all_orders = len(df["money_diference_percentage"])
  under_authorized = len(df[operator(df["money_diference_percentage"], threshold)])

  order_type_percentage = (under_authorized / all_orders) * 100

  if threshold == 0:
    return order_type_percentage, f"{order_type_percentage}% of the orders are under authoridzed orders"
  else:
    return order_type_percentage, f"{order_type_percentage}% of the orders are correctly authorized w/ incremental authorization"

def check_by_group(df, p_type, percentage, operator):
  if p_type == "country":
    grouped = df[operator(df["money_diference_percentage"], percentage)].groupby("country_code")

  elif p_type == "store":
    grouped = df[operator(df["money_diference_percentage"], percentage)].groupby("store_address")
    
  else:
    return "invalid parameter, should be 'country' or 'store'"

  df = pd.DataFrame(grouped["money_diference_percentage"].count())
  top_10 = df.sort_values("money_diference_percentage", ascending=False).head(10)
  top_10 = top_10.reset_index()
  return top_10
  

def main_exploration():

  orders = pd.read_csv("./data/orders.csv", header=None)

  orders.columns =['order_id', 'activation_time_local', 'country_code', 'store_address','final_status', 'payment_status', 'products', 'products_total','purchase_total_price']

  orders["money_diference_percentage"] = (orders["purchase_total_price"] - orders["products_total"]) / orders["products_total"] * 100

  under_authorized_by_country = check_by_group(orders, "country", 0, operator.lt)

  over_authorized_by_country= check_by_group(orders, "country", 20, operator.gt)

  under_authorized_by_store = check_by_group(orders, "store", 0, operator.lt)

  over_authorized_by_store = check_by_group(orders, "store", 20, operator.gt)