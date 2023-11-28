import os
from flask import Flask, request, render_template, redirect, url_for

from openai import OpenAI
client = OpenAI()

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def index():
    return(
        render_template("index.html")
    )

@app.route("/generate.html", methods=["GET","POST"])
def generate():
    if request.method == "POST":
        topic = request.form["topic"]
        tone = request.form["tone"]
        keywords = request.form["keywords"]
        caption = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=generate_prompt(topic, tone, keywords),
            temperature=0.6,
            max_tokens = 200,
       )
        result_caption = caption.choices[0].text

        image = client.images.generate(
        model="dall-e-3",
        prompt=generate_image(topic,keywords),
        size="1024x1024",
        quality="hd",
        style = "natural",
        n=1,
        )
        response_image = image.data[0].url
        return render_template("result.html", result=result_caption, image=response_image)
        
    result = request.args.get("result")
    return render_template("generate.html")

@app.route("/result.html")
def result(result, image):
    return render_template("result.html", result = result, image = image)


def generate_prompt(topic, tone, keywords):
    return f"Create an instagram's caption for a post about {topic} with a {tone} tone. Keywords: {keywords}. Please be objective"

def generate_image(topic,keywords):
  return f"Create an image for a social media post about {topic}. Useful keywords for the image are: {keywords}. If there are words used in the image, please make sure they are properly arranged and form valid english words."

if __name__ == "__main__":
    app.run(debug=True)