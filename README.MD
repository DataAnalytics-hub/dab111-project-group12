Stock Market Data Set
---------------------

The dataset we choose is the stocks information of 4 tech companies namely, Apple, Microsoft, Amazon and Nvdia. We collected stocks values from Jan 1, 2024 to Dec 10, 2024 with 5min timespans.

### Data Source

[**Polygon.io**](https://polygon.io/) is a data platform that provides high-quality financial market data through APIs. It offers access to real-time and historical data for stocks, options, forex, and cryptocurrencies, catering to developers and businesses in the financial sector. The platform is known for its ease of integration, with RESTful APIs that are well-documented and simple to use. Polygon.io also provides websocket support for streaming real-time market data, enabling users to build trading algorithms, analytical tools, and financial dashboards effectively.

The service stands out for its fast response times and high reliability, making it a popular choice for both individual developers and enterprise clients. With flexible pricing plans, including a free tier for basic use, it appeals to a wide range of users. Polygon.io supports global markets, making it suitable for projects with international scope. Additionally, the platform offers resources like community forums and example projects, making it beginner-friendly while still robust enough for advanced applications.

* Fetched Columns -
    - timestamp: The Unix Msec timestamp for the start of the timespan window.
    - open: The open price for the symbol in the given time period.
    - close: The close price for the symbol in the given time period.
    - high: The highest price for the symbol in the given time period.
    - low: The lowest price for the symbol in the given time period.

### Instructions to get your own API Key,

*   Sign Up for a free account at [Polygon.io](https://polygon.io/)
*   Verify your email and login to your account
*   Click on `Dashboard` on the right-side of navigation bar
*   Click on `Keys` on the left-panel
*   Use the default key or create a new key as required

### Instructions to use the API key to update this dataset,

*   Create `credentials.py` file in project root folder
*   Create `polygon_api_key` variable in the file with the key as its value
*   Save and run `datacollection.py` script to rebuild the dataset
    *   This script will take more than 4min to complete due to the polygon's restriction of only 5 API calls per minute
    *   Feel free to explore this script and modify any parameters as you wish

Team Information
----------------

### Group 12

Members,

*   0858474 - Kishore Arra
*   0873467 - Deepesh Dixit
*   0876264 - Geetha Siva Srinivas Gollapalli
*   0873782 - Rajesh Thota
*   0872873 - Yogeshwar Moruboyina