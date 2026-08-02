import graphviz
import tkinter as tk

dot = graphviz.Digraph()

dot.node("A", "Node A")
dot.edge("A", "B", label="Edge AB")

dot.format = "png"

dot.render("output")