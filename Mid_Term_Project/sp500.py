import streamlit as st
import pandas as pd
import base64
import altair as alt
import yfinance as yf
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

st.title('S&P 500 Stock Price Analysis - User Guide (by Arsh Ahtsham)')

# Load the original image
image = Image.open("sp.jpg")

# Resize the image
new_width = 300
new_height = 200
resized_image = image.resize((new_width, new_height))

# Save the resized image
resized_image.save("resized_sp.jpg")

# Display the resized image using st.image
st.image("resized_sp.jpg", use_column_width=True)

st.title('Understanding the S&P 500')

st.markdown("The S&P 500, often referred to simply as the 'S&P,' is a renowned stock market index in the United States. It is widely regarded as a key indicator of the performance of the U.S. stock market and the broader economy.")
st.markdown("This index includes 500 of the largest publicly traded companies in the United States, representing various sectors and industries. As such, the S&P 500 serves as a valuable benchmark for investors and traders, offering insights into market trends and economic health.")

st.title("Who Is This App For and What Does It Do?")

st.markdown("This app provides tools and visualizations to help you analyze the stock price data of companies within the S&P 500. Whether you're a seasoned investor or a beginner looking to understand the market, you can use these interactive charts to make more informed trading decisions.")
st.markdown("Explore the available options in the sidebar to get started with your analysis.")

st.markdown("""
### How to Use This App

#### 1. Explore S&P 500 Companies by Sector

   - The S&P 500 comprises 500 companies, each of which can be grouped into sectors. To get started, use the sidebar's "Select Sector(s)" option to choose a sector of interest.

#### 2. Download Your Customized Dataset

   - After filtering companies by sector, you have the option to download your customized dataset for further analysis.

#### 3. Visualize Sector Distribution

   - Gain insights into sector representation by selecting a chart type from the sidebar. This chart will display the percentage of sectors within the S&P 500.

#### 4. Real-Time Stock Data

   - Utilizing Yahoo Finance (yFinance), the app provides access to real-time stock data. In the "Stock Visualization Options (Closing Price)" section of the sidebar, specify the time period and the name of the company. This will give you up-to-date information about the stock's performance during that period.

#### 5. Informed Trading Decisions

   - To assist with informed trading decisions, the app offers various analysis options:
      - 'Time Series Price Plot'
      - 'Candlestick Chart'
      - 'Correlation Heatmap'
      - 'Rolling Average'
      - 'Trading Volume Analysis'
      - 'Trading Volume Analysis (with closing price)'

   - Once again, select the desired time period, company, and analysis type to generate a plot. Each plot is accompanied by details on how to interpret it and draw insights for your trading decisions.

""")


st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Select Sectors', sorted_sector_unique, sorted_sector_unique)

# Filtering data based on selected sectors
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sectors')
st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data as CSV
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)


# Create a bar plot of sector distribution
st.sidebar.subheader('Sector Distribution')
sector_counts = df_selected_sector['GICS Sector'].value_counts().reset_index()
sector_counts.columns = ['Sector', 'Count']

chart_type = st.sidebar.selectbox("Select Chart Type", [ "Pie Chart","Bar Chart","Donut Chart"])

# Create the selected chart
if chart_type == "Bar Chart":
    st.subheader('Bar Chart - Sector Distribution')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Count', y='Sector', data=sector_counts, palette='viridis')
    plt.xlabel('Number of Companies')
    plt.ylabel('Sector')
    plt.title('S&P 500 Sector Distribution')
    st.pyplot(plt)

elif chart_type == "Pie Chart":
    st.subheader('Pie Chart - Sector Distribution')
    plt.figure(figsize=(8, 8))
    sns.set_palette('viridis')
    plt.pie(sector_counts['Count'], labels=sector_counts['Sector'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('S&P 500 Sector Distribution')
    st.pyplot(plt)

elif chart_type == "Donut Chart":
    # Create a horizontal bar plot for sector distribution
    plt.figure(figsize=(8, 8))
    sns.set_palette('viridis')
    plt.pie(sector_counts['Count'], labels=sector_counts['Sector'], autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(circle)
    plt.axis('equal')
    plt.title('S&P 500 Sector Distribution')
    st.pyplot(plt)


# Stock data retrieval and visualization
st.sidebar.subheader('Stock Visualization Options (Closing price)')
start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-12-31'))

selected_symbol = st.sidebar.selectbox('Select a Company', list(df_selected_sector['Symbol']))
company_data = yf.download(selected_symbol, start=start_date, end=end_date)

st.header('Stock Closing Price for ' + selected_symbol)
st.write(f'Data for {selected_symbol} from {start_date} to {end_date}')
st.line_chart(company_data['Close'])

#######################



# Sidebar for user options
st.sidebar.subheader('User Options for Informed Decision-Making')
start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2023-01-01'), key='start_date')
end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-12-31'), key='end_date')
selected_symbol = st.sidebar.selectbox('Select a Company', list(df_selected_sector['Symbol']), key='company_select')

# Download stock data
company_data = yf.download(selected_symbol, start=start_date, end=end_date)

st.header('Stock Data Visualization')

# Prompt the user to select the type of plot
plot_option = st.sidebar.selectbox('Select a Plot Type', [
    'Time Series Price Plot',
    'Candlestick Chart',
    'Correlation Heatmap',
    'Rolling Average',
    'Trading Volume Analysis',
    'Trading Volume Analysis (with closing price)'
])

if plot_option == 'Time Series Price Plot':
    st.header('Time Series Price Plot')
    st.write(f'Data for {selected_symbol} from {start_date} to {end_date}')
    st.line_chart(company_data['Close'])

elif plot_option == 'Candlestick Chart':
    st.header('Candlestick Chart')
    # Display the explanation using st.markdown
    fig = go.Figure(data=[go.Candlestick(x=company_data.index,
                    open=company_data['Open'],
                    high=company_data['High'],
                    low=company_data['Low'],
                    close=company_data['Close'])])
    st.plotly_chart(fig)
    st.markdown(f'##### Candle chart for {selected_symbol}')

    candlestick_chart_guide = """
    #### Guide to Making Informed Investment Decisions with Candlestick Charts

    Candlestick charts are powerful tools for investors and traders to gain insights into the price movements of assets, such as stocks, commodities, or currencies. These charts offer a visual representation of price data over a specific time period and provide valuable information for making informed investment decisions. In this guide, we will explore how to interpret and use candlestick charts effectively.

    **Understanding the Basics:**

    - **Candlestick Structure:** Each candlestick consists of a "body" and "wicks" (also known as "shadows").
    - **Body:** The rectangular part of the candlestick represents the opening and closing prices of the asset for the given time period. The color of the body indicates whether the price increased or decreased during that period.
        - If the closing price is higher than the opening price, the body is typically filled (colored) or hollow (white) and is often green or another color to indicate a "bullish" or positive day.
        - If the closing price is lower than the opening price, the body is filled or hollow, often red or another color to indicate a "bearish" or negative day.
    - **Wicks/Shadows:** The lines extending above and below the body are called wicks (or shadows).
        - The upper wick represents the highest price during the time period.
        - The lower wick represents the lowest price during the time period.

    **Using Candlestick Charts for Investment:**

    1. **Trend Analysis:** Candlestick charts are powerful tools for identifying trends in asset prices. When the closing price is consistently above the opening price (bullish), it suggests an uptrend. Conversely, when the closing price is consistently below the opening price (bearish), it indicates a downtrend.

    2. **Volatility Assessment:** The distance between the closing price and the body of the candlestick can provide insights into the asset's volatility. A larger gap suggests higher volatility, while a narrower gap implies lower volatility.

    3. **Support and Resistance Levels:** Candlestick patterns can help you identify potential support and resistance levels. Look for instances where the closing price bounces off the moving average as a potential indicator of support and resistance.

    4. **Entry and Exit Points:** Traders often use candlestick patterns to identify entry and exit points for buying or selling assets. For example, a common strategy is to buy when the closing price crosses above the long-term moving average (golden cross) and sell when it crosses below (death cross).

    5. **Candlestick Patterns:** Explore common candlestick patterns like doji, hammer, shooting star, and engulfing patterns to gain insights into potential price reversals or continuations.

    6. **Interpreting Long and Short-term Trends:** The choice of time frames for your candlestick chart can provide insights into both long-term and short-term trends. Longer periods provide a smoother line and are suitable for identifying long-term trends, while shorter periods capture short-term fluctuations.

    7. **Creating Strategies:** Traders often use different combinations of short-term and long-term moving averages to create strategies. For example, combining a short-term and long-term moving average can signal entry and exit points.

    Remember that candlestick charts are just one of many tools available for making investment decisions. It's essential to consider other factors such as fundamental analysis, news events, and risk management strategies. No single indicator can predict future performance with certainty, so always conduct thorough research and risk analysis before making investment decisions.
    """
    st.markdown(candlestick_chart_guide)


elif plot_option == 'Trading Volume Analysis':
# Create a Seaborn scatterplot
    st.header('Trading Volume Analysis')

    st.write(f'Data for {selected_symbol} from {start_date} to {end_date}')
    st.line_chart(company_data['Volume'])

    st.markdown("""
    ### Making Informed Investment Decisions with Trading Volume Analysis

    Welcome to our "Trading Volume Analysis" section! This analysis provides valuable insights for investors looking to understand how trading volume can impact our investment decisions. Below, we'll explore the key takeaways:

    #### 1. Understanding Trading Volume

    - **Data Range:** The chart displays the trading volume for our selected stock (selected_symbol) within the specified date range (from start_date to end_date).

    - **What is Trading Volume:** Trading volume represents the total number of shares or contracts traded during a specific time period, such as a day. It's an important indicator of market activity and can influence price movements.

    #### 2. Interpreting the Chart

    - **Volume Trends:** We can observe the volume trends to gauge the level of interest in the stock. Higher trading volume typically indicates increased market activity and interest in the stock.

    - **Price Impact:** Changes in trading volume can often precede price movements. A surge in volume may indicate a potential price change in the near future. Pay attention to spikes in volume for potential opportunities or risks.

    - **Divergence:** We can analyze the relationship between trading volume and price movements. Are there instances where volume surges or decreases while the price remains relatively stable or experiences a significant change? These divergences can offer insights into market sentiment.

    - **Confirmation:** Volume can be used to confirm price trends. For example, rising prices accompanied by increasing volume can provide validation for an upward trend.

    #### 3. Investment Implications

    - **Trading Strategies:** We, as investors, often use volume analysis to inform our trading strategies. For example, some of us look for "breakout" opportunities when volume spikes accompany price increases, while others consider "distribution" patterns when volume surges alongside price declines.

    - **Risk Management:** Volume analysis can help in managing risk. Unexpected high volume during a price decline might signal a potential trend reversal, allowing us to make informed decisions to limit losses.

    - **Long-term vs. Short-term:** We consider whether volume trends are short-term fluctuations or indicate longer-term shifts in market dynamics.

    #### 4. Combined Analysis

    To make well-informed investment decisions, we consider combining trading volume analysis with other technical and fundamental indicators. No single factor should be the sole basis for our investment strategy.

    """)


elif plot_option == 'Trading Volume Analysis (with closing price)':
    st.header('Trading Volume Analysis (with closing price)')

# Convert the selected start_date and end_date to datetime objects
   # Convert the selected start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the data for the selected date range
    filtered_data = company_data[(company_data.index >= pd.Timestamp(start_date)) & (company_data.index <= pd.Timestamp(end_date))]

    # Reset the index of the filtered data to ensure only the selected date range is displayed
    filtered_data = filtered_data.reset_index()

    # Create a Seaborn scatterplot with the closing price as a hue
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=filtered_data, x='Date', y='Volume', hue='Close', palette='coolwarm')

    # Customize the plot
    plt.xlabel('Date')
    plt.ylabel('Trading Volume')
    plt.title('Scatterplot of Trading Volume Over Time')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set a custom x-axis range to display only the selected date range
    plt.xlim(start_date, end_date)

    # # Display the plot by passing the figure to st.pyplot()
    # fig, ax = plt.subplots()
    # ax = sns.scatterplot(data=filtered_data, x='Date', y='Volume', hue='Close', palette='coolwarm')
    # plt.xticks(rotation=45)
    st.pyplot(fig)
    st.markdown("""
    ### Analyzing Trading Volume and Closing Price Together

    In this analysis, we're exploring the combined impact of trading volume and the closing price of our selected stock. Here's what we can learn from this visual representation:


    #### 1. Understanding the Plot

    - **Volume and Closing Price:** In this scatterplot, each point represents a day in the selected date range. The x-axis shows the date, the y-axis displays the trading volume, and the color (hue) corresponds to the closing price. 

    - **Volume Trends:** The height of the points (y-axis) indicates the trading volume for each day. A higher point suggests increased trading activity, while a lower point means fewer shares were traded.

    - **Closing Price Variation:** The color of the points (hue) represents the closing price of the stock on that day. Warmer colors (e.g., red) may indicate higher closing prices, while cooler colors (e.g., blue) may signify lower closing prices.

    - **Patterns and Relationships:** By examining the arrangement of points, we can identify potential patterns and relationships between trading volume and closing price.

    #### 2. Investment Implications

    - **Price and Volume Relationship:** The relationship between the height (volume) and color (closing price) of the points can offer insights into potential price movements. For instance, we may look for patterns where increased volume aligns with higher closing prices or vice versa.

    - **Identifying Anomalies:** Sudden spikes or drops in volume can be linked to significant price changes. We use this information to identify potential market anomalies or trading opportunities.

    - **Confirmation and Divergence:** By comparing volume and closing price movements, we assess if they confirm or diverge from one another. Consistent volume-price alignment can confirm trends, while divergences may suggest reversals.

    #### 3. Long-term vs. Short-term

    - **Time Sensitivity:** Keep in mind that the time period you've selected (start_date to end_date) impacts your analysis. The insights drawn can differ based on whether we focus on short-term or long-term trends.

    #### 4. Combining Insights

    - **Holistic Approach:** Remember that trading volume and closing price are just two aspects of your investment strategy. To make well-informed decisions, we combine these insights with other indicators and conduct comprehensive research.

    By exploring the interaction between trading volume and closing price, we aim to make better-informed investment decisions and discover opportunities in the market.

    """)


########****************************

elif plot_option == 'Correlation Heatmap':
    st.header('Correlation Heatmap')
    correlation_matrix = company_data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5,ax=ax)
    st.pyplot(fig)
    insights = """
    #### Guide to Make Informed Investment Decisions with Correlation Heatmap

    - **Price Movements:** We can observe that the opening, high, low, and closing prices are closely related to each other. Strong positive correlations between these columns indicate that they tend to move together, demonstrating a strong linear relationship in daily price movements.

    - **Price Range:** We noticed a strong positive correlation between the 'High' and 'Low' prices, which suggests that the stock's intraday price range tends to be relatively stable.

    - **Adj Close vs. Close:** The correlation between 'Adj Close' and 'Close' is extremely high, as expected. This ensures data accuracy and highlights the consistency between the two columns.

    - **Volume and Price:** We found a significant positive correlation between the 'Volume' and price columns, indicating that higher trading volumes tend to coincide with price changes.

    - **Liquidity:** The correlation between trading volume and price range ('High' - 'Low') suggests that higher trading volumes are associated with increased price volatility. This insight can be valuable for assessing liquidity and potential price fluctuations.

    - **Potential Trading Strategies:** As traders, we can use these correlations to develop strategies. For example, a strong negative correlation between 'Open' and 'Close' may lead us to consider a gap-trading strategy.

    - **Risk Assessment:** The strong positive correlation between 'Open' and 'High' indicates that the stock tends to open near its daily high. This can be a useful insight for assessing intraday price volatility and managing risk.

    - **Sector Analysis:** To understand how this stock relates to broader industry trends, we can compare its correlation matrix with other stocks in the same sector. High positive correlations with sector peers may indicate that the stock closely follows sector movements.

    - **Long-term vs. Short-term Relationships:** By examining correlations across different time frames, we can assess whether the relationships between these variables change over time. Consistent correlation patterns can provide insights into the stock's long-term behavior.

    Remember that correlation measures linear relationships and doesn't imply causation. These insights can guide our further analysis and decision-making but should be considered alongside other forms of research and analysis.
    """

    st.markdown(insights)


elif plot_option == 'Rolling Average':
    st.header('Rolling Average')
    rolling_period = st.sidebar.slider('Select Rolling Period', min_value=1, max_value=100, value=20)
    company_data['Rolling Average'] = company_data['Close'].rolling(rolling_period).mean()
    st.line_chart(company_data[['Close', 'Rolling Average']])

    rolling_average_insights = """
    #### Making Informed Decisions with Rolling Average Analysis

    The graph we've mentioned is a **Rolling Average** plot that displays both the daily closing prices and the rolling average of a selected stock or asset over a specified period. From this graph, we can draw several insights:

    - **Trend Analysis:** By comparing the rolling average line to the actual closing prices, we can identify trends in the stock's performance. When the rolling average line is above the closing price line, it suggests an uptrend. Conversely, when the rolling average is below, it indicates a downtrend.

    - **Volatility Assessment:** The distance between the rolling average line and the closing price line can provide insights into the stock's volatility. A larger gap suggests higher volatility, while a narrower gap implies lower volatility.

    - **Support and Resistance Levels:** We can identify potential support and resistance levels based on how the closing price interacts with the rolling average. If the closing price consistently bounces off the rolling average, it may indicate support and resistance levels.

    - **Entry and Exit Points:** Traders often use rolling averages to identify potential entry and exit points for buying or selling stocks. For example, a common strategy is to buy when the closing price crosses above the rolling average and sell when it crosses below.

    - **Signal for Momentum and Reversals:** Crossovers between the closing price and the rolling average can be used to identify potential changes in momentum or trend reversals. For example, a "golden cross" occurs when the closing price crosses above the long-term rolling average, signaling a potential bullish trend.

    - **Rolling Average Period:** The period we choose for the rolling average (specified by the slider) affects the sensitivity of the line. Longer periods provide a smoother line and are suitable for identifying long-term trends, while shorter periods capture short-term fluctuations.

    - **Long-term vs. Short-term Trends:** If we observe that the rolling average is moving upwards, it suggests a longer-term bullish trend. If the rolling average is moving downwards, it suggests a longer-term bearish trend.

    - **Moving Averages Strategies:** Traders often use different combinations of short-term and long-term rolling averages to create strategies. For example, the crossover of a short-term average above a long-term average can signal entry and exit points.

    These insights can help us make informed decisions about a particular stock or asset, whether we're investors looking for long-term trends or traders seeking short-term opportunities. 
    """
    st.markdown(rolling_average_insights)


st.markdown("""


""")

# Show a table with detailed stock data
st.subheader('Stock Data')
st.write(company_data)

# sp500['Daily_Return'] = sp500['Close'].pct_change()
# plt.figure(figsize=(10, 6))
# sns.distplot(sp500['Daily_Return'].dropna(), kde=False, bins=30, color='blue')
# plt.title('S&P 500 Daily Returns Distribution')
# plt.xlabel('Daily Returns')
# plt.ylabel('Frequency')
# plt.show()

# Provide insights and explanations
st.markdown("""
**Insights:**
- This chart displays the closing price of the selected company's stock.
- You can select a specific date range using the sidebar options.
- Analyze the stock's performance during the selected period.
""")

st.markdown("""

**References**
            
* **Python libraries:** base64, pandas, streamlit, numpy, altair, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")
