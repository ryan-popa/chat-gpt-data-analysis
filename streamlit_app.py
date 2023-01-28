from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import os
from cache.cache import cache_string
import openai
import matplotlib.pyplot as plt
import seaborn
import sys
import numpy as np

api_key = os.environ.get("OPENAI_API_KEY")

def ask_chat_gpt(question):
    return cache_string(question, lambda: openai.ask_chat_gpt_question(question, api_key), -1)

def execute_script(code):
    ret = {}

    with st.expander("Show code", True):
        st.code(code)
    
    try:
        exec(code, None, ret)
    except Exception as ex:
        st.error(ex)
        
    return ret
       
def show_variables_for_debugging(ret): 
    pyplot_chart = None
    last_value = None
    for k, v in ret.items():
        st.write(v)
        if "pyplot" in str(v):
            st.write("found pyplot")
            pyplot_chart = v
        last_value = v
        
    if pyplot_chart:
        st.pyplot(pyplot_chart)
    else:
        st.write(last_value)
    
    k = st.selectbox("Variable", ret.keys())
    if k:
        st.write(ret[k])
        
    return ret
    
    

if not api_key:
    st.error("OPENAI_API_KEY environmnet variable set")
    
# TODO: replace with the ability to load dynamic datasets 
dataset_name = st.selectbox("Select dataset", ["titanic.csv", ""])
df = pd.read_csv(dataset_name)
st.write(df)

col = list(zip(df.columns, df.dtypes))
def format_column(tpl):
    return "{}: {}".format(tpl[0], tpl[1])

cols_description = ", ".join(list(map(format_column, col)))

question = st.text_input(label="Your question")
if st.button("Ask"):
    question_with_context = "Considering a pandas dataframe with columns {} write the python code to {}".format(cols_description, question)
    st.info(question_with_context)
    resp = openai.ask_chat_gpt_question(question_with_context, api_key)
    try:
        execute_script(resp)
    except Exception as ex:
        st.error(ex)
        st.code(resp)
    
code_query = st.text_area(label="Code to run")
previous_execution_vars = st.session_state.get("code_vars", {})
if st.button("Run"):
    previous_execution_vars = execute_script(code_query)
    st.session_state["code_vars"] = previous_execution_vars

if previous_execution_vars:
    show_variables_for_debugging(previous_execution_vars)