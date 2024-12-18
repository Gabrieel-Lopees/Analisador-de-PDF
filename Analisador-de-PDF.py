import os
import shutil
import openai
import PyPDF2
from PyPDF2 import PdfReader

#configurações API
openai.api_key = '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'

# receber um PDF
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None

# 2: Converter para Markdown
def convert_to_markdown(text):
    try:
        markdown_text = "\n".join([f"# {line}" if line.strip() else line for line in text.splitlines()])
        return markdown_text
    except Exception as e:
        print(f"Erro ao converter para Markdown: {e}")
        return None

# 3: Análise e Resumo 
def summarize_with_chatgpt(content, filename):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em resumir PDFs."},
                {"role": "user", "content": f"Por favor, analise o seguinte texto extraído do PDF '{filename}' e forneça um resumo detalhado:\n{content}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro na API do ChatGPT: {e}")
        return None

# 4: Salvar em uma pasta com o nome original
def save_files(pdf_path, markdown_content, summary):
    try:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = base_name

        
        os.makedirs(output_dir, exist_ok=True)

        
        if markdown_content:
            with open(os.path.join(output_dir, f"{base_name}.md"), "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)

        if summary:
            with open(os.path.join(output_dir, f"{base_name}_summary.md"), "w", encoding="utf-8") as summary_file:
                summary_file.write(summary)

        print(f"Arquivos salvos em: {output_dir}")
    except Exception as e:
        print(f"Erro ao salvar arquivos: {e}")

def main():
    pdf_path = input("Digite o caminho do arquivo PDF: ").strip()

    if not os.path.exists(pdf_path):
        print("O arquivo PDF não foi encontrado.")
        return


    text = extract_text_from_pdf(pdf_path)
    if not text:
        return

    
    markdown_content = convert_to_markdown(text)


    summary = summarize_with_chatgpt(text, os.path.basename(pdf_path))
    if not summary:
        return

    
    save_files(pdf_path, markdown_content, summary)

if __name__ == "__main__":
    main()

