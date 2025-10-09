# Exploratory Data Analysis & ETL Prototyping

This directory contains the Jupyter Notebooks used for the initial exploratory data analysis (EDA) and for prototyping the ETL logic before it was refactored into production scripts.

## The Role of the Notebook in this Project

While the final, automated pipeline is run using `.py` scripts orchestrated by Airflow, the initial development and validation were performed in a notebook environment. This approach is crucial for several reasons:

1.  **Interactivity:** Notebooks allow for executing code in small, isolated cells. This is essential for inspecting intermediate dataframes, debugging transformations step-by-step, and ensuring the logic at each stage (Bronze, Silver, Gold) is correct.
2.  **Rapid Prototyping:** It provides a fast and efficient way to test different approaches to data cleaning, enrichment, and aggregation before committing to a final script.
3.  **Visualization:** The notebook environment makes it easy to generate inline plots and tables to visually inspect the data and validate the results of the final Gold layers.

In essence, the notebook served as the "laboratory" where the ETL recipe was created and perfected.

---
## Key Insights from the Exploratory Phase

The initial analysis in the notebook revealed several key characteristics of the data that directly influenced the design of the ETL pipeline.

* **Data Quality Issues Identified:** The raw data required significant cleaning, which was addressed in the Silver layer. Key issues included:
    * **Null CustomerIDs:** A considerable number of transactions were missing a `CustomerID` and had to be filtered out for customer-centric analysis.
    * **Negative Quantities:** These entries, corresponding to returns, were removed to ensure sales calculations were accurate.
    * **Inconsistent Naming:** The source data contained table and column names with spaces and special characters (e.g., `online retail (3)`, `Customer Name`). This required specific handling during the ingestion and transformation phases to conform to data engineering best practices.

* **Business Insights Discovered:**
    * **Sales Concentration:** A vast majority of sales originate from the **United Kingdom**, indicating a strong geographical concentration.
    * **Top Customer Value:** The analysis confirmed a power-law distribution, where a small percentage of top customers are responsible for a disproportionately large share of total revenue.
    * **Sales Seasonality:** Plotting sales over time revealed clear seasonal trends, with a significant increase in transaction volume in the final months of the year, likely due to holiday shopping.

---

## Transition to Production

Once the logic for the Bronze, Silver, and Gold layers was validated in the `initial_development.ipynb` notebook, the code was refactored into modular, production-ready Python scripts (`bronze.py`, `silver.py`, `gold.py`). This separation of exploration (notebooks) from production (scripts) is a critical best practice that ensures the final pipeline is robust, efficient, and easy to maintain.
