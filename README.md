# Scientific-Programming---Project

My project is creating a local app where you can get movie recommendations based on the genre and characteristics of a selected movie title. I am using the CSV file called IMDB-Movie-Data, a dataset from which I get the movies for the recommendations. I found this data set in a GitHub repository of which I leave the link below so anyone who wants to go check it out can do so, it is quite nice because they have tips and resources to learn about Data Science. The recommendations are going to be made by Content-based filtering, so based on the user's input, the system finds the movies that are more similar to it and recommends others that the user might like too.

Link to the dataset: https://github.com/LearnDataSci/articles/blob/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv

This dataset has 12 columns and 1000 rows.

For the app interface, I am using Streamlit which turns data scripts into shareable web apps in minutes. All in pure Python, and no front‑end experience is required.

Lastly is important to mention that to run the code first you need to go to the project folder (where the .venv directory lives) and run this command to activate it (mac and linux, for windows is different): .venv/bin/activate And afterwards to run it just write this: streamlit run appmovie.py

If you have any questions or doubts let me know.