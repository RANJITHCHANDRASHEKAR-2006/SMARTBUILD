
from flask import Flask, render_template ,request
from components import COMPONENTS
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/pc-builder")
def pc_builder():
    return render_template("pc_builder.html")



@app.route("/generate-build", methods=["POST"])
def generate_build():
    budget = int(request.form["budget"])
    purpose = request.form["purpose"]

    purpose_names = {
        "study": "Study and everyday use",
        "gaming": "Gaming",
        "editing": "Video editing and VFX",
        "programming": "Programming and development",
        "workstation": "Professional workstation"
    }

    # Set a spending limit for the components.
    # This first version uses a simple selection rule.
    spending_limit = budget * 0.95

    allocations = {
        "CPU": 0.20,
        "Motherboard": 0.13,
        "RAM": 0.08,
        "Graphics Card": 0.25,
        "SSD": 0.08,
        "Power Supply": 0.09,
        "Cabinet": 0.09
    }

    if purpose == "gaming":
        allocations["CPU"] = 0.18
        allocations["Graphics Card"] = 0.35
    elif purpose == "editing":
        allocations["CPU"] = 0.25
        allocations["RAM"] = 0.12
    elif purpose == "study":
        allocations["CPU"] = 0.25
        allocations["Graphics Card"] = 0.05

    components = []
    total = 0

    # Choose the most expensive catalog item that fits
    # the budget allocated to each component category.
    for category, percentage in allocations.items():
        category_limit = budget * percentage

        available = [
            item for item in COMPONENTS.get(category, [])
            if item["price"] <= category_limit
        ]

        if not available:
            continue

        chosen = max(available, key=lambda item: item["price"])

        components.append({
            "category": category,
            "name": chosen["name"],
            "price": chosen["price"]
        })

        total += chosen["price"]

    return render_template(
        "build_result.html",
        budget=budget,
        purpose=purpose_names.get(purpose, "General use"),
        components=components,
        total=total,
        remaining=budget - total
    )

if __name__ == "__main__":
    app.run(debug=True)
