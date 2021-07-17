import pandas as pd

def load_kaggle_player_games(timezone='US/Eastern'):
    # Read boxscores
    df = pd.read_csv('kaggle-NHL-Game-Data/game_skater_stats_NEW.csv', delimiter=',')
    # Extract only Yahoo-relevant stats
    df = df.loc[:, 
        [
            'game_id',
            'player_id',
            'timeOnIce',
            'goals',
            'assists',
            'plusMinus',
            'powerPlayTimeOnIce',
            'powerPlayGoals',
            'powerPlayAssists',
            'shortHandedTimeOnIce',
            'shortHandedGoals',
            'shortHandedAssists',
            'shots',
            'hits',
            'blocked',
            'team_id'
        ]]
    df.rename(
        columns={
            'player_id': 'p',
            'goals': 'G',
            'assists': 'A',
            'plusMinus': '+/-',
            'timeOnIce': 'TOI',
            'powerPlayTimeOnIce': 'PPTOI',
            'powerPlayGoals': 'PPG',
            'powerPlayAssists': 'PPA',
            'shortHandedTimeOnIce': 'SHTOI',
            'shortHandedGoals': 'SHG',
            'shortHandedAssists': 'SHA',
            'shots': 'S',
            'hits': 'HIT',
            'blocked': 'BLK'
        },
        inplace=True)
    df['GP'] = 1
    df['PPP'] = df['PPG'] + df['PPA']
    df['SHP'] = df['SHG'] + df['SHA']
    
    # Add game time info
    df_games = pd.read_csv('kaggle-NHL-Game-Data/game_NEW.csv', delimiter=',', parse_dates=['date_time_GMT'])
    df_games = df_games[['game_id', 'date_time_GMT', 'season']]
    df_games['dt'] = df_games['date_time_GMT'].dt.tz_convert(timezone)
    df_games.drop(['date_time_GMT'], axis=1, inplace=True)
    
    df_games = df_games.set_index('game_id')
    df = df.join(df_games, on='game_id', how='left')

    # Add player descriptive info
    df_players = pd.read_csv('kaggle-NHL-Game-Data/player_info_NEW.csv', delimiter=',', parse_dates=['birthDate'])
    df_players = df_players[['player_id', 'primaryPosition', 'birthDate', 'firstName', 'lastName']]
    df_players['Fwd'] = (df_players['primaryPosition'] != 'D')

    df_players = df_players.set_index('player_id')
    df = df.join(df_players, on='p', how='left')

    df['Age'] = (df['dt'].astype('datetime64[ns]') - df['birthDate'])/pd.Timedelta('365 days')
    df.drop(['birthDate', 'primaryPosition'], axis=1, inplace=True)
    
    # Reindex by player-date and return
    df.drop_duplicates(['p', 'dt'], inplace=True)
    df.set_index(['p', 'dt'], verify_integrity=True, inplace=True)
    df.sort_values(['p', 'dt'], ascending=True, inplace=True)
    return df