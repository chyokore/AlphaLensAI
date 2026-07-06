import json
import streamlit as st
from pathlib import Path


def get_economic_events():

    json_path = Path(__file__).parent / "economic_calendar.json"



    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    
        return data

    except Exception as e:
        import traceback

        st.error(str(e))
        st.code(traceback.format_exc())

        return []