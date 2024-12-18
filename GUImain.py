import tkinter as tk
from tkinter import messagebox
from rdflib import Graph, Literal
from rdflib.namespace import Namespace

# Loading the RDF/XML ontology
g = Graph()
g.parse("ontology.owl", format="xml")

# Defining Namespaces (Ontology URIs)
SHAPES = Namespace("urn:shapes:ontology#")

# Creating a main window
root = tk.Tk()
root.title("Intelligent Tutoring System for Shapes")


# Defining a function for handling the shape selection
def show_formulas(event=None):
    # Getting the selected shape
    selected_shape = shape_var.get()

    # Clearing previous formula text and input fields
    formula_text.delete(1.0, tk.END)
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Querying for formulas related to the selected shape
    query = """
        SELECT ?formula ?description WHERE {
            ?shape rdf:type <urn:shapes:ontology#Shape> .
            ?shape rdfs:label ?shapeLabel .
            ?shape <urn:shapes:ontology#hasFormula> ?formula .
            OPTIONAL { ?formula rdfs:comment ?description . }
            FILTER(?shapeLabel = ?selectedShape)
        }
    """

    results = g.query(query, initBindings={"selectedShape": Literal(selected_shape)})

    # Displaying the formulas in the text area
    if results:
        formula_options = []
        for row in results:
            description = (
                row.description
                if hasattr(row, "description")
                else "No description available"
            )
            formula_text.insert(
                tk.END, f"{row.formula.split('#')[-1]}: {description}\n"
            )
            formula_options.append(row.formula.split("#")[-1])

        # Updating the formula dropdown menu
        formula_var.set(formula_options[0])
        formula_menu["menu"].delete(0, "end")
        for option in formula_options:
            formula_menu["menu"].add_command(
                label=option, command=tk._setit(formula_var, option, show_input_fields)
            )

        # Showing input fields based on the selected formula
        show_input_fields()
    else:
        formula_text.insert(tk.END, "No formulas found for this shape.")


# Defining a function for creating input fields
def create_input_fields(fields):
    global input_entries
    input_entries = {}
    for field in fields:
        label = tk.Label(input_frame, text=field + ":")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(input_frame)
        entry.pack(side=tk.LEFT)
        input_entries[field.lower()] = entry


# Defining a function for showing input fields based on the selected formula
def show_input_fields(event=None):
    for widget in input_frame.winfo_children():
        widget.destroy()

    selected_shape = shape_var.get()
    selected_formula = formula_var.get()

    if selected_shape == "Triangle":
        if "Area" in selected_formula:
            create_input_fields(["Base", "Height"])
        elif "Perimeter" in selected_formula:
            create_input_fields(["Side1", "Side2", "Side3"])
    elif selected_shape == "Circle":
        if "Area" in selected_formula:
            create_input_fields(["Radius"])
        elif "Circumference" in selected_formula:
            create_input_fields(["Radius"])
    elif selected_shape == "Square":
        if "Area" in selected_formula:
            create_input_fields(["Side"])
        elif "Diagonal" in selected_formula:
            create_input_fields(["Side"])
    elif selected_shape == "Rectangle":
        if "Area" in selected_formula:
            create_input_fields(["Length", "Breadth"])
        elif "Diagonal" in selected_formula:
            create_input_fields(["Length", "Breadth"])
    elif selected_shape == "Pentagon":
        if "Area" in selected_formula:
            create_input_fields(["Side"])
    elif selected_shape == "Hexagon":
        if "Area" in selected_formula:
            create_input_fields(["Side"])


# Defining a function for calculating the area or perimeter
def calculate():
    selected_shape = shape_var.get()
    selected_formula = formula_var.get()
    try:
        if selected_shape == "Triangle":
            if "Area" in selected_formula:
                base = float(input_entries["base"].get())
                height = float(input_entries["height"].get())
                area = 0.5 * base * height
                messagebox.showinfo("Result", f"Area of Triangle: {area}")
            elif "Perimeter" in selected_formula:
                side1 = float(input_entries["side1"].get())
                side2 = float(input_entries["side2"].get())
                side3 = float(input_entries["side3"].get())
                perimeter = side1 + side2 + side3
                messagebox.showinfo("Result", f"Perimeter of Triangle: {perimeter}")
        elif selected_shape == "Circle":
            if "Area" in selected_formula:
                radius = float(input_entries["radius"].get())
                area = 3.14159 * radius**2
                messagebox.showinfo("Result", f"Area of Circle: {area}")
            elif "Circumference" in selected_formula:
                radius = float(input_entries["radius"].get())
                circumference = 2 * 3.14159 * radius
                messagebox.showinfo(
                    "Result", f"Circumference of Circle: {circumference}"
                )
        elif selected_shape == "Square":
            if "Area" in selected_formula:
                side = float(input_entries["side"].get())
                area = side**2
                messagebox.showinfo("Result", f"Area of Square: {area}")
            elif "Diagonal" in selected_formula:
                side = float(input_entries["side"].get())
                diagonal = side * (2**0.5)
                messagebox.showinfo("Result", f"Diagonal of Square: {diagonal}")
        elif selected_shape == "Rectangle":
            if "Area" in selected_formula:
                length = float(input_entries["length"].get())
                breadth = float(input_entries["breadth"].get())
                area = length * breadth
                messagebox.showinfo("Result", f"Area of Rectangle: {area}")
            elif "Diagonal" in selected_formula:
                length = float(input_entries["length"].get())
                breadth = float(input_entries["breadth"].get())
                diagonal = (length**2 + breadth**2) ** 0.5
                messagebox.showinfo("Result", f"Diagonal of Rectangle: {diagonal}")
        elif selected_shape == "Pentagon":
            if "Area" in selected_formula:
                side = float(input_entries["side"].get())
                area = 1 / 4 * (5 * (5 + 2 * 2.2360679775) ** 0.5) * side**2
                messagebox.showinfo("Result", f"Area of Pentagon: {area}")
        elif selected_shape == "Hexagon":
            if "Area" in selected_formula:
                side = float(input_entries["side"].get())
                area = 3 * (3**0.5) / 2 * side**2
                messagebox.showinfo("Result", f"Area of Hexagon: {area}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")


# Creating a Label for Shape Selection
label = tk.Label(root, text="Select a Shape:")
label.pack()

# Creating a dropdown menu for selecting a shape
shapes = ["Triangle", "Circle", "Square", "Rectangle", "Pentagon", "Hexagon"]
shape_var = tk.StringVar(value=shapes[0])  # default shape
shape_menu = tk.OptionMenu(root, shape_var, *shapes, command=show_formulas)
shape_menu.pack()

# Creating a Label for Formula Selection
formula_label = tk.Label(root, text="Select a Formula:")
formula_label.pack()

# Creating a dropdown menu for selecting a formula
formula_var = tk.StringVar()
formula_menu = tk.OptionMenu(root, formula_var, [], command=show_input_fields)
formula_menu.pack()

# Creating a frame for input fields
input_frame = tk.Frame(root)
input_frame.pack()

# Creating a button for calculating the area or perimeter
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

# Creating a Text widget for displaying formulas
formula_text = tk.Text(root, height=10, width=60)
formula_text.pack()

# Starting the Tkinter event loop
root.mainloop()
