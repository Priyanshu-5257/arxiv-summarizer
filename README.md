**README for Research Paper Summarizer**

## Introduction

This code is designed to help you generate detailed summaries for research papers on a given topic. By providing a search query and the number of recent papers you want to retrieve, the code will fetch the papers from arXiv, extract their content, and create a summary for each paper. Finally, it will generate a blog-style document (docx file) containing the summaries of all the papers retrieved.

## Prerequisites

Before running the code, you need to have the following prerequisites:

1. Python 3 installed on your system.
2. Install the required Python libraries using the following command:

```
pip install -r requirements.txt
```

## How to Use

1. Clone or download the code from the provided repository.

2. Create a virtual environment (optional but recommended):

```
python -m venv venv
```

3. Activate the virtual environment:

   - **Windows**:

   ```
   venv\Scripts\activate
   ```

   - **Linux/macOS**:

   ```
   source venv/bin/activate
   ```

4. Make sure you have an arXiv API key. If you don't have one, you can sign up for it at [https://arxiv.org/account/signup](https://arxiv.org/account/signup). Once you have the API key, create a file named `.env` in the same directory as your code and add the following line:

```
API_KEY=YOUR_ARXIV_API_KEY
```

Replace `YOUR_ARXIV_API_KEY` with your actual arXiv API key.

5. Run the code:

```
python your_code_filename.py
```

6. The code will prompt you to enter the search query for the type of research papers you want and the number of recent papers you want to retrieve.

7. After providing the inputs, the code will download the papers, generate summaries for each paper, and then create a docx file named "final_post_[PAPER_TITLE].docx" for each paper. These docx files will contain the detailed summaries.

## Additional Information

- The code uses the arXiv API to fetch research papers related to the provided search query.
- It then uses Google's GPT-3 based language model, called GooglePalm, to generate summaries for each paper.
- The summaries are generated in two steps: First, the code creates a prompt to ask the model to summarize chunks of the paper. Then, it generates a final blog-style post using the individual summaries.
- The summary is written in the second person, assuming you are a machine learning enthusiast writing about the research paper.

Please note that using the arXiv API and GooglePalm API may involve costs based on usage. Make sure to review the terms of use for these services.

For more information or to report any issues, feel free to contact [Your Contact Email/Username].

**Happy Summarizing!**
