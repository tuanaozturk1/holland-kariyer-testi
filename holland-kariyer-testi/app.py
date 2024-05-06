from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_entry_page(request: Request):
    return templates.TemplateResponse("giris.html", {"request": request})

@app.get("/test")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


personality_types = {
    "Araştırıcı": [1, 3, 4, 8, 11, 17, 22, 34, 39, 41, 47, 48, 68, 71, 80],
    "Artistik": [6, 10, 14, 31, 32, 42, 44, 45, 50, 62, 72, 74, 77, 78, 81],
    "Sosyal": [2, 21, 29, 37, 49, 55, 58, 60, 64, 65, 66, 73, 87, 88, 90],
    "Girişimci": [7, 15, 16, 18, 20, 28, 33, 35, 51, 56, 63, 67, 75, 83, 85],
    "Geleneksel": [5, 12, 23, 24, 27, 30, 36, 43, 46, 57, 69, 76, 86, 89],
    "Gerçekçi": [9, 13, 19, 25, 26, 38, 40, 52, 53, 54, 59, 61, 70, 82, 84]
}


answer_scores = {
    "like": 1,
    "neutral": 0,
    "dislike": 0
}

colors = {
    "Araştırıcı": "rgba(255, 99, 132, 1)",
    "Artistik": "rgba(255, 159, 64, 1)",
    "Sosyal": "rgba(54, 162, 235, 1)",
    "Girişimci": "rgba(255, 206, 86, 1)",
    "Geleneksel": "rgba(75, 192, 192, 1)",
    "Gerçekçi": "rgba(153, 102, 255, 1)"
}



@app.post("/submit")
async def calculate_personality(request: Request):
    form_data = await request.form()
    scores = {ptype: 0 for ptype in personality_types.keys()}  # Initialize scores

    for ptype, questions in personality_types.items():
        for qnum in questions:
            answer_key = f"question{qnum}"
            answer = form_data.get(answer_key, "neutral")
            scores[ptype] += answer_scores.get(answer, 0)

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    labels = [ptype for ptype, score in sorted_scores]
    data = [score for ptype, score in sorted_scores]

    return templates.TemplateResponse("results.html", {
        "request": request,
        "sorted_scores": sorted_scores,
        "scores": data,
        "labels": labels,
        "colors": colors

    })


