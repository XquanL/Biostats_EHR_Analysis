# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

## Modules

* `ehr_analysis` provides four simple analytical capabilities for EHR data and two class(`Patient` and `Lab`), including functions that are able to:
1. **Read and parse the data files to store data into a SQLite database**
2. **Return the age in years of a given patient**
3. **Indicate a patient's situation based on a test result**
4. **Compute the age of a given patient when their earliest lab was recorded**

## Installation
Feel free to copy [ehr_analysis.py](https://github.com/biostat821-2023/ehr-utils-XquanL/blob/phase3_new/src/ehr_analysis.py).

## Usage
The `ehr_analysis` contains two classes and one function.
1. **Read and parse the data files**
  
   This function takes both patient and lab file names, or the path to those files (`string`), inserts data in those files into a SQLite database, and produces two lists in a tuple format that contain patients' basic information(`Patient` class) and relevant lab data(`Lab` class), respectively.
  
   *Example usage:*
  ```{python}
  from ehr_analysis import parse_data
  
    def test_Patient_class() -> None:
    """Test the parse_data() Patient has the correct attributes."""
        with fake_files(temp_patient, temp_lab) as (patient, lab):
            patient, labs = parse_data(patient, lab)
        assert patient[0].id == "1"
        assert patient[0].gender == "F"
        assert patient[0].dob == "1947-01-01 00:00:00.000000"
        assert patient[0].race == "white"


    def test_Lab_class() -> None:
        """Test the parse_data() Lab has the correct attributes."""
        with fake_files(temp_patient, temp_lab) as (patient, lab):
            patient, labs = parse_data(patient, lab)
        assert labs[0].patient_id == "1"
        assert labs[0].lab_name == "HDL"
        assert labs[0].lab_value == "50"
        assert labs[0].lab_units == "mg/dL"
        assert labs[0].lab_date == "1980-01-01 00:00:00.000000"
   ```

    
    
2. **Return the age in years of a given patient**
    
    This is a property of the class `Patient`, which returns the age in years of the given patient.
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_age
  
    def test_patient_age() -> None:
    """test whether the Patient age property returns the correct age"""
    lab1 = Lab(
        patient_id="1",
    )
    patient1 = Patient(
        id="1",
    )
    assert patient1.age == 76
    ```
    

    
    
3. **Indicate a patient's situation based on a test result**
    
    This is a property of the class `Patient`, which takes a lab name (`string`), an operator (`string`), and a value of that lab result (`float`), returns a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. 
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_is_sick
  
    def test_is_sick() -> None:
    """Test whether the is_sick method returns the correct boolean value"""
    lab1 = Lab(
        patient_id="1",
    )
    patient1 = Patient(
        id="1",
    )
    assert patient1.is_sick("HDL", ">", 30) is True
    ```



4. **Compute the age of a given patient when their earliest lab was recorded**

    This is a method of the class `Patient`, which returns the age in years (`int`) of a given patient when their earliest lab was recorded.
    
   *Example usage:*
    ```{python}
    from ehr_analysis import patient_is_sick
  
    def test_earliest_admission() -> None:
    """Test whether the earliest_admission property returns the correct age"""
    patient1 = Patient(
        id="1",
    )
    assert patient1.earliest_admission == 33
    ```


 ## Development
 We welcome contributions! Before opening a pull request, please confirm that existing regression tests pass:
   ```{python}
   python -m pytest tests/
   ```
    
