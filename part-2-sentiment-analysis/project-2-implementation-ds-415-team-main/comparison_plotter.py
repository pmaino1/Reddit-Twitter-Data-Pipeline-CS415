import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd


def main():
    
    
    df = pd.read_csv("gcp_vader.csv")
    #sort dataframe by gcp values, want to see similar linear curve from vader
    df.sort_values('gcp', inplace=True)
    #create lists for each column
    vader_list = df['vader'].tolist()
    gcp_list = df['gcp'].tolist()
    
    #plot vader points
    plt.plot(vader_list, label = "Vader")
    #plot gcp points
    plt.plot(gcp_list, label = "GCP")
    plt.legend()
    plt.ylabel("Respective Score")
    plt.show()
    #plt.savefig('comparison.png')
    
main()