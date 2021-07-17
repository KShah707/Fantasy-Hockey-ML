def add_rate_stats(df, stats, time=''):
    for stat in stats:
        df[stat+'/60'+time] = (df[stat]/df[time+'TOI']*3600).fillna(0)
    return df