from flask import Flask, render_template, request, flash, send_file
import os
import pandas as pd
import dotenv
from urllib.parse import urlparse

from scraper.distribucion import scrape_task
from scraper.excel import descargar_excel

dotenv.load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("X-RapidAPI-Key")


def is_valid_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica que se haya enviado un archivo
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo')
            return render_template('index.html')

        file = request.files['file']

        # Verifica que el nombre del archivo y la extensión sean válidos
        if file.filename == '':
            flash('No se seleccionó ningún archivo')
            return render_template('index.html')

        if file and file.filename.endswith('.xlsx'):
            try:
                # Lee el archivo Excel y obtén el contenido de la primera columna
                df = pd.read_excel(file, header=None)
                # first_column_data = df.iloc[:, 0].tolist()
                first_column_data = [url for url in df.iloc[:, 0] if is_valid_url(str(url))]
                
                if not first_column_data:
                    flash('No se encontraron URLs válidas en la primera columna del archivo Excel.')
                    return render_template('index.html')
                
                Excel = scrape_task(first_column_data)
                output = descargar_excel(Excel)
                return send_file(
                    output,
                    as_attachment=True,
                    download_name='output.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except Exception as e:
                flash(f'Ocurrió un error al procesar el archivo: {e}')

        else:
            flash('Formato de archivo no válido. Se espera un archivo Excel (.xlsx)')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
