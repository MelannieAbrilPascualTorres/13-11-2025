from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

apiKey ="1320e414b5414686ac59e14362f5a2d3"
api_url = "https://api.spoonacular.com/recipes/"

app = Flask(__name__)
app.secret_key = "cuando_donde_tiras_queso"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=["POST"])
def search():
    recipe_name = request.form.get('receta', '').strip().lower()

    if not recipe_name:
        flash('Ingrese una receta', 'error')
        return redirect(url_for('index'))

    try:
        buscar = f"{api_url}complexSearch"
        params = {
            'apiKey': apiKey,
            'query': recipe_name,
            'number': 1
        }

        resp = requests.get(buscar, params=params)

        if resp.status_code == 200:
            data = resp.json()

            if data['results']:
                recipe_data = data['results'][0]
                recipe_id = recipe_data['id']
                
                info_url = f"{api_url}{recipe_id}/information"
                info_params = {
                    'apiKey': apiKey,
                    'includeNutrition': True
                }

                info_resp = requests.get(info_url, params=info_params)
                
                if info_resp.status_code == 200:
                    recipe2 = info_resp.json()

                    recipe_info = {
                        'name': recipe2['title'].title(),
                        'id': recipe2['id'],
                        'image': recipe2['image'],
                        'ready_in_minutes': recipe2.get('readyInMinutes', 'N/A'),
                        'servings': recipe2.get('servings', 'N/A'),
                        'nutrition': recipe2.get('nutrition', {})
                    }
                    return render_template('api.html', recipe=recipe_info)
                else:
                    flash('Error al obtener información detallada', 'error')
                    return redirect(url_for('index'))
            else:
                flash(f'Receta "{recipe_name}" no encontrada', 'error')
                return redirect(url_for('index'))
        else:
            flash(f'Receta "{recipe_name}" no encontrada', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('Error al buscar la receta', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)