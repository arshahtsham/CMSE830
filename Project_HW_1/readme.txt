✍🏼 **Problem 11**: This problem is the most difficult: be sure to give yourself plenty of time to work on it.

If you get stuck, put your questions in the general channel on Slack so that other students can help and learn from you.

There are two goals of this problem:
1. develop your ability to manage new Python libraries on your computer,
2. begin the first steps of building a DS-based web app for your midterm project.

The reason this will be challenging is that:
* you have some choices to make that will be unique to you,
* your computer, its operating system and your library distributions are not necessarily like other students'.

Here are the steps  to follow:
1. If you don't have one already, put a text editor on your computer. There are many to choose from: [Sublime](https://www.sublimetext.com/), [VSCode](https://code.visualstudio.com/), and so on. There are many times when using a Jupyter notebook, as amazing as they are, won't work. If you haven't used any of these editors, I recommend getting a few so that you can compare them. The choice is often very personal, which is why I am giving you the opportunity to explore and choose the best one for you.
2. Be sure that you can work at the command line. How this works differs greatly from computer to computer. For example, on a Mac you always use the [Terminal](https://en.wikipedia.org/wiki/Terminal_(macOS)). As with the editors, there are many choices, [like this](https://iterm2.com/).  If you are a windows user, you definitely want to [read this](https://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/). Together, the editor and the command line will allow you to execute `.py` files, which can be really useful if you are using another computer (such as a cluster located somewhere else, such as MSU's HPCC facility).
3. Once those two steps are done, open the editor you chose and put this code in it, giving it any name you want, but ending with `.py`:
```
import streamlit as st
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_wine
import altair as alt
wine_data = load_wine()
labels = wine_data.feature_names
targets = wine_data.target
print(labels)
df_form = pd.DataFrame(wine_data.data, columns = labels)
df_form['targets'] = targets
st.write("""
# Italian Wine Dataset
How are malic acid and alcohol correlated in Italian wines?
""")
alt_handle = alt.Chart(df_form).mark_circle(size=60).encode(x='alcohol', y='malic_acid',
	color='hue', tooltip=['ash', 'magnesium',
	'proanthocyanins']).interactive()
st.altair_chart(alt_handle)
```
Note that you will likely have to install some libraries on your computer.
4. At the command line, run your file using `streamlit run name.py`, where `name` is whatever name you chose for your file in your editor. An interactive web app should appear in your browser. Don't worry about the details at this point, which we will cover later in the course: the goal for this HW is just to **get your computer setup properly** for deployable interactive DS apps.
5. In a markdown cell, put the answers to these questions:
* which editor(s) did you choose, and why?
* what did you decide to use for your command line? (e.g., are you on OSX and using the built-in `Terminal`?)
* did you have any problems installing the libraries, such as `streamlit` and `altair`?
* yes or no, did you get the interactive app working? if not, give details of your situation (i.e., your computer, what you tried, what you saw), so that we can fix the problems for next time.

Again, if you have issues, post your questions. Everyone has a different background in setting up their computer and every computer is different.

Once you have it working: congrats on your first, tiny data science app!
