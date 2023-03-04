FROM continuumio/miniconda3

WORKDIR /home/app

RUN pip install pandas streamlit matplotlib plotly
COPY . /home/app/

EXPOSE 8501

CMD streamlit run --server.port $PORT app.py