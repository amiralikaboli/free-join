#!/usr/bin/env python3

import json
import os
import statistics
import sys

import matplotlib.pyplot as plt
import numpy as np


def geometric_mean(arr1, arr2):
	return round(np.prod(np.array(arr2) / np.array(arr1)) ** (1 / len(arr1)), 2)


if __name__ == '__main__':
	args = sys.argv[1:]
	mode = args[0] if args else "gj"

	if mode == "gj":
		alt = "gj"
	else:
		alt = "fj_scalar_colt"

	with open(f"{os.path.dirname(__file__)}/../gj/gj.json") as json_file:
		results = json.load(json_file)
	queries = [result["query"] for result in results["ours"]]

	duckdb_results = []
	for result in results["duckdb"]:
		if result["query"] in queries:
			duckdb_results.append((result["query"], float(result["time"])))
	duckdb_results = sorted(duckdb_results)
	duckdb_times = [result[1] for result in duckdb_results]

	ours_results = sorted([(result["query"], float(result["time"])) for result in results["ours"]])
	queries = [result[0] for result in ours_results]
	ours_times = [result[1] for result in ours_results]

	gj_results = sorted([(result["query"], statistics.mean(result["time"])) for result in results[alt]])
	gj_results = [result for result in gj_results if result[0] in queries]
	gj_times = [result[1] for result in gj_results]

	print(f'DuckDB Speedup: {geometric_mean(ours_times, duckdb_times)}x')
	print(f'{mode.upper()} Speedup: {geometric_mean(ours_times, gj_times)}x')

	plt.figure(figsize=(12, 5))
	ratio = 1.2

	plt.subplot(1, 2, 1)
	plt.scatter(gj_times, ours_times, color="orange", s=10)
	points = [max(min(gj_times), min(ours_times)) / ratio, min(max(gj_times), max(ours_times)) * ratio]
	plt.plot(points, points, color="gray")
	plt.xscale("log")
	plt.yscale("log")
	plt.xlabel(f"{mode.upper()} (s)")
	plt.ylabel("Ours (s)")

	plt.subplot(1, 2, 2)
	plt.scatter(duckdb_times, ours_times, color="orange", s=10)
	points = [max(min(duckdb_times), min(ours_times)) / ratio, min(max(duckdb_times), max(ours_times)) * ratio]
	plt.plot(points, points, color="gray")
	plt.xscale("log")
	plt.yscale("log")
	plt.xlabel("DuckDB (s)")
	plt.ylabel("Ours (s)")

	plt.show()
