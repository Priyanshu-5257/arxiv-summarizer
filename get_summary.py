import requests
import xml.etree.ElementTree as ET
import PyPDF2
import os
from docx import Document
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings import GooglePalmEmbeddings
from langchain.text_splitter import CharacterTextSplitter
load_dotenv(find_dotenv())
import google.generativeai as palm
palm.configure(api_key=os.environ.get('API_KEY'))
from langchain.llms import GooglePalm

def search_arxiv(query, max_results=10):
    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:{query}',
        'max_results': max_results,
        'sortBy': 'submittedDate',  # Sort by announcement date
        'sortOrder': 'descending'   # Sort in descending order
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve data from arXiv. Status code: {response.status_code}")
        return None

    return response.text

def parse_arxiv_response(response_text):
    papers = []
    root = ET.fromstring(response_text)

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        pdf_link = entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]').attrib['href']
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        paper = {
            'title': title,
            'authors': authors,
            'pdf_link': pdf_link,
            'published': published
        }
        papers.append(paper)

    return papers

def download_paper(link, path):
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Failed to download the PDF. Status code: {response.status_code}")
        return

    with open(path, 'wb') as f:
        f.write(response.content)
    print(f"PDF downloaded successfully: {path}")

def read_paper(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        paper_text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            paper_text += page.extract_text()
    return paper_text

def divide_into_chunks(long_string, chunk_size):
    chunks = []
    for i in range(0, len(long_string), chunk_size):
        chunk = long_string[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def summ_prompt(txt):
    prompt = f"You are a machine learning enthusiast and you have to write the detailed summary of the given piece of research paper. \nGiven piece of research paper : {txt} . \nOutput summary : "
    return prompt

def final_sum(txt, authors, publication):
    prompt = f"You are a machine learning enthusiast and you have to write the detailed final blog for the given summary of the research paper of authors: {authors}. Keep in mind you are not the author so write it in the second person. \nSummary of the paper: {txt}. \nData of publication: {publication}. \nOutput: "
    return prompt

def generate_post(search_query, max_results=1):
    response_text = search_arxiv(search_query, max_results)
    if response_text:
        papers = parse_arxiv_response(response_text)
        llm = GooglePalm()
        llm.temperature = 0.1
        llm.max_output_tokens = 1024

        for paper in papers:
            link = paper['pdf_link']
            path = "temp.pdf"
            download_paper(link, path)
            paper_text = read_paper(path)

            chunks = divide_into_chunks(paper_text, 10000)

            t_prompt = [summ_prompt(chunk) for chunk in chunks]
            result = llm._generate(t_prompt)
            summary = "\n".join([res[0].text for res in result.generations if len(res) != 0])

            final_prompt = final_sum(summary, paper['authors'], paper['published'])
            post_ = llm._generate([final_prompt])
            final_post_output = post_.generations[0][0].text

            # Save the final_post as a docx file for each paper
            doc = Document()
            doc.add_paragraph(final_post_output)
            doc.save(f"final_post_{paper['title']}.docx")
            print(f"Final post for {paper['title']} saved as 'final_post_{paper['title']}.docx'.")

if __name__ == "__main__":
    search_query = input("Enter your desired query: ")
    max_results = int(input("Enter the number of papers to retrieve: "))
    generate_post(search_query, max_results)
