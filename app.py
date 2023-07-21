import os
import openai
from flask import Flask, render_template, request, redirect, url_for, session
openai.api_key = "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"

app = Flask(__name__, template_folder='C:/Users/rachkim/OneDrive - Capgemini/Python/compl.AI/templates', static_folder='C:/Users/rachkim/OneDrive - Capgemini/Python/compl.AI/static')

app.secret_key = "b68fd3754a9b394a78bf4055e2d519d6"

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    uploaded_regpdf = request.files['file']

    reg_input = request.form['reg_input']
    if uploaded_file.filename != '':
        contents = uploaded_file.read().decode('utf-8')
        prompt_openAI = 'Give me a holistic list of all sections in my policy document that may not be compliant with the following regulation: ' +reg_input +', \
                        and provide specific and detailed suggested edits that corporate and investment banks can take: ' + contents
        messages_openAI = [
            {'role':'assistant', 'content':'Your role is to act as the chief compliance officer of a corporate and investment bank'},
            {'role':'assistant', 'content':'For each modification that is needed to the policy, the answer should be in the format of 1 line beginning with "Section: " listing the document section name for the policy,\
                                            a second line below which begins with a "• " bullet point, stating which regulatory board and regulation name this policy relates to, \
                                            a third line below which begins with a "• " bullet point, explaining what the current policy states\
                                            and why it is not compliant, then a fourth line below that begins with "• Suggested enhancement" bullet point that explains as specifically as possible \
                                            how the policy should be modified to make this compliant.'},
            {"role": "user", "content": prompt_openAI}         
        ]

        response_openAI = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_openAI,
            temperature=0,
            max_tokens=2000,
        )
        ai_output = response_openAI["choices"][0].message["content"]   

        output_filename = 'temp_output.txt'
        with open(output_filename, 'w') as f:
            f.write(ai_output)

        return redirect(url_for('results', output_file=output_filename))
    else:
        return "No file uploaded", 400

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/results")
def results():
    output_file = request.args.get('output_file', None)
    if output_file:
        with open(output_file, 'r') as f:
            message = f.read()
    else:
        return redirect(url_for('index'))

    formatted_message = []
    for line in message.split('\n'):
        if "•" not in line and "Suggested edit:" not in line:
            formatted_line = f'<span class="header">{line}</span><br>'
        else:
            formatted_line = f'{line}<br>'
        formatted_message.append(formatted_line)
    
    formatted_message = ''.join(formatted_message)

    message = message.replace('\n', '<br>')
    return render_template('index.html', message=formatted_message)

if __name__ == "__main__":
    app.run(debug=True)
