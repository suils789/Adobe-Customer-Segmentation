import numpy as np
import pandas as pd
import math as mt
import matplotlib.pyplot as plt
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--clusters", type=int, help="Number of Clusters", default=5)
parser.add_argument("--metric", type=str, choices=["Calinski-Harabaz"], help="Clustering Evaluation Metric",
                    default="Calinski-Harabaz")
parser.add_argument("--model", type=str, choices=["K-means", "Encoder+K-means", "Matrix Factorization + K-means"],
                    help="Model to be used", default="K-means")
args = parser.parse_args()

print("Running with the following configuration:")
print ("Model: " + args.model)
print ("Metric: " + args.metric)
print ("Number of Clusters: " + str(args.clusters))

if args.model == "K-means":
    print("Use K-means model here")
elif args.model == "Encoder+K-means":
    print("Use Auto-Encoder + K-means here")
else:
    print("Use MF + K-means here")


print("Calculate the "+ args.metric + " Metric")
