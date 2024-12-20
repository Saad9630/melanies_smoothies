# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("My Parents New Healthy Breakfast Dinner")
st.write("Choose the fruits you want in your custom smoothie!")


name_on_order = st.text_input("Breakfast menu:")
st.write("The name on smoothe will be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "choose upto 5 ingredients:",
    my_dataframe ,
    max_selections = 5
    
)

my_insert_stmt = None  # Define it outside the block to avoid the unbound error

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('""" + ingredients_string.strip() + """', '"""+name_on_order+ """')
    """
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")


