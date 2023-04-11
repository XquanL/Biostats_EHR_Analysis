"""Object-oriented EHR Analysis."""

import sqlite3
import pickle
import datetime
from dataclasses import dataclass

connection = sqlite3.connect("ehr.db")


@dataclass
class Lab:
    """Lab class for lab information."""

    patient_id: str
    cursor = connection.cursor()

    @property
    def lab_name(self) -> str:
        """Return the lab name."""
        self.cursor.execute(
            "SELECT lab_name FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def lab_value(self) -> str:
        """Return the lab value."""
        self.cursor.execute(
            "SELECT lab_value FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def lab_units(self) -> str:
        """Return the lab units."""
        self.cursor.execute(
            "SELECT lab_units FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def lab_date(self) -> str:
        """Return the lab date."""
        self.cursor.execute(
            "SELECT lab_date FROM Labs WHERE patient_id = ?",
            (self.patient_id,),
        )
        return str(self.cursor.fetchone()[0])

    def __str__(self) -> str:
        """Print lab info."""
        return "lab " + self.lab_name + " info for patient " + self.patient_id


@dataclass
class Patient:
    """Patient class for patient information."""

    id: str
    cursor = connection.cursor()

    @property
    def gender(self) -> str:
        """Return the patient gender."""
        self.cursor.execute(
            "SELECT gender FROM Patients WHERE id = ?",
            (self.id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def dob(self) -> str:
        """Return the patient date of birth."""
        self.cursor.execute(
            "SELECT dob FROM Patients WHERE id = ?",
            (self.id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def race(self) -> str:
        """Return the patient race."""
        self.cursor.execute(
            """SELECT race FROM Patients WHERE id = ?""",
            (self.id,),
        )
        return str(self.cursor.fetchone()[0])

    @property
    def labs(self) -> list[Lab]:
        """Return a list of Lab objects for the patient."""
        # select patient_id, lab_name, lab_value, lab_units,
        # lab_date from Labs with patient_id = id
        self.cursor.execute(
            "SELECT patient_id, lab_name, lab_value, lab_units,"
            "lab_date FROM Labs WHERE patient_id = ?",
            (self.id,),
        )
        lab_info = self.cursor.fetchall()
        lab_list = []
        for i in range(len(lab_info)):
            lab_list.append(Lab(lab_info[i][0]))
        return lab_list

    def __str__(self) -> str:
        """Print patient info."""
        return "patient " + self.id + " info"

    def is_sick(self, lab_name: str, operator: str, value: float) -> bool:
        """Return a boolean indicating whether the patient is sick."""
        # get lab info for the patient
        lab_info = self.labs
        for i in range(len(lab_info)):
            if lab_info[i].lab_name == lab_name:
                labvalue = float(lab_info[i].lab_value)
                if operator == ">":
                    if labvalue > value:
                        return True
                elif operator == "<":
                    if labvalue < value:
                        return True
        return False

    @property
    def age(self) -> int:
        """Calculate the age in years of the given patient."""
        birth = datetime.datetime.strptime(
            str(self.dob), "%Y-%m-%d %H:%M:%S.%f"
        )
        age_year = (datetime.datetime.today() - birth).days / 365
        age_year_int = int(age_year)
        return age_year_int

    @property
    def earliest_admission(self) -> int:
        """Find the earliest admission date for the patient."""
        # select lab_name, lab_value, lab_units,
        # lab_date from Labs with patient_id = id
        self.cursor.execute(
            "SELECT lab_name, lab_value, lab_units,"
            "lab_date FROM Labs WHERE patient_id = ?",
            (self.id,),
        )
        lab_info = self.cursor.fetchall()
        for i in range(len(lab_info)):
            if i == 0:
                earliest_date = lab_info[i][3]
                earliest_time = datetime.datetime.strptime(
                    str(earliest_date), "%Y-%m-%d %H:%M:%S.%f"
                )
            else:
                lab_date = lab_info[i][3]
                lab_time = datetime.datetime.strptime(
                    str(lab_date), "%Y-%m-%d %H:%M:%S.%f"
                )
                if lab_time < earliest_time:
                    earliest_time = lab_time
        birth = datetime.datetime.strptime(
            str(self.dob), "%Y-%m-%d %H:%M:%S.%f"
        )
        age_year = (earliest_time - birth).days / 365
        age_year_int = int(age_year)
        return age_year_int


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[list[Patient], list[Lab]]:
    """Parse the patient and lab data files and return a tuple of lists."""
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS Labs")
    cursor.execute("DROP TABLE IF EXISTS Patients")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Labs(patient_id VARCHAR, lab_name VARCHAR,"
        "lab_value VARCHAR, lab_units VARCHAR, lab_date VARCHAR)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Patients(id VARCHAR PRIMARY KEY,"
        "gender VARCHAR, dob VARCHAR, race VARCHAR)"
    )
    patient_list: list[Patient] = []
    lab_list: list[Lab] = []

    with open(lab_filename, "r", encoding="utf-8-sig") as lab_file:
        lab_data = lab_file.readlines()
        columns = lab_data[0].strip().split("\t")
        for lines in lab_data[1:]:
            lab_info = lines.strip().split("\t")
            lab_dict = {columns[i]: lab_info[i] for i in range(len(columns))}
            lab_list.append(Lab(lab_dict["patient_id"]))
            cursor.execute(
                "INSERT INTO Labs VALUES (?, ?, ?, ?, ?)",
                lab_info,
            )

    with open(patient_filename, "r", encoding="utf-8-sig") as patient_file:
        patient_data = patient_file.readlines()
        columns = patient_data[0].strip().split("\t")
        for lines in patient_data[1:]:
            patient_info = lines.strip().split("\t")
            patient_dict = {
                columns[i]: patient_info[i] for i in range(len(columns))
            }
            patient_list.append(Patient(patient_dict["id"]))
            cursor.execute(
                "INSERT INTO Patients VALUES (?, ?, ?, ?)",
                patient_info,
            )

    connection.commit()
    return patient_list, lab_list
