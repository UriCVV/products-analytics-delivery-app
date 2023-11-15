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
  
def count_plot(df, xlabel=None, ylabel=None, figname=None):
  column1 = df.iloc[:, 0]
  column2 = df.iloc[:, 1]
  sns.barplot(data=df, x=column1, y=column2, palette="Blues")
  plt.xticks(rotation=45)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(figname)
  plt.savefig(f"./images/{figname}.png")
  plt.show()

def main_exploration():

  orders = pd.read_csv("./data/orders.csv", header=None)

  orders.columns =['order_id', 'activation_time_local', 'country_code', 'store_address','final_status', 'payment_status', 'products', 'products_total','purchase_total_price']

  orders["money_diference_percentage"] = (orders["purchase_total_price"] - orders["products_total"]) / orders["products_total"] * 100

  under_authorized_by_country = check_by_group(orders, "country", 0, operator.lt)

  over_authorized_by_country= check_by_group(orders, "country", 20, operator.gt)

  under_authorized_by_store = check_by_group(orders, "store", 0, operator.lt)

  over_authorized_by_store = check_by_group(orders, "store", 20, operator.gt)

  count_plot(under_authorized_by_country, figname="under_authorized_by_country")

  count_plot(over_authorized_by_country, figname="over_authorized_by_country")

  count_plot(under_authorized_by_store, figname="under_authorized_by_store")

  count_plot(over_authorized_by_store, figname="over_authorized_by_store")

  sns.scatterplot(data=orders, x='country_code', y='money_diference_percentage')
  plt.xticks(rotation=45)
  plt.xlabel("Countries")
  plt.ylabel("%Diference amount")
  plt.title("Percentage of diference between countries")
  plt.savefig("./images/percentage-of-diference-between-countries.png")
  plt.show()

  merged_by_country = pd.merge(under_authorized_by_country, over_authorized_by_country, on="country_code", how="inner")
  print(merged_by_country)

  merged_by_store = pd.merge(under_authorized_by_store, over_authorized_by_store, on="store_address", how="inner")
  print(merged_by_store)

  cleaned_orders = orders.query("final_status != 'CanceledStatus'")

  under_authorized_by_country_no_cancel = check_by_group(cleaned_orders, "country", 0, operator.lt)
  over_authorized_by_country_no_cancel = check_by_group(cleaned_orders, "country", 20, operator.gt)
  under_authorized_by_store_no_cancel = check_by_group(cleaned_orders, "store", 0, operator.lt)
  over_authorized_by_store_no_cancel = check_by_group(cleaned_orders, "store", 20, operator.gt)
  
  sns.scatterplot(data=cleaned_orders, x='country_code', y='money_diference_percentage')
  plt.xticks(rotation=45)
  plt.xlabel("Countries")
  plt.ylabel("%Diference amount")
  plt.title("Percentage of diference between countries without canceled orders")
  plt.savefig("./images/percentage-of-diference-between-countries-no-cancel.png")
  plt.show();

  orders.groupby("final_status")["purchase_total_price"].mean().reset_index()

  authorized = orders.query("money_diference_percentage > 0 and money_diference_percentage < 20")

  authorized["capture_amount"] = (authorized["products_total"] * 1.2) - authorized["purchase_total_price"]

  sns.scatterplot(data=authorized, x="order_id", y="capture_amount")

  print(authorized["capture_amount"].describe())