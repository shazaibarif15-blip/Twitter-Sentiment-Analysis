from textblob import TextBlob
import pandas as pd
import streamlit as st
import cleantext
import emoji

st.title("Sentiment Web Analyzer")

# Safe image loading
try:
    st.image('image.jpg', use_column_width=True)
except:
    st.warning("Image not found")

st.header("Now Scale Your Thoughts")

# ---------------- TEXT ANALYSIS ---------------- #
with st.expander("Analyze Your Text"):
    text = st.text_input("Text here:")

    if text:
        blob = TextBlob(text)
        p = round(blob.sentiment.polarity, 2)

        st.write('Polarity :', p)

        if p >= 0.1:
            st.write(emoji.emojize("Positive Speech :grinning_face_with_big_eyes:"))
        elif p == 0.0:
            st.write(emoji.emojize("Neutral Speech :zipper-mouth_face:"))
        else:
            st.write(emoji.emojize("Negative Speech :disappointed_face:"))

        st.write('Subjectivity:', round(blob.sentiment.subjectivity, 2))

    
    pre = st.text_input('Clean Your Text:')

    if pre:
     
        cleaned = cleantext.clean(
            pre,
            fix_unicode=True,
            to_ascii=False,
            lower=True,
            no_line_breaks=True,
            no_urls=True,
            no_emails=True,
            no_phone_numbers=True,
            no_numbers=False,
            no_digits=False,
            no_currency_symbols=True,
            no_punct=False
        )
        st.write(cleaned)

# ---------------- FILE ANALYSIS ---------------- #
# ---------------- FILE ANALYSIS ---------------- #
with st.expander('Analyze Excel files'):
    st.write("_**Note**_ : Your file must contain the column name 'Tweets'.")

    upl = st.file_uploader('Upload file', type=['csv', 'xlsx'])

    def score(x):
        return TextBlob(str(x)).sentiment.polarity

    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'

    # FIXED INDENTATION BELOW
    if upl is not None:
        try:
            # Handle CSV
            if upl.name.endswith('.csv'):
                df = pd.read_csv(upl)

            # Handle Excel
            elif upl.name.endswith('.xlsx'):
                # import openpyxl # Best to move this to the top of your file
                df = pd.read_excel(upl, engine='openpyxl')

            else:
                st.error("Unsupported file format")
                st.stop()

            # Debug: show columns
            st.write("Columns in file:", df.columns)

            if 'Tweets' not in df.columns:
                st.error("Column 'Tweets' not found in file")
            else:
                df['score'] = df['Tweets'].apply(score)
                df['analysis'] = df['score'].apply(analyze)

                st.write(df.head(10))

                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode('utf-8')

                csv = convert_df(df)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='sentiment.csv',
                    mime='text/csv',
                )

        except Exception as e:
            st.error("Error reading file. Please upload a valid CSV or Excel file.")
            st.exception(e)

# ---------------- FOOTER ---------------- #
st.write("\n" * 5)
st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)
st.write("Copy© 2026 Azib Sindhu | Made With ❤️ in Pakistan")
