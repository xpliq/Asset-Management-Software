import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QCheckBox, QComboBox, QDateEdit
from PyQt6.QtCore import Qt, QDate
from datetime import datetime

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 500, 400)

        # Create a tab widget
        self.tabs = QTabWidget()

        # Create the tabs
        search_tab = QWidget()
        add_tab = QWidget()
        display_tab = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(search_tab, "Search")
        self.tabs.addTab(add_tab, "Add")
        self.tabs.addTab(display_tab, "Display")

        # Set the central widget of the main window to the tab widget
        self.setCentralWidget(self.tabs)

        # Populate the search tab
        self.populate_search_tab(search_tab)

        # Populate the add tab
        self.populate_add_tab(add_tab)

        # Populate the display tab
        self.populate_display_tab(display_tab)


    def populate_display_tab(self, tab):
        layout = QVBoxLayout()
        table = QTableWidget()

        # Read the CSV file
        df = pd.read_csv('draft.csv')

        # Sort by location
        df = df.sort_values(by='Location')

        # Get the number of rows and columns from the DataFrame
        num_rows, num_cols = df.shape

        # Set the table dimensions
        table.setRowCount(num_rows)
        table.setColumnCount(num_cols)

        # Set the table headers
        table.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data
        for i in range(num_rows):
            for j in range(num_cols):
                value = df.iat[i, j]
                if pd.isna(value):  # Handle empty cells
                    value = ""
                item = QTableWidgetItem()
                if isinstance(value, float):
                    formatted_value = f'{value:.0f}'.rstrip('.0')  # Remove the .0
                    item.setData(Qt.ItemDataRole.DisplayRole, formatted_value)
                else:
                    item.setData(Qt.ItemDataRole.DisplayRole, str(value))
                table.setItem(i, j, item)

        # Resize the columns to fit the content
        table.resizeColumnsToContents()

        # Set table properties
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)  # Change to SelectItems
        table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        layout.addWidget(table)
        tab.setLayout(layout)

    def populate_search_tab(self, tab):
        layout = QVBoxLayout()

        # Search input fields
        serial_number_label = QLabel("Serial Number:")
        self.serial_number_input = QLineEdit()
        self.serial_number_input.returnPressed.connect(self.search_machines)  # Added "Enter" key press event
        id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        self.id_input.returnPressed.connect(self.search_machines)
        name_label = QLabel("Machine Name:")
        self.name_input = QLineEdit()
        self.name_input.returnPressed.connect(self.search_machines)


        # Check for Completed Only toggle
        self.completed_only_checkbox = QCheckBox("Check for Distributable Only")
        self.completed_only_checkbox.stateChanged.connect(self.search_machines)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_machines)

        layout.addWidget(serial_number_label)
        layout.addWidget(self.serial_number_input)
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.completed_only_checkbox)
        layout.addWidget(search_button)

        # Search results table
        self.search_results_table = QTableWidget()
        self.search_results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)  # Enable cell selection
        layout.addWidget(self.search_results_table)

        tab.setLayout(layout)

    def populate_add_tab(self, tab):
        layout = QVBoxLayout()

        # Line edit fields
        self.machine_name_input = QLineEdit()
        layout.addWidget(QLabel("Machine Name:"))
        layout.addWidget(self.machine_name_input)
        self.serial_number_input_add = QLineEdit()
        layout.addWidget(QLabel("Serial Number/ID:"))
        layout.addWidget(self.serial_number_input_add)
        self.hub_id_input = QLineEdit()
        layout.addWidget(QLabel("Hub ID:"))
        layout.addWidget(self.hub_id_input)
        self.description_input = QLineEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        # Date edit fields
        self.updated_snx_input = QDateEdit()
        layout.addWidget(QLabel("Updated (snx):"))
        layout.addWidget(self.updated_snx_input)
        self.updated_manual_input = QDateEdit()
        layout.addWidget(QLabel("Updated (Manual):"))
        layout.addWidget(self.updated_manual_input)

        # Combo box fields
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "Distributed/Loaned", "Waiting", "In Progress", "In Progress (surplus)", "Complete"])
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_input)
        self.deliverable_input = QComboBox()
        self.deliverable_input.addItems(["Holding", "In For Repair", "Distributable", "Awaiting", "Surplus", "Surplused"])
        layout.addWidget(QLabel("Deliverable:"))
        layout.addWidget(self.deliverable_input)
        self.location_input = QComboBox()
        self.location_input.addItems([f"{i}{j}" for i in "ABCDEF" for j in range(1, 7)])
        layout.addWidget(QLabel("Location:"))
        layout.addWidget(self.location_input)

        # Add button
        add_button = QPushButton("Add Machine")
        add_button.clicked.connect(self.add_machine)
        layout.addWidget(add_button)

        tab.setLayout(layout)

    def add_machine(self):
        # Read the CSV file
        df = pd.read_csv('draft.csv')

        # Get input data
        data = {
            "Machine Name": self.machine_name_input.text().strip(),
            "Serial Number/ID": self.serial_number_input_add.text().strip(),
            "Hub ID": self.hub_id_input.text().strip(),
            "Updated(snx)": self.updated_snx_input.date().toString("yyyy-MM-dd"),
            "Updated(Manual)": self.updated_manual_input.date().toString("yyyy-MM-dd"),
            "Status": self.status_input.currentText(),
            "Description": self.description_input.text().strip(),
            "Deliverable": self.deliverable_input.currentText(),
            "Location": self.location_input.currentText(),
        }

        # Append new row to DataFrame
        df = df._append(data, ignore_index=True)

        # Write DataFrame to CSV
        df.to_csv('draft.csv', index=False)

        # Clear input fields
        self.machine_name_input.clear()
        self.serial_number_input_add.clear()
        self.hub_id_input.clear()
        self.updated_snx_input.setDate(QDate.currentDate())
        self.updated_manual_input.setDate(QDate.currentDate())
        self.status_input.setCurrentIndex(0)
        self.description_input.clear()
        self.deliverable_input.setCurrentIndex(0)
        self.location_input.setCurrentIndex(0)

        # Refresh Display tab
        self.populate_display_tab(self.tabs.widget(2))

        # Refresh all tabs
        self.re_populate_all_tabs()

        # Stay on the Add tab after submitting a new machine
        self.tabs.setCurrentIndex(1)

    def search_machines(self):
        # Clear the existing search results
        self.search_results_table.clearContents()

        # Read the CSV file
        df = pd.read_csv('draft.csv')

        # Apply filters based on user input
        serial_number = self.serial_number_input.text().strip()
        id_value = str(self.id_input.text().strip())  # Convert to string
        name = self.name_input.text().strip()
        completed_only = self.completed_only_checkbox.isChecked()

        # Apply filters based on user input
        filtered_df = df

        # Apply serial number filter
        if serial_number:
            filtered_df = filtered_df[filtered_df['Serial Number/ID'].str.contains(serial_number, case=False, na=False)]

        # Apply ID filter
        if id_value:
            filtered_df = filtered_df[filtered_df['Hub ID'].astype(str).str.contains(id_value, case=False, na=False)]

        # Apply machine name filter
        if name:
            filtered_df = filtered_df[filtered_df['Machine Name'].str.contains(name, case=False, na=False)]

        # Additional filter for status (completed only)
        if completed_only:
            filtered_df = filtered_df[filtered_df['Deliverable'] == 'Distributable']

        # Sort by location
        filtered_df = filtered_df.sort_values(by='Location')

        # Update the search results table
        self.update_search_results_table(filtered_df)

    def re_populate_all_tabs(self):
        # Clear all tabs
        for _ in range(self.tabs.count()):
            self.tabs.removeTab(0)

        # Recreate the tabs
        search_tab = QWidget()
        add_tab = QWidget()
        display_tab = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(search_tab, "Search")
        self.tabs.addTab(add_tab, "Add")
        self.tabs.addTab(display_tab, "Display")

        # Populate the tabs
        self.populate_search_tab(search_tab)
        self.populate_add_tab(add_tab)
        self.populate_display_tab(display_tab)

    def update_search_results_table(self, df):
        # Clear the existing table contents
        self.search_results_table.clearContents()

        # Get the number of rows and columns from the DataFrame
        num_rows, num_cols = df.shape

        # Set the table dimensions
        self.search_results_table.setRowCount(num_rows)
        self.search_results_table.setColumnCount(num_cols)

        # Set the table headers
        self.search_results_table.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data
        for i in range(num_rows):
            for j in range(num_cols):
                value = df.iat[i, j]
                if pd.isna(value):  # Handle empty cells
                    value = ""
                item = QTableWidgetItem()
                if isinstance(value, float):
                    formatted_value = f'{value:.0f}'.rstrip('.0')  # Remove the .0
                    item.setData(Qt.ItemDataRole.DisplayRole, formatted_value)
                else:
                    item.setData(Qt.ItemDataRole.DisplayRole, str(value))
                self.search_results_table.setItem(i, j, item)


        # Resize the columns to fit the content
        self.search_results_table.resizeColumnsToContents()

        # Set table properties
        self.search_results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.search_results_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.search_results_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.search_results_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.search_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
