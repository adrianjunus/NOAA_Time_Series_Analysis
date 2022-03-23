###########################################
#             Adrian Junus                #
#             CSE 160                     #
#             Final Project               #
# Charactizing Hurricanes using Wave Data #
###########################################

import os
import matplotlib.pyplot as plt
import numpy

# Beaufort Scale details provided by NOAA, the 
# National Oceanic and Atmospheric Administration.

def txt_file_to_dict(filename,metric_string):
    """ 
    Imports a text file containing standard meteorological data 
    proivded by the National Data Buoy Center and returns "data_list", a list of
    dictionaries with the keys (WSPD, metric_string)
    """

    metric_index = {"Wind Speed": 6,"Wave Height": 8, "Air Pressure": 12}
    
    myFile = open(filename)
    data_list = []
    skip_first_two_lines = 0
    
    
    # extract data from month of august, for desired metric, excluding
    # large values. According to NDBC, 99.0 in the data represents null
    # values. There are also some spikes i manually ejected with the > 30
    # criterion.
    
    for line in myFile:
        dic = {}
        a = line.split()
        if skip_first_two_lines > 2 and float(a[6]) < 30.0  and float(a[8]) < 30.0 and a[1] == '08': 
            dic["Date and Time"] = a[0]+"/"+a[1]+"/"+a[2]+" "+ a[3]+":"+a[4]+":"+a[5]
            dic["Wind Speed"] = float(a[6])
            dic[metric_string] = float(a[metric_index[metric_string]])
            data_list.append(dic)
        else:
            skip_first_two_lines += 1
        
    return data_list


def myplot(xs, ys):
    """
    Plots the dictionaries metric and datum
    """

    plt.plot(xs,ys, linestyle = '-')
    
def setup_plot():
    """
    Plots the dictionaries metric and datum
    """
    
    plt.xlabel("Date and Time")
    plt.ylabel("Storm Rank")
    

def finish_plot(elt):
    """
    Plots the dictionaries metric and datum
    """
    
    plt.legend()
    plt.show()
    plt.savefig(elt + ".png")

    
def mean_squared_error(metric_rank,datum_rank):
    """ Takes too list of identical length, of integers, and returns
    the Mean Square error.
    """
    
    MSE_denom = len(metric_rank)
    MSE_numer = 0

    for i in range(len(metric_rank)):
        # Sum the square of the differences
        MSE_numer += (metric_rank[i] - datum_rank[i])**2
    
    MSE = MSE_numer / float(MSE_denom)
    return MSE
    
def apply_rank_to_storm(ranking,data_list,metric_string):
    """
    Takes in main data list for any data, and ranks them based on the
    passed in ranking system, returns as list of lists of [date and time, rank int].
    """
    ranked_data = []
    i = 0
    
    # compares data value to subsequently larger rankings, appending the 
    # smallest rank to our list.
    for dic in data_list:
        while i < len(ranking):
            if dic[metric_string] <= ranking[i][0]:
                ranked_data.append(ranking[i][1])
                i = len(ranking)
            i += 1
        i = 0
            
    return ranked_data
                
        
def create_rank(scale, metric_string):
    """ 
    Takes the scale, a dict of {"Wind Speed": unique value, metric_string: metric value}
    and a string, metric_string creates a new list of lists [metric value : rank]
    """
    
    rank = []
    
    # builds rank by reorganizing the input scale, based on the metric
    for dic in scale:
        rank.append([dic[metric_string],classify_Beaufort(dic["Wind Speed"])])
        
    rank.sort()
    
    return rank

def create_scale(data_list,unique_list, metric_string):
    """
    Takes in a list of dictionaries and creates a scale, or list of dictionaries 
    mapping from {"Wind Speed" : unique speed, "Metric" : metric average value}.
    """
    
    rank = []
    
    # traverse the unique list of wind speeds found in the data
    # and finds all metric values corresponding to that value
    # in the data
    for elt in unique_list:
        new_dic = {}
        new_dic.setdefault("Wind Speed",elt)
        new_dic.setdefault(metric_string, find_avg(list_metric(data_list,elt,metric_string)))
        rank.append(new_dic)
    
    return rank

def clean_up_rank(ranking):
    """ 
    Converts a ranking (list of lists) to a list of lists of 
    [max metric of a ranking, rank]
    """
    
    
    # Traverse the rank (in this case "rough_new_rank") backwards, finds the 
    # first storm ranking using this method to find the max metric value
    # of a rank, and puts this in the list decribed in the docstring
    used_ranks = set()
    clean_ranking = []
    
    for i in range(-1,-len(ranking),-1):
        if ranking[i][1] not in used_ranks:
            used_ranks = set([ranking[i][1]]) | used_ranks
            clean_ranking.append(ranking[i])
    
    clean_ranking.sort()
    return clean_ranking
        

def list_unique_wndspd(data_list):
    """ 
    Takes the main list of dictionaries and returns a sorted list of the
    unique wind speeds.
    """
    unique_list = []
    
    # basically makes a set, but is a list
    for dic in data_list:
        if dic["Wind Speed"] not in unique_list:
            unique_list.append(dic["Wind Speed"])
            
    unique_list.sort()

    return unique_list

    
def list_metric(data_list,wndspd_float,metric_string):
    """ 
    Takes main data list, uses wndspd_float to find wave heights
    that correspsond to that value in the data. Returns a dictionary
    of {wndspd_float:[list of metric floats]}
    """
    
    list_of_metrics = []
    
    # scours the main data for metric values corresponding to 
    # the passed in wind speed
    for dic in data_list:
        if dic["Wind Speed"] == wndspd_float:
            list_of_metrics.append(dic[metric_string])
    
    return list_of_metrics
    

def find_avg(lst):
    """
    Takes a list and returns the integer average of that list.
    """
    
    return float("%.1f" % numpy.mean(lst))


def classify_Beaufort(wndspd_float):
    """
    Takes a wind speed and returns a Beaufort scale ranking.
    """

    convert = wndspd_float/.514 # 1 knot = .514 m/s, Beaufort is in knots
    
    if wndspd_float < 1:
        return 0
        
    elif wndspd_float <= 3:
        return 1
    
    elif wndspd_float <= 6:
        return 2
    
    elif wndspd_float <= 10:
        return 3
    
    elif wndspd_float <= 16:
        return 4
    
    elif wndspd_float <= 21:
        return 5
    
    elif wndspd_float <= 27:
        return 6

    elif wndspd_float <= 33:
        return 7
    
    elif wndspd_float <= 40:
        return 8
    
    elif wndspd_float <= 47:
        return 9
    
    elif wndspd_float <= 55:
        return 10
    
    elif wndspd_float <= 63:
        return 11
    
    else:
        return 12
        
        
# The code in this function is executed when this file is run as a Python program
def main():
    
    
    #Create a rank, and apply it and plot it against other data sets
    FI = "C:\\Users\\junus\\Downloads\\dsd\\Florida_Irene.txt"
    DK = "C:\\Users\\junus\\Downloads\\dsd\\Dauphin_Katrina.txt"
    LK = "C:\\Users\\junus\\Downloads\\dsd\\Louisiana_Katrina.txt"
    city_index = [FI,DK,LK]
    metric_index = ['Wave Height', 'Air Pressure']
    
    print("Report MSE against Beaufort Datum")
    print(" ")
    
    for elt in city_index:
        for elt2 in metric_index:
            
            # Build our ranking system off of our base data
            main_data_list = txt_file_to_dict(FI,elt2)
            unique_list = list_unique_wndspd(main_data_list)
            scale = create_scale(main_data_list,unique_list,elt2)
            rough_Beaufort_rank = create_rank(scale, "Wind Speed")
            rough_new_rank = create_rank(scale, elt2)
            Beaufort_rank = clean_up_rank(rough_Beaufort_rank)
            New_rank = clean_up_rank(rough_new_rank)
            
            # Apply the ranking system to new data
            data_list = txt_file_to_dict(elt,elt2)
            new_plot = apply_rank_to_storm(New_rank,data_list,elt2)
            wind_plot = apply_rank_to_storm(Beaufort_rank,data_list,"Wind Speed")
            
            # Reliability/consistency of ranking system?
            mse = mean_squared_error(new_plot,wind_plot)
            
            print("MSE for " + elt2 + " for " + elt + "... " + str(mse))
            
            plt.figure(city_index.index(elt))
            plt.figure(city_index.index(elt)).subplots_adjust(hspace=.5)
            #plt.subplot(int("21"+str(metric_index.index(elt2))))
            plt.title(elt2 + " for " + elt)
            setup_plot()
            myplot(range(len(wind_plot)),wind_plot)
            myplot(range(len(new_plot)),new_plot)
        finish_plot(elt) 
            

if __name__ == "__main__":
    main()