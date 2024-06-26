import csv
import os

import pandas as pd

if __name__ == '__main__':
	except_queries = []
	for path, dir_list, file_list in os.walk("imdb"):
		for file_name in file_list:
			if file_name.endswith(".parquet"):
				print(file_name)
				df = pd.read_parquet(os.path.join(path, file_name))
				for col in df.columns:
					if df[col].dtype == "int32":
						df[col] = df[col].fillna(-1)
					elif df[col].dtype == "float64":
						df[col] = df[col].fillna(-1).astype("int32")
					# elif df[col].dtype == "object":
					# 	df[col] = df[col].str.replace('"', '').replace('|', '')
				try:
					df.to_csv(
						os.path.join("imdb_csv", file_name.replace("parquet", "csv")),
						index=False,
						header=False,
						sep="|",
						quoting=csv.QUOTE_NONE
					)
				except:
					except_queries.append(os.path.join(path, file_name))
					df.to_csv(
						os.path.join("imdb_csv", file_name.replace("parquet", "csv")),
						index=False,
						header=False,
						sep="|",
						quoting=csv.QUOTE_MINIMAL
					)

	print("Except queries:", except_queries)
