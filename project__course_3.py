"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv


MAIN_INFO = {"masterfile": "Master_2016_short.csv",   # Name of Master CSV file
                        "battingfile": "batting2.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}


##
## Provided code from Week 3 Project
##

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table

# The following lines are for testing sample datasets during the program construction
# my_list= read_csv_as_list_dict("batting2.csv", ',', '"')
# print (my_list)

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

# my_dict= read_csv_as_nested_dict("batting2.csv", 'playerID', ',', "'")
# print (my_dict)

##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500

def batting_average(info, batting_stats): # info
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]]) 
    at_bats = float(batting_stats[info["atbats"]]) 
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0
 
def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0

def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid): 
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """    
    
    # !!!The following 4 lines are an alternative to the Lambda line beneath. I chose to go with the Lambda
    # filtered_statistics = []
    # for row in statistics:
        #if row[yearid] == year:
            #filtered_statistics.append(row)
    
    # In the following line, the 'year' variable is not a string, assuming that the input for the\
    # function is an int. This is the reason why I added str(), in the file it is written as a str.
    filtered_statistics = list(filter(lambda row: row[yearid] == str(year), statistics)) 
    
    return filtered_statistics

# The following lines are a test for filter_by_year(statistics, year, yearid)
# 'my_list' is from a test for the function read_csv_as_list_dict(filename, separator, quote)
# only_2005 = filter_by_year(my_list, 2011, "yearID")
# print (only_2005)


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    
    
    # 'all_result' is a list of tuples with (playerid, stat). 
    all_result = []
    
    # For each row we will insert into each tuple the id('id_per_row'), and the relevant\
    # statistics ('id_stat')
    for row in statistics:
        id_per_row = row[info['playerid']]
        id_stat = formula(info, row)
        # Now creating the tuple
        id_result = (id_per_row, id_stat) 
        all_result.append(id_result)
    
    # In order to pick the top players, we need first to sort the tuples by their result.
    top_players = []
    all_result.sort(key=lambda pair: pair[1], reverse=True)
    
    # Now we ask the program to make a list of the top players. 
    for seq in range(numplayers):
        top_players.append(all_result[seq])
            
    return top_players

# The following 'print' is a test for top_player_ids function
# 'my_list' is from a test for the function read_csv_as_list_dict(filename, separator, quote)
# print (top_player_ids(MAIN_INFO, my_list, batting_average, 3))


def lookup_player_names(info, top_ids_and_stats): 
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    
    # 'list_of_names' is the required output
    list_of_names = []
    
    # We need to handle each tuple separately
    for tup in top_ids_and_stats:
        player_id_tup = tup[0]
        grade_id_tup = tup[1]
        # The following line extracts the row of the relevant layer from the master file
        relevant_row = list(filter(lambda row: row[info['playerid']] == player_id_tup,\
                                          read_csv_as_list_dict(info["masterfile"], ',', '"')))
        # The following couple of lines extract the first and last names from the above row.
        # The '[0]' at the middle is required since the dictionary(the row) is hidingnow within\
        # The new list created above in the filter line
        first = relevant_row[0][info['firstname']]
        last = relevant_row[0][info['lastname']]
        player_string = "{0:.3f} --- {1} {2}".format(grade_id_tup, first, last)
        # player_string = str(grade_id_tup) + " --- " + first + " " + last
        list_of_names.append(player_string)
        
    return list_of_names


# The following 'print' is a test for lookup_player_names function 
# print (lookup_player_names(MAIN_INFO, check_list))

def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    my_list = read_csv_as_list_dict(info["battingfile"], ',', '"')
    filtered_data = filter_by_year(my_list, year, info['yearid'])
    top_players = top_player_ids(info,filtered_data , formula, numplayers)
    top_names_by_year = lookup_player_names(info, top_players)
    
    return top_names_by_year

# The following two lines are a test for compute_top_stats_year function
# result = compute_top_stats_year(MAIN_INFO, batting_average, 4, 2007)
# print (result)


## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields): 
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    # 'agg_stat_dict' is the outer dictionary and th eputput of the fuction.
    agg_stat_dict = {}
    
    # 'list_of_ids' is a list of all players in the data. 
    list_of_ids = []
    for row in statistics:
        id_per_row = row[playerid]
        list_of_ids.append(id_per_row)
        
    # id_list gives us a list of players with duplication. Using 'set' we eliminate the\
    # duplicaitons. Will be used as the keys for outer dict.
    unique_id_list = set(list_of_ids)
    
    for player in unique_id_list:
        # For each player we need to filter the file so that we have only his data.
        id_stat = list(filter(lambda row: row[playerid] == player, statistics))
        # 'local_dict' is the inner dictionary. Each field will be added to this dict.
        local_dict = {}
        for field in fields:
            local_dict['playerID'] = player
            sum_field = 0
            for id_row in id_stat:
                # On the line below we aggregate all the rows for the specific field.
                sum_field += float(id_row[field])
            local_dict[field] = sum_field #This line append the field to the inner dict.
        agg_stat_dict[player] = local_dict #This line append the playerid to the outer dict.
    
    return agg_stat_dict

# The following two lines are a test for aggregate_by_player_id function
# my_result = aggregate_by_player_id(my_list, MAIN_INFO["playerid"], MAIN_INFO["battingfields"]) 
# print (my_result)

def compute_top_stats_career(info, formula, numplayers): 
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    # 'aggregate_by_player_id' function provides a dictionary, and we need a list.
    agg_stat_list = []
    # So we take the value of each key in 'aggregate_by_player_id' into our list.
    for local_dict in aggregate_by_player_id(read_csv_as_list_dict(info["battingfile"], ',', '"'), info["playerid"], \
                                                     info["battingfields"]).values():
        id_agg_stat = local_dict
        agg_stat_list.append(id_agg_stat)
    # We use the function 'top_player_ids' to calculate the top players.
    top_players_career = top_player_ids(info, agg_stat_list, formula, numplayers)
    # The next line is the output of the function.
    top_names_by_career = lookup_player_names(info, top_players_career)    
        
    return top_names_by_career

# The following 'print' is a test for compute_top_stats_career function
# print (compute_top_stats_career(MAIN_INFO, batting_average, 3))

##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

#test_baseball_statistics()