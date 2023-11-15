import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

   
    #make sure the columns contains the right information
    #Columns 1.Company_ID	2.company_type	3.founded	4.region	5.county	6.Sum_operatingcosts	7.Material_assetsr	8.accounts_receivable	9.Cash_and_bank	10.Sum_assets	11.Long_term_liabilities	12.Accounts_payable	13.Current_liabilities 14.Shareholders'_equity	15.Corporation_tax	16.Sum_financial_assets	17.Finished_goods	18.Employees	19.Revenue	20.Profit	21.Year


    # Read the CSV file and making a useable array
    file_path = 'data/Data.csv' #Change this to your own file path
    data_frame = pd.read_csv(file_path, header=None, delimiter=';')
    data = data_frame.to_numpy()
    
    #Variables for each index for eas of use
    company_id_column_index = 0
    Long_term_liabilities_column_index = 10
    Accounts_payable_column_index = 11
    Current_liabilities_column_index = 12
    Shareholders_equity_index = 13
    Employees_column_index = 17
    revenue_column_index = 18 
    profit_column_index = 19
    year_column_index = 20
    
    #Array of the years the data contains 
    unique_years = np.unique(data[:, year_column_index]) 
    
    #Calculating the total revenue, profit and profit margin for each year  
    total_revenue_by_year = {year: np.sum(data[data[:, year_column_index] == year, revenue_column_index]) for year in unique_years}
    
    total_profit_by_year = {year: np.sum(data[data[:, year_column_index] == year, profit_column_index]) for year in unique_years}
    
    profit_margin_by_year = {
        year: (total_profit_by_year[year] / total_revenue_by_year[year]) * 100
        if total_revenue_by_year[year] != 0  # Avoid division by zero
        else 0
        for year in unique_years
    }
    
    #Calculating total ROE for each year
    total_shareholders_equity_by_year = {year: np.sum(data[data[:, year_column_index] == year, Shareholders_equity_index]) for year in unique_years}
    total_ROE_by_year = {}
    for year in unique_years:
        total_ROE_by_year[year] = (total_profit_by_year[year] / total_shareholders_equity_by_year[year]) * 100
    
    #Calculating HHI Herfindahl–Hirschman Index for the market each year  
    hhi_by_year = {
        year: np.sum((data[data[:, year_column_index] == year, revenue_column_index] / total_revenue_by_year[year] * 100) ** 2)
        for year in unique_years
    }   

    # Calculating Revenue per Employee for each year
    revenue_per_employee_by_year = {
        year: total_revenue / np.sum(data[data[:, year_column_index] == year, Employees_column_index])  
        for year, total_revenue in total_revenue_by_year.items()
    }  
    
    # Calculating Debt-to-Equity Ratio for each year
    total_liabilities_by_year = {
        year: np.sum(data[data[:, year_column_index] == year, Long_term_liabilities_column_index]) + np.sum(data[data[:, year_column_index] == year, Accounts_payable_column_index]) + np.sum(data[data[:, year_column_index] == year, Current_liabilities_column_index])
        for year in unique_years
    }
    
    debt_equity_ratio_by_year = {
        year: total_liabilities_by_year[year] / total_shareholders_equity_by_year[year]
        if total_shareholders_equity_by_year[year] != 0  
        else 0
        for year in unique_years
    }
    
    unique_years = unique_years.astype(int)
    
    # Line graph for Total Revenue
    plt.plot(unique_years, list(total_revenue_by_year.values()), label='Total Revenue', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Total Revenue')
    plt.grid(True)
    plt.title('Line Graph of Total Revenue over Years')
    plt.xticks(unique_years)
    plt.legend()
    plt.show()
    
    # Line graph for Total Profit
    plt.plot(unique_years, list(total_profit_by_year.values()), label='Total Profit', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Total Profit')
    plt.grid(True)
    plt.title('Line Graph of Total Profit over Years')
    plt.xticks(unique_years)
    plt.legend()
    plt.show()
    
    # Line graph for total Profit Margin
    plt.plot(unique_years, list(profit_margin_by_year.values()), label='Profit Margin', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Profit Margin (%)')
    plt.grid(True)
    plt.title('Line Graph of Profit Margin over Years')
    plt.xticks(unique_years)
    plt.legend()
    plt.show()
    
    #Printing key values for the market
    
    print("\nTotal Revenue by Year")
    print(total_revenue_by_year)
    
    print("\nTotal Profit by Year")
    print(total_profit_by_year)
    
    print("\nProfit Margin by Year (in %)")
    print(profit_margin_by_year)
    
    
    print("\nTotal ROE by Year")
    print(total_ROE_by_year)
    
    print("\nHerfindahl–Hirschman Index (HHI) for the Market by Year:")
    print(hhi_by_year)
    print("0-1500 is an unconsentraded market, 1500-2500 is moderately concentrated and 2500+ is higly consentrated")
    
    print("\nRevenue per Employee by Year:")
    print(revenue_per_employee_by_year)
    
    print("\nDebt-to-Equity Ratio by Year:")
    print(debt_equity_ratio_by_year)
          
    
    while True:
        # User chooses how many of the biggest companies to focus on
        input_value = input("\nEnter the number of top companies to focus on (press 'q' to exit): ")
    
        # Check if the user wants to exit
        if input_value.lower() == 'q':
            print("Exiting the program.")
            break
    
        # Try to convert the input to an integer
        try:
            num_top_companies = int(input_value)
        except ValueError:
            print("Invalid input. Please enter a valid number or 'q' to exit.")
            continue   
        
        # Summing up the revenue for each unique Company ID for the top companies
        unique_company_ids = np.unique(data[:, company_id_column_index])
        company_revenue_dict = {
            company_id: {
                year: np.sum(data[(data[:, year_column_index] == year) & (data[:, company_id_column_index] == company_id),
                                 revenue_column_index])
                for year in unique_years
            }
            for company_id in unique_company_ids
        }
        
        # Sorting companies based on total revenue and getting the top companies
        top_companies = sorted(
            unique_company_ids,
            key=lambda company_id: np.sum(data[data[:, company_id_column_index] == company_id, revenue_column_index]),
            reverse=True
        )[:num_top_companies]
        
        # Extracting the Company IDs of the top companies
        top_company_ids = top_companies
        
        
        #Making a new array with only the top companies
        rows_to_include = [i for i, company_id in enumerate(data[:, company_id_column_index]) if company_id in top_company_ids]
        data_top_companies = data[rows_to_include, :]
        
        # Summarizing the revenue, profit and profitmargin of the top companies for each year
        top_total_revenue_by_year = {year: np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, revenue_column_index]) for year in unique_years}
        
        top_total_profit_by_year = {year: np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, profit_column_index]) for year in unique_years}
         
        top_profit_margin_by_year = {
            year: (top_total_profit_by_year[year] / top_total_revenue_by_year[year]) * 100
            if top_total_revenue_by_year[year] != 0  # Avoid division by zero
            else 0
            for year in unique_years
        }
        
        # Calculate the market share percentage for each year of the top companies
        market_share_percentage_by_year = {
            year: (top_total_revenue_by_year[year] / total_revenue_by_year[year]) * 100
            for year in unique_years
        } 
        
        #Calculate the ROE for top companies year over year
        top_total_shareholders_equity_by_year = {year: np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, Shareholders_equity_index]) for year in unique_years}
        top_total_ROE_by_year = {}
        for year in unique_years:
            top_total_ROE_by_year[year] = (top_total_profit_by_year[year] / top_total_shareholders_equity_by_year[year]) * 100
            
         # Calculating Revenue per Employee for each year
        top_revenue_per_employee_by_year = {
            year: top_total_revenue / np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, Employees_column_index])  
            for year, top_total_revenue in top_total_revenue_by_year.items()
        }
        
        # Calculating Debt-to-Equity Ratio for each year
        top_total_liabilities_by_year = {
            year: np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, Long_term_liabilities_column_index]) + np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, Accounts_payable_column_index]) + np.sum(data_top_companies[data_top_companies[:, year_column_index] == year, Current_liabilities_column_index])
            for year in unique_years
        }
        
        top_debt_equity_ratio_by_year = {
            year: top_total_liabilities_by_year[year] / top_total_shareholders_equity_by_year[year]
            if top_total_shareholders_equity_by_year[year] != 0  
            else 0
            for year in unique_years
        }
        
        print(f"\nTop {num_top_companies} Companies' Combined Revenue by Year:")
        print(top_total_revenue_by_year)
        
        print(f"\nTotal Profit of top {num_top_companies} companies by Year")
        print(top_total_profit_by_year)
    
        print(f"\nProfit Margin by Year (in %) for top {num_top_companies} companies")
        print(top_profit_margin_by_year)
        
        print(f"\nMarket Share of Top {num_top_companies} Companies by Year (in %):")
        print(market_share_percentage_by_year)
        
        print(f"\nTotal ROE for top {num_top_companies} companies by Year")
        print(top_total_ROE_by_year)
        
        print(f"\nRevenue per Employee by Year for top {num_top_companies} companies:")
        print(top_revenue_per_employee_by_year)
        
        print(f"\nDebt-to-Equity Ratio by Year for top {num_top_companies} companies:")
        print(top_debt_equity_ratio_by_year)
        
        # Line graph for top Total Revenue
        plt.plot(unique_years, list(top_total_revenue_by_year.values()), label='Total Revenue', marker='o')
        plt.xlabel('Year')
        plt.ylabel('Total Revenue')
        plt.grid(True)
        plt.title(f'Line Graph of top {num_top_companies} Companies Total Revenue over Years')
        plt.xticks(unique_years)
        plt.legend()
        plt.show()
        
        # Line graph for top Total Profit
        plt.plot(unique_years, list(top_total_profit_by_year.values()), label='Total Profit', marker='o')
        plt.xlabel('Year')
        plt.ylabel('Total Profit')
        plt.grid(True)
        plt.title(f'Line Graph of top {num_top_companies} Companies Total Profit over Years')
        plt.xticks(unique_years)
        plt.legend()
        plt.show()
        
        # Line graph for top Total Profit Margin
        plt.plot(unique_years, list(top_profit_margin_by_year.values()), label='Profit Margin', marker='o')
        plt.xlabel('Year')
        plt.ylabel('Profit Margin (%)')
        plt.grid(True)
        plt.title(f'Line Graph of top {num_top_companies} Companies Profit Margin over Years')
        plt.xticks(unique_years)
        plt.legend()
        plt.show()
        
        # Creating a scatter plot with revenue on the x-axis and profit on the y-axis
        plt.figure(figsize=(10, 6))
        
        for year in unique_years:
            # Filter data for the current year
            data_year = data_top_companies[data_top_companies[:, year_column_index] == year]
            
            # Extract revenue and profit for the current year
            revenue = data_year[:, revenue_column_index].astype(float)
            profit = data_year[:, profit_column_index].astype(float)
            
            # Choose a unique color for each year
            color = plt.cm.viridis(float(year - min(unique_years)) / float(max(unique_years) - min(unique_years)))
            
            # Scatter plot for the current year with a unique color
            plt.scatter(revenue, profit, label=str(year), color=color)
            
            # Fittig a polynomial regression line (1st degree) for the current year
            coeffs = np.polyfit(revenue, profit, 1)
            regression_line = np.polyval(coeffs, revenue)
            
            # Plot the regression line
            plt.plot(revenue, regression_line, linestyle='--', linewidth=2, color=color)
            
        plt.xlabel('Revenue')
        plt.ylabel('Profit')
        plt.grid(True)
        plt.title('Scatter Plot of Revenue vs. Profit')
        plt.legend(title='Year')
        plt.show()
        
        # Creating a line graph with revenue on the x-axis and top_revenue_per_employee on the y-axis
        plt.figure(figsize=(10, 6))
        
        for year in unique_years:
            # Filter data for the current year
            data_year = data_top_companies[data_top_companies[:, year_column_index] == year]
        
            # Loop through each company in the current year
            for company_id in np.unique(data_year[:, company_id_column_index]):
                # Extract revenue and revenue per employee for the current company
                company_data = data_year[data_year[:, company_id_column_index] == company_id]
                revenue = company_data[:, revenue_column_index].astype(float)
                revenue_per_employee = revenue / company_data[:, Employees_column_index].astype(float) if company_data[:, Employees_column_index] != 0 else 0
        
                # Choose a unique color for each year
                color = plt.cm.viridis(float(year - min(unique_years)) / float(max(unique_years) - min(unique_years)))
        
                # Scatter plot for the current year and company with a unique color
                plt.scatter(revenue, revenue_per_employee, label=f"{year} - Company {company_id}", color=color)
                   
    
        plt.xlabel('Revenue')
        plt.ylabel('Revenue per Employee')
        plt.grid(True)
        plt.title('Scatter Plot of Revenue per Employee vs. Revenue')
        handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(year), markerfacecolor=plt.cm.viridis(float(year - min(unique_years)) / float(max(unique_years) - min(unique_years)))) for year in unique_years]
        plt.legend(handles=handles, title='Year')
        plt.show()