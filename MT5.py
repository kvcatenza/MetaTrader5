import streamlit as st
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import time

# Initialize MetaTrader5
mt5.initialize()

# Streamlit app header
st.header("MetaTrader5 Dashboard")

# Sidebar login form
with st.sidebar:
    st.header("Login")
    with st.form("credentials"):
        login = int(st.text_input("ID", "99185"))
        password = st.text_input("Password", "Kvcatenza1!", type="password")
        server = st.selectbox("Server", ["FusionMarkets-Demo"])
        log = st.form_submit_button("Login")

        if log:
            try:
                logged_in = mt5.login(login, password, server)
                if logged_in:
                    st.success("Login successful")
                else:
                    st.error("Login failed")
            except ValueError:
                st.error("ID must be an integer")

def display_positions():
    positions = mt5.positions_get()

    if positions is None:
        placeholder.warning("No positions found, error code = " + str(mt5.last_error()))
    else:

        positions_data = []
        for position in positions:
            positions_data.append([
                position.symbol,
                str(position.ticket).replace(",", ""),
                datetime.fromtimestamp(position.time).strftime('%Y-%m-%d %H:%M:%S'),
                'BUY' if position.type == 0 else 'SELL',
                position.volume,
                position.price_open,
                position.sl,
                position.tp,
                mt5.symbol_info_tick(position.symbol).bid if position.type == 1 else mt5.symbol_info_tick(position.symbol).ask,
                position.profit
            ])


        df = pd.DataFrame(positions_data, columns=['Symbol', 'Ticket', 'Time', 'Type', 'Volume', 'Price', 'S/L', 'T/P', 'Current Price', 'Profit'])


        df.set_index('Symbol', inplace=True)
        with placeholder.container():
            st.write(f"Number of current positions: {len(positions)}")
            st.write(df)


if 'logged_in' in locals() and logged_in:
    st.subheader(f"Server: {server}")

    placeholder = st.empty()

    while True:
        display_positions()
        time.sleep(0.1)
else:
    st.write("Please log in to view your positions.")
