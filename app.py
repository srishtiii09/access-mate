from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Lightweight summarization model
model_name = "facebook/bart-large-cnn"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# Clean webpage text extraction
def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        content = soup.find("div", {"class": "mw-parser-output"})

        if content:
            text = content.get_text(separator=" ")
        else:
            text = soup.get_text(separator=" ")

        return text[:800]

    except:
        return "Unable to extract webpage content."


# Summarizer (Stable Output Version)
def summarize_text(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=800
    )

    outputs = model.generate(
        inputs["input_ids"],
        max_length=100,
        min_length=40,
        do_sample=False,
        repetition_penalty=3.0,
        num_beams=4
    )

    summary = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    summary = summary.replace("Wikipedia", "").strip()

    return summary


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simplify", methods=["POST"])
def simplify():

    url = request.json["url"]

    webpage_text = extract_text_from_url(url)

    summary = summarize_text(webpage_text)

    return jsonify({
        "simplified": summary
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)