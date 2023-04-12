# -*- coding: utf-8 -*-
"""
Author: Andrew deBerardinis
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

'''
    Shows how Blocks Per Game in the NBA is predicated on height.
    Blocks Per Game go up as NBA Players get taller.
'''
def nba_scatter_HT_BLPG():
    df = pd.read_csv('NBA_Players.csv', index_col=0)
    height = df[' HT']
    blkpg = df[' BLKPG']
    plt.plot(height, blkpg, linestyle='', marker='o')
    plt.xlabel("NBA Player's Height(cm)", fontsize=18)
    plt.ylabel("NBA Player's Blocks Per Game", fontsize=18)
    m, b = np.polyfit(height, blkpg, 1)
    plt.plot(height, m*height + b) #Add regression line
    plt.show()
    
'''
    Shows that the NBA is a young league and the most players fall
    in the category of having a year or two of experience in the NBA.
'''
def nba_hist_Experience():
    df = pd.read_csv('NBA_Players.csv', index_col=0)
    exp = df[' EXPERIENCE']
    plt.hist(exp, bins = 10)
    plt.xlabel("NBA Player's Experience(Years)", fontsize=18)
    plt.ylabel("Number of NBA Players", fontsize=18)
    plt.show()
    
'''
    Also shows that the NBA is a young league but shows that most NBA
    Players are in their low-mid 20's.
'''
def nba_hist_Age():
    df = pd.read_csv('NBA_Players.csv', index_col=0)
    age = df[' AGE'].sort_values()
    plt.hist(age)
    plt.xlabel("NBA Player's Age", fontsize=18)
    plt.ylabel("Number of NBA Players", fontsize=18)
    plt.show()
    
'''
    The Experience and Age Histograms show that the NBA is comprised of
    mostly 20 year olds, and most of them are low-mid 20's, but also shows 
    that Players don't last long in the NBA. Most NBA Players play in the
    NBA 5 years or less.
'''
def main():
    nba_scatter_HT_BLPG()
    nba_hist_Experience()
    nba_hist_Age()

main()

