FROM python:3.10
# Pehle root user hai by default, to yahan packages install karo
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Ab user add karo aur switch karo
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir openai-chatkit==1.4.0


COPY --chown=user . /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
