import pdfplumber
import pandas as pd

def pdf_to_markdown(pdf_path):
    #Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        #Initialize an empty string to store the markdown text
        markdown_text = ""

        #Iterate over each page in the PDF
        for page in pdf.pages:
            #Extract the text from the page and add it to the markdown text
            markdown_text += page.extract_text()

            #Extract the tables
            tables = page.extract_tables()

            #Iterate over each table
            for table in tables:
                #Convert table to DF
                df = pd.DataFrame(table[1:], columns=table[0])

                #Convert the DF to md and add it
                markdown_test += df.to_markdown()

        return markdown_test

md = pdf_to_markdown("test.pdf")

with open("test.md", "w", encoding='utf-8') as f:
    f.write(md)
