# Python file for Project 2 queries and data visualizations
# File written by Kim Benson

# import statements

import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings

# turn off warnings
warnings.filterwarnings('ignore')

# functions for making graphs
def plot_bar_graph(data, x_axis, y_axis, x_label, y_label, title):
    """
    Function to plot a bar graph
    Parameters:
    data (dtype-> DataFrame)
    column on x-axis (dtype -> string)
    column on y-axis (dtype -> string)
    x-axis label (dtype -> string)
    y-axis label (dtype -> string)
    title for the plot (dtype -> string)
    """
    
    plt.figure(figsize=(10, 6))

    colors = cm.viridis(np.linspace(0, 1, len(data[x_axis])))

    plt.bar(data[x_axis], data[y_axis], color=colors)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_scatter_plot(data, x_axis, y_axis, x_label, y_label, title):
    """
    Function to plot a scatter plot graph
    Parameters:
    data (dtype-> DataFrame)
    column on x-axis (dtype -> string)
    column on y-axis (dtype -> string)
    x-axis label (dtype -> string)
    y-axis label (dtype -> string)
    title for the plot (dtype -> string)
    """

    plt.figure(figsize=(10,6))

    colors = cm.viridis(np.linspace(0, 1, len(data[x_axis])))

    plt.scatter(data[x_axis], data[y_axis], color=colors)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=15)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_pie_chart(data, x_axis, y_axis, legend_title, title):
    """
    Function to plot a pie chart
    Parameters:
    data (dtype-> DataFrame)
    column on x-axis (dtype -> string)
    column on y-axis (dtype -> string)
    title for the legend (dtype -> string)
    title for the plot (dtype -> string)
    """
    
    plt.figure(figsize=(10,6))

    colors= cm.viridis(np.linspace(0, 1, len(data[x_axis])))

    plt.pie(data[y_axis], labels=data[y_axis], colors=colors)
    plt.legend(data[x_axis], title=legend_title)
    
    plt.title(title)
    plt.xticks(rotation=15)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

# Establish SQL connection
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "KiCaB432005!",
    database = "sakila"
    )

if conn.is_connected():
    print("Established")

# Data Queries and Visualizations

# 1 - Overall customer rental counts.

overall_rental_query = "SELECT customer_id, COUNT(customer_id) AS rental_count FROM rental GROUP BY customer_id ORDER BY rental_count DESC;"

overall_rental_data = pd.read_sql(overall_rental_query, conn)

print(overall_rental_data)

plot_scatter_plot(overall_rental_data, "customer_id", "rental_count", "Customer ID", "Rental Count", "Overall customer rental counts")

# 2- Aggregated rental counts for each film category.

aggregated_rental_query = "SELECT c.name AS category_name, COUNT(r.rental_id) AS rental_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN film f ON fc.film_id = f.film_id JOIN inventory i ON f.film_id = i.film_id JOIN rental r ON i.inventory_id = r.inventory_id GROUP BY c.category_id ORDER BY rental_count DESC;"

aggregated_rental_data = pd.read_sql(aggregated_rental_query, conn)

print(aggregated_rental_data)

plot_bar_graph(aggregated_rental_data, "category_name", "rental_count", "Film Category", "Rental Count", "Aggregated rental counts for each film category.")

# 3 - Total rental counts per actor across the entire dataset.

# get top 20
total_rentals_top_20_actor_query = "SELECT a.actor_id, CONCAT(a.first_name, \" \", a.last_name) AS actor_name, COUNT(fa.film_id) AS total_films FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id GROUP BY actor_id ORDER BY total_films DESC LIMIT 20"

total_rentals_top_20_actor_data = pd.read_sql(total_rentals_top_20_actor_query, conn)

print(total_rentals_top_20_actor_data)

plot_bar_graph(total_rentals_top_20_actor_data, "actor_name", "total_films", "Actor Name", "Total Films Rented", "Total rental counts per actor for top 20 actors")

# get all actors
total_rentals_per_actor_query = "SELECT a.actor_id,COUNT(fa.film_id) AS total_films FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id GROUP BY actor_id ORDER BY total_films DESC"

total_rentals_per_actor_data = pd.read_sql(total_rentals_per_actor_query, conn)

print(total_rentals_per_actor_data)

plot_scatter_plot(total_rentals_per_actor_data, "actor_id", "total_films", "Actor ID", "Total Films Rented", "Total rental counts per actor across the entire dataset")

# 4 - Calculating total revenue per store.
revenue_per_store_query = "SELECT  s.store_id, s.address_id, SUM(p.amount) AS total_amount FROM store s JOIN inventory i ON s.store_id = i.store_id JOIN rental r ON i.inventory_id = r.inventory_id JOIN payment p ON r.rental_id = p.rental_id GROUP BY s.store_id;"

revenue_per_store_data = pd.read_sql(revenue_per_store_query, conn)

print(revenue_per_store_data)

plot_pie_chart(revenue_per_store_data, "store_id", "total_amount", "Store ID", "Total revenue per store ($)")