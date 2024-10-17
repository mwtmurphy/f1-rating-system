import streamlit as st


# page config
st.set_page_config(page_title="F1 rating system | Home")


# streamlit page 
st.title("Is your favourite driver/constructor as good as you think they are?")

st.markdown("""
    A tale as old as time: X driver is the GOAT, Y driver only did well because constructor Z built 
    a rocket ship, etc.. Cue discourse with a 5 to 50% chance of developing into an argument.

    Well, this app joins said non-argument, but does it using data so you can't blame the creator.

    Modifying the rating system made popular in chess, this app uses a freshly homebaked rating 
    system separating the influence of the driver and constructor and allows us to understand how 
    drivers and constructors compare across the past 70+ years of F1. 
            
    Explore:
    
    - [The greatest F1 driver of all time (GOAT)](/who-is-the-goat) based on their career rating
    - The current ratings for [drivers](/current-drivers-ratings) and 
      [constructors](current-constructors-ratings) in 2024 and who's improved the most
    - How your favourite [drivers](/compare-driver-ratings) and 
      [constructors](/compare-constructor-ratings) compare to each other over the past 70+ years
""")
