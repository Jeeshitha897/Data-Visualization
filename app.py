import streamlit as st
import fitz  # PyMuPDF
import docx
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter

# Text extraction functions
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Text cleaning
def clean_text(text):
    text = re.sub(r'\W+', ' ', text.lower())
    words = text.split()
    return [word for word in words if len(word) > 2]

# Visualization functions
def plot_word_freq(words):
    freq = Counter(words).most_common(20)
    df = pd.DataFrame(freq, columns=['Word', 'Frequency'])
    st.bar_chart(df.set_index('Word'))

def show_wordcloud(words):
    wc = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Streamlit UI
st.title("📄 Text Visualization from PDF/DOCX")
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_docx(uploaded_file)

    st.subheader("📃 Extracted Text Preview")
    st.write(raw_text[:1000] + "...")  # Show first 1000 characters

    words = clean_text(raw_text)

    st.subheader("📊 Word Frequency")
    plot_word_freq(words)

    st.subheader("☁️ Word Cloud")
    show_wordcloud(words)
