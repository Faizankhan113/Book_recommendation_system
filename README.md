👋👋Hello this is the book recomendatation system.

This system follows a **Hybrid Recommendation Approach**.

# 1. Collaborative Filtering (User-Based)

1. Identifies users who have read the same or similar books  
2. Assigns a similarity score to users based on overlapping books  
3. Prioritizes users with higher similarity scores  

# 2. Content-Based Filtering (Author Boost)

1. Extracts authors of books read by the user  
2. Gives additional weight to books written by the same authors  
3. Improves recommendation relevance  

Built using **Python, Pandas, and Dash**


# main.py contains the final system with the website view by using dash.
# main.jpynb contains only the core logic of the recommendation system with step by step explanation.
# while the csv files contains the data on which the system is build.


# ⚙️ How the Recommendation Works:

1. The user selects books they have read  
2. The system assigns scores to these books  
3. Books by the same authors receive extra weight  
4. Users who read similar books are identified  
5. Top similar users are selected  
6. Books read by these users are aggregated  
7. Books are ranked by relevance score  
8. The **Top 5 books** are recommended  


> **Note:**  
> This system does **not** use machine learning models.  
> All recommendations are generated using **custom scoring logic** for clarity and efficiency.

