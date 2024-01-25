from flask import Flask, request, jsonify
import pdfplumber
import json

app = Flask(__name__)

# Replace 'your_pdf_file.pdf' with the path to your PDF file
# pdf_path = './tt.pdf'

def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            table = page.extract_tables()
            tables.extend(table)
        return tables

@app.route('/extract_tables', methods=['POST'])
def extract_tables_api():
    try:
        # Assuming the PDF file is sent in the request as a file
        pdf_file = request.files['file']
        
        # Save the uploaded PDF file
        # pdf_file.save(pdf_path)

        # Extract tables from PDF
        tables = extract_tables_from_pdf(pdf_file)

        # Convert all tables into a single JSON array
        json_array = []
        for table_number, table in enumerate(tables, start=1):
            for row in table:
                json_object = {}
                for i, cell in enumerate(row):
                    json_object[f'Column_{i + 1}'] = cell
                json_object['Table'] = table_number
                json_array.append(json_object)
                print(json_array)
        return jsonify(json_array)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
