import pandas as pd
import matplotlib.pyplot as plt


def load_and_calculate_indicators(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    # Sortuj dane według kolumny 'Date' w kolejności rosnącej
    data.sort_values('Date', ascending=True, inplace=True)

    # Filtrowanie danych począwszy od roku 2018
    start_date = pd.to_datetime("2018-01-01")
    data = data[data['Date'] >= start_date]

    # Ograniczenie danych do pierwszych 1000 rekordów od roku 2018
    data = data.head(1000)

    data.set_index('Date', inplace=True)

    # Oblicz MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Oblicz RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(span=14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(span=14, adjust=False).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


def simulate_trading_with_rsi(data, investment_per_trade):
    capital = 1000
    shares_owned = 0
    buy_dates, sell_dates = [], []  # Listy na daty transakcji kupna i sprzedaży

    for i in range(14, len(data)):  # Zaczynamy od 14, ponieważ RSI jest obliczany na 14 dniach
        # Sygnał kupna
        if data['MACD'].iloc[i] > data['Signal'].iloc[i] and data['RSI'].iloc[i] < 30:
            if capital >= investment_per_trade:
                bought_shares = investment_per_trade / data['Close'].iloc[i]
                shares_owned += bought_shares
                capital -= investment_per_trade
                buy_dates.append(data.index[i])  # Zapisz datę zakupu

        # Sygnał sprzedaży
        elif data['MACD'].iloc[i] < data['Signal'].iloc[i] and data['RSI'].iloc[i] > 70:
            # Sprzedaj tylko, jeśli coś kupiłeś wcześniej (lista buy_dates nie jest pusta)
            if shares_owned > 0 and buy_dates:
                capital += shares_owned * data['Close'].iloc[i]
                shares_owned = 0
                sell_dates.append(data.index[i])  # Zapisz datę sprzedaży

    final_capital = capital + shares_owned * data['Close'].iloc[-1]

    return final_capital, buy_dates, sell_dates



def plot_with_signals(data, buy_dates, sell_dates):

    plt.figure(figsize=(14, 10))

    # Wykres cen zamknięcia z sygnałami kupna i sprzedaży
    plt.plot(data.index, data['Close'], label='Cena Zamknięcia', color='skyblue')
    plt.scatter(buy_dates, data.loc[buy_dates]['Close'], label='Zakup', marker='^', color='green')
    plt.scatter(sell_dates, data.loc[sell_dates]['Close'], label='Sprzedaż', marker='v', color='red')
    plt.title('Cena Zamknięcia i Transakcje')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Wykres MACD
    plt.subplot(312)
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['Signal'], label='Linia Sygnału', color='orange')
    plt.title('Wskaźnik MACD')
    plt.legend()

    # Wykres RSI
    plt.subplot(313)
    plt.plot(data.index, data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', color='red', label='Przekupienie')
    plt.axhline(30, linestyle='--', color='green', label='Wyprzedanie')
    plt.title('Wskaźnik RSI')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    file_path = 'Binance_LTCUSDT_d.csv'
    data = load_and_calculate_indicators(file_path)
    data2 = load_and_calculate_indicators(file_path)

    final_capital, buy_dates, sell_dates = simulate_trading_with_rsi(data, 1000)
    final_capital2, buy_dates2, sell_dates2 = simulate_trading_with_rsi(data2, 250)


    print(f"Kapitał startowy: 1000")
    print(f"Kapitał końcowy przy stałym inwestowaniu 1000$: {final_capital:.2f}")
    print(f"Kapitał końcowy przy stałym inwestowaniu 250$: {final_capital2:.2f}")



    plot_with_signals(data, buy_dates, sell_dates)
    plot_with_signals(data2, buy_dates2, sell_dates2)


if __name__ == "__main__":
    main()
