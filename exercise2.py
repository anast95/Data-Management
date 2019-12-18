#Anastasios Tzinieris
#2554
import sys

skyline = {}

def bnl(player, key_player):
    global skyline
    keys_found=[]
    part_domination=0
    domination=0

    for key in skyline:
        comparison=0
        for i in range(len(player)):
            if(int(skyline[key][i])<int(player[i])):
                comparison+=1
        if(comparison>0 and comparison<len(player)):
            part_domination=1
        elif(comparison==len(player)):
            domination=1
            keys_found.append(key)
        elif(comparison==0):
            part_domination=0
            domination=0
            break

    if(domination==1):
        for i in range(len(keys_found)):
            del skyline[keys_found[i]]

    if(part_domination==1 or domination==1):
        skyline[key_player]=player


def run(files_list):
    global skyline
    player =[]
    id_players={}
    all_csv = open('2017_ALL.csv', 'r')
    all_csv.readline()
    row = all_csv.readline()
    columns = row.split(',')
    skyline[int(columns[0])]=columns[1]
    m=0
    #print(players)
    for i in range(len(files_list)):
        player.append(columns[files_list[i] + 2])
    skyline[int(columns[0])]=player

    while(row!=''):
        player = []
        columns = row.split(',')
        id_players[int(columns[0])]=columns[1]
        for i in range(len(files_list)):
            player.append(columns[files_list[i] + 2])
        bnl(player, columns[0])
        row = all_csv.readline()

    for player in skyline:
        m+=1
        print(player,id_players[int(player)],skyline[player])
    print('\n')
    print("Total players in skyline = ",m)


def main():
    files_list = list(map(int, sys.argv[1].strip('[]').split(',')))
    run(files_list)


if __name__ == "__main__":
    main()
