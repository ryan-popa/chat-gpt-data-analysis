import requests
import json
import streamlit as st

from cache.cache import cache_string

def _make_gpt_request(text, api_key):
    r = requests.post(
        "https://api.openai.com/v1/engines/text-davinci-003-playground/completions",
        data=json.dumps({
            "prompt": text,
            "max_tokens":256,
            "temperature":0.7,
            "top_p":1,
            "frequency_penalty":0,
            "presence_penalty":0,
            "best_of":1,
            "echo":False,
            "logprobs":0,
            "stream":False
            }),
        headers={
            "authorization": "Bearer {}".format(api_key),
            "content-type": "application/json"
        }
    )
    return r.text

def _parse_gpt_response(r: str):
    try:
        d = json.loads(r)
        # st.code(d)
        return (d["choices"][0]["text"], d["choices"][0]["finish_reason"])
    except Exception as ex:
        st.error(ex)
        st.code(d)

def ask_chat_gpt_question(question, api_key):
    try:
        r = _make_gpt_request(question, api_key)
        return _parse_gpt_response(r)[0]
    except Exception as ex:
        st.write("Exception while processing question {}".format(question))
        raise ex
