import csv
import statistics
import math

# process fly ball woba and turn into list of tuples (player_id, woba)
def process_flyball_woba() -> list:
    file_name = open("pull_flyball_woba.csv")
    pull_woba = csv.reader(file_name)
    data = []
    for row in pull_woba:
        player_id = int(row[0])
        woba = float(row[1])
        data.append((player_id, woba))
    return data

# process line drive woba and turn into list of tuples (player_id, woba)
def process_linedrive_woba() -> list:
    file_name = open("push_linedrive_woba.csv")
    push_woba = csv.reader(file_name)
    data = []
    for row in push_woba:
        player_id = int(row[0])
        woba = float(row[1])
        data.append((player_id, woba))
    return data

# process ball in play woba and turn into list of tuples (player_id, woba)
def process_ball_in_play_woba() -> list:
    file_name = open("ball_in_play_woba.csv")
    ball_in_play_woba = csv.reader(file_name)
    data = []
    for row in ball_in_play_woba:
        player_id = int(row[0])
        woba = float(row[1])
        data.append((player_id, woba))
    return data

def process_flyball_data() -> list:
    file_name = open("flyball_woba.csv")
    flyball_woba = csv.reader(file_name)
    data = []
    for row in flyball_woba:
        player_id = int(row[0])
        woba = float(row[1])
        data.append((player_id, woba))
    return data

# trim ball in play woba down to same set of players for comparison
def trim_list(specific_data, ball_in_play) -> list:
    new_bip_list = []
    player_ids_in_bip = []
    for entry in ball_in_play:
        player_ids_in_bip.append(entry[0])
    inds = []
    for entry in specific_data:
        player_id = entry[0]
        # computationally inefficient but whateva
        for i in range(len(player_ids_in_bip)):
            if player_ids_in_bip[i] == player_id:
                inds.append(i)
    for i in inds:
        new_bip_list.append(ball_in_play[i])
    return new_bip_list

# get list of differences flyballwoba - ballinplaywoba
# player ids should be identical and sorted, so we will be comparing same player at each step
def get_differences(specific_data, ball_in_play) -> list:
    diff = []
    for i in range(len(specific_data)):
        diff.append(specific_data[i][1] - ball_in_play[i][1])
    return diff

# get stats necessary for test statistic calculation
def calc_stats(diff):
    mean = statistics.mean(diff)
    stdDev = statistics.stdev(diff)
    n = len(diff)
    return (mean, stdDev, n)

def calc_regular_mean(data):
    for i in range(len(data)):
        data[i] = data[i][1]
    return statistics.mean(data)    

# calculate t_0
def test_statistic(diff, delta):
    mean, stdDev, n = calc_stats(diff)
    test_stat = (mean - delta) / (stdDev / math.sqrt(n))
    return test_stat
    
def main():
    
    flyball_woba = process_flyball_woba()
    linedrive_woba = process_linedrive_woba()
    ball_in_play_woba = process_ball_in_play_woba()
        
    fb_ball_in_play_woba = trim_list(flyball_woba, ball_in_play_woba)
    ld_ball_in_play_woba = trim_list(linedrive_woba, ball_in_play_woba)
    
    flyball_diff = get_differences(flyball_woba, fb_ball_in_play_woba)
    linedrive_diff = get_differences(linedrive_woba, ld_ball_in_play_woba)
    
    print("REGULAR wOBA MEAN: ", calc_regular_mean(ld_ball_in_play_woba)) # edit based on if you're checking the flyball hitters or the linedrivers
    print("FLYBALL wOBA MEAN: ", calc_regular_mean(flyball_woba))
    print("LINEDRIVE wOBA MEAN: ", calc_regular_mean(linedrive_woba))
    
    print("FLYBALL STATS: mean, std, n", calc_stats(flyball_diff))
    print("LINEDRIVE STATS: mean, std, n", calc_stats(linedrive_diff))
    
    print("TEST STATISTIC FLYBALL WOBA: ", test_statistic(flyball_diff, 0))
    print("TEST STATISTIC LINEDRIVE WOBA: ", test_statistic(linedrive_diff, 0))
    
main()