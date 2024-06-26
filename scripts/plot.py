#!/usr/bin/env python3

import json
import os
import statistics

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
	with open(f"{os.path.dirname(__file__)}/../gj/gj.json") as json_file:
		results = json.load(json_file)

	queries = []
	if 'ours' in results:
		queries = [result["query"] for result in results["ours"]]

	duckdb_results = []
	for result in results["duckdb"]:
		if not queries or result["query"] in queries:
			duckdb_results.append((result["query"], float(result["time"])))
	duckdb_results = sorted(duckdb_results)
	xs = [result[1] for result in duckdb_results]

	ys = []
	legend = []
	if 'ours' in results:
		ours_results = sorted([(result["query"], float(result["time"])) for result in results["ours"]])
		ours_ys = [result[1] for result in ours_results]
		ys.extend(ours_ys)
		plt.scatter(xs, ours_ys, color="orange", s=10)
		legend.append("Ours")

	if 'gj' in results:
		gj_results = sorted([(result["query"], statistics.mean(result["time"])) for result in results["gj"]])
		if queries:
			gj_results = [result for result in gj_results if result[0] in queries]
		gj_ys = [result[1] for result in gj_results]
		ys.extend(gj_ys)
		plt.scatter(xs, gj_ys, color="silver", s=10)
		legend.append("GJ")
		if 'ours' in results:
			print(f'GJ Speedup: {round(np.prod(np.array(gj_ys) / np.array(ours_ys)) ** (1 / len(gj_ys)), 2)}x')

	if 'fj' in results:
		fj_results = sorted([(result["query"], statistics.mean(result["time"])) for result in results["fj"]])
		if queries:
			fj_results = [result for result in fj_results if result[0] in queries]
		fj_ys = [result[1] for result in fj_results]
		ys.extend(fj_ys)
		plt.scatter(xs, fj_ys, color="black", s=10)
		legend.append("FJ")

	plt.legend(legend)
	plt.xlabel("DuckDB (s)")
	plt.ylabel("Join (s)")

	ratio = 1.2
	mn_x, mx_x = min(xs), max(xs)
	mn_y, mx_y = min(ys), max(ys)
	xs = [max(mn_x, mn_y) / ratio, min(mx_x, mx_y) * ratio]
	ys = [max(mn_x, mn_y) / ratio, min(mx_x, mx_y) * ratio]
	plt.plot(xs, ys, color="gray")

	plt.xscale("log")
	plt.yscale("log")
	plt.show()
