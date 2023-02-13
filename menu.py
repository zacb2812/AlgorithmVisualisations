import os
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        width = 500
        height = 400

        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.title("Algorithm Visualisations")
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.minsize(500, 400)
        self.maxsize(500, 400)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        def run_A_star():
            self.destroy()
            os.system("python Python\\Algorithms\\AlgorithmVisualisations\\a_star_visualisation.py")

        def run_Bubble_sort():
            self.destroy()
            os.system("python Python\\Algorithms\\AlgorithmVisualisations\\bubble_sort_visualisation.py")

        def run_Insertion_sort():
            self.destroy()
            os.system("python Python\\Algorithms\\AlgorithmVisualisations\\insertion_sort_visualisation.py")

        label1 = ctk.CTkLabel(master=self, text="Zac Barsdell's\n Algorithm Visualisations", font=(None, 25))
        label1.grid(row=0, column=0, columnspan=2)

        button1 = ctk.CTkButton(master=self, text="A* Search Visualisation", command=run_A_star)
        button1.grid(row=1, column=0)

        button2 = ctk.CTkButton(master=self, text="Insertion Sort Visualisation", command=run_Insertion_sort)
        button2.grid(row=1, column=1)

        button3 = ctk.CTkButton(master=self, text="Bubble Sort Visualisation", command=run_Bubble_sort)
        button3.grid(row=2, column=0, pady=80)


if __name__ == "__main__":
    app = App()
    app.mainloop()
