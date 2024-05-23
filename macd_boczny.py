import pandas as pd
import matplotlib.pyplot as plt
def calculate_ema(prices, days, smoothing=2):
    return prices.ewm(span=days, adjust=False).mean()


def load_and_calculate_indicators(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values('Date', ascending=True, inplace=True)

    data.set_index('Date', inplace=True)
    start_date = pd.to_datetime("2022-04-01")

    filtered_data = data.loc[start_date:].copy()

    filtered_data['EMA26'] = calculate_ema(filtered_data['Close'], 26)
    filtered_data['EMA12'] = calculate_ema(filtered_data['Close'], 12)
    filtered_data['MACD'] = filtered_data['EMA12'] - filtered_data['EMA26']
    filtered_data['Signal'] = calculate_ema(filtered_data['MACD'], 9)

    return filtered_data


def plot_with_signals2(data):
    cross_up = (data['MACD'] > data['Signal']) & (data['MACD'].shift() < data['Signal'].shift())
    cross_down = (data['MACD'] < data['Signal']) & (data['MACD'].shift() > data['Signal'].shift())

    plt.figure(figsize=(14, 7))

    # Wykres MACD z linią sygnału
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['Signal'], label='Linia Sygnału', color='orange')

    # Dodanie sygnałów kupna i sprzedaży
    plt.scatter(data.index[cross_up], data['MACD'][cross_up], color='green', marker='^', label='Sygnał Kupna', alpha=1)
    plt.scatter(data.index[cross_down], data['MACD'][cross_down], color='red', marker='v', label='Sygnał Sprzedaży',
                alpha=1)

    plt.title('Wskaźnik MACD')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.tight_layout()
    plt.show()


def simulate_trading(data, positions_limit):
    initial_capital = 1000.0
    capital = initial_capital
    positions = []
    transactions = {'buy': [], 'sell': []}
    position_cost = capital / positions_limit

    cross_up = (data['MACD'] > data['Signal']) & (data['MACD'].shift() < data['Signal'].shift())
    cross_down = (data['MACD'] < data['Signal']) & (data['MACD'].shift() > data['Signal'].shift())

    for i in range(1, len(data)):
        if cross_up.iloc[i] and len(positions) < positions_limit:
            investment_per_trade = position_cost
            shares_bought = investment_per_trade / data['Close'].iloc[i]
            positions.append((shares_bought, data['Close'].iloc[i]))
            capital -= investment_per_trade
            transactions['buy'].append(data.index[i])
        elif cross_down.iloc[i] and positions:
            for shares_bought, purchase_price in positions:
                capital += shares_bought * data['Close'].iloc[i]
            positions.clear()
            transactions['sell'].append(data.index[i])
            position_cost = capital / positions_limit

    for shares_bought, _ in positions:
        capital += shares_bought * data['Close'].iloc[-1]
    positions.clear()

    final_value = capital
    profit_loss = final_value - initial_capital

    return transactions, final_value, profit_loss


def plot_with_signals(data, transactions):
    plt.figure(figsize=(14, 7))

    plt.plot(data.index, data['Close'], label='Cena Zamknięcia', color='skyblue')
    plt.scatter(transactions['buy'], data.loc[transactions['buy']]['Close'], label='Zakup', marker='^', color='green',
                alpha=1)
    plt.scatter(transactions['sell'], data.loc[transactions['sell']]['Close'], label='Sprzedaż', marker='v',
                color='red', alpha=1)

    plt.title('Cena Zamknięcia LTC/USDT i Transakcje')
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    file_path = 'Binance_LTCUSDT_d.csv'
    data = load_and_calculate_indicators(file_path)
    transactions, final_value, profit_loss = simulate_trading(data, 1)
    print(f"Kapitał końcowy: {final_value:.2f}")
    print(f"Zysk/Strata: {profit_loss:.2f}")
    plot_with_signals(data, transactions)

    transactions, final_value, profit_loss = simulate_trading(data, 4)
    print(f"Kapitał końcowy: {final_value:.2f}")
    print(f"Zysk/Strata: {profit_loss:.2f}")
    plot_with_signals(data, transactions)
    plot_with_signals2(data)


if __name__ == "__main__":
    main()