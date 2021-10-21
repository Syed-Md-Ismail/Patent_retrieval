from flask import Flask, render_template, flash, redirect, request
from forms import InputTextForm


########################################################################################

from query_from_solr_system import query_string

########################################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b3cb4acbd4972dd1b378e5ec3524706d'

########################################################################################


## Redirects user to home page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Welcomes user to Patent Search engine home page. 
    User can type in the text that could be connected to patent, 
    and if similar matching words are present in solr system, they will get recommendations back. 
    
    After validating that input text, the function query_string is triggered.
    It finds the best matches to that incident number and is stored in variable posts.
    query_string also returns a variable 'message'. 
    In case 'message' == "No error", 
        the recommendations are displayed in home.html, by passing posts as parameter
    else
        empty html page is displayed
    
    """
    
    
    form = InputTextForm()
    
    ## Input incident number or text is captured here.
    data = request.form.get('input_text')
    
    if form.validate_on_submit():

        # posts, message = recommendation_pipeline(data)
        posts, message = query_string(data)
        
        if(message == "No error"):
            return render_template('home.html', posts=posts, form=form)
        else:
            ## Display flash message
            flash(f'{message}', 'danger')
            return render_template('home.html', form=form)
    
    else:
        return render_template('home.html', form=form)



@app.route('/Chemovator')
def Chemovator():
    return redirect('https://www.chemovator.com/ventures/#ventureportfolio')

########################################################################################


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=7000, use_reloader=True)