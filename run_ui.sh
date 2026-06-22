#!/bin/bash
cd "$(dirname "$0")"
streamlit run Ui/app.py --logger.level=info
