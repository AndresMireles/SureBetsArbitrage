from load_data.load_tennis_quotes_betfair import tennis_data_betfair
from load_data.load_tennis_quotes_bwin import tennis_data_bwin
from load_data.load_tennis_quotes_betway import tennis_data_betway
from load_data.load_tennis_quotes_williamhill import tennis_data_williamhill
#
import pandas as pd
import time


start = time.time()

pages = {'betfair': tennis_data_betfair,
         'bwin': tennis_data_bwin,
         'betway': tennis_data_betway,
         'williamhill': tennis_data_williamhill}

# We can skip this CSV part later for optimization
for [page, matches] in pages.items():
    try:
        data = pd.DataFrame.from_dict(
            matches(), orient='index').reset_index()
        data.columns = ['Match', '1', '2']
        data.to_csv(f'datos_tennis_{page}.csv', encoding='utf-8')
    except Exception as error:
        print(error)
#

matches_betfair = pd.read_csv('datos_tennis_betfair.csv', index_col=0)
matches_bwin = pd.read_csv('datos_tennis_bwin.csv', index_col=0)
matches_betway = pd.read_csv('datos_tennis_betway.csv', index_col=0)
matches_williamhill = pd.read_csv('datos_tennis_williamhill.csv', index_col=0)

names_betfair = list(matches_betfair['Match'])
names_bwin = list(matches_bwin['Match'])
names_betway = list(matches_betway['Match'])
names_williamhill = list(matches_williamhill['Match'])

names_list = [names_betfair, names_betway,
              names_bwin, names_williamhill]
dict_matches = {"Betfair": [names_betfair, matches_betfair],
                "Betway": [names_betway, matches_betway], "Bwin": [names_bwin, matches_bwin], "William Hill": [names_williamhill, matches_williamhill]}

# Store common matches:
common_names = []
for name_list in names_list:
    for other_name_list in names_list:
        if name_list != other_name_list:
            for name in name_list:
                if (name in other_name_list or (name.split(" ")[0][0:1] + " " + name.split(" ")[1]) in other_name_list) and (name not in common_names):
                    common_names.append(name)

print(common_names)

# Store each common match from each bookmaker with their respective odds:
matches_bak = {}
for [page, [name_list, matches_list]] in dict_matches.items():
    for name in common_names:
        if name in name_list:
            # If it's not yet in the list:
            if name not in matches_bak.keys():
                matches_bak[name] = {page: list(
                    matches_list.loc[matches_list['Match'] == name].to_dict('split')['data'][0][1:3])}
            else:
                matches_bak[name] = {**matches_bak[name], page: list(
                    matches_list.loc[matches_list['Match'] == name].to_dict('split')['data'][0][1:3])}

for [key, value] in matches_bak.items():
    print(key+': '+f'{value}')
    print("\n\n")

# Now we will check if the mathematical condition is met:
print("The good deals are: \n\n")
for [match, odds_bookmakers] in matches_bak.items():
    odds_first = []
    odds_second = []
    bookmakers = []
    for [bookmaker, odds] in odds_bookmakers.items():
        try:
            if type(odds[0]) == str:
                odds_first.append(float(odds[0].replace(",", ".")))
            else:
                odds_first.append(odds[0])

            if type(odds[1]) == str:
                odds_second.append(float(odds[1].replace(",", ".")))
            else:
                odds_second.append(odds[1])
        except:
            pass
        bookmakers.append(bookmaker)

    for odd in odds_first:
        for second_odd in odds_second:
            try:
                # Check if an arbitrage opportunity exists
                if odd > (1 + 1/(second_odd-1)) or second_odd > (1 + 1/(odd-1)):
                    print(match)
                    print(odds_bookmakers)

                    # Calculate the optimal bet allocation
                    total_stake = 1.00  # Let's assume we bet $1 on the first outcome
                    stake_on_second = total_stake * (odd / second_odd)  # Bet allocation for second outcome

                    # Calculate payouts to verify
                    payout_first = total_stake * odd
                    payout_second = stake_on_second * second_odd

                    print(
                        f'{match.split(" - ")[0]} ({bookmakers[odds_first.index(odd)]}). Odds: {odd}, Money: {total_stake}€.')
                    print(
                        f'{match.split(" - ")[1]} ({bookmakers[odds_second.index(second_odd)]}). Odds: {second_odd}, Money: {round(stake_on_second, 2)}€.')
                    
                    # Guaranteed payout should be the same
                    print(f'Payout for both outcomes: {round(payout_first, 2)}€')
                    profit = payout_first - (total_stake + stake_on_second)
                    print(f'Guaranteed profit: {round(profit, 2)}€\n')

            except:
                pass

end = time.time()

print("Elapsed time:", end-start)
