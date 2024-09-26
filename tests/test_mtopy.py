import unittest
import numpy as np

from mtopy.mtopy import MatlabToPythonConverter

class TestMatlabToPythonConversion(unittest.TestCase):
    def test_conversion(self, matlab_code, predefined_inputs, expected_outputs, converter_function):
        """
        Helper function to convert MATLAB code to Python and verify correctness for multiple inputs.
        """
        converter = MatlabToPythonConverter()
        # Convert MATLAB code to Python
        python_code = converter.convert_code(matlab_code)

        # Loop through each set of predefined inputs and expected outputs
        for predefined_input, expected_output in zip(predefined_inputs, expected_outputs):
            # Execute the converted Python code
            result = self.execute_python_code(python_code, predefined_input)

            # Assert the result matches the expected output
            self.assertEqual(result, expected_output, 
                             f"Failed for input: {predefined_input}. Expected: {expected_output}, got: {result}")

    def execute_python_code(self, python_code, predefined_input):
        """
        Execute the Python code with predefined input and return the result.
        Assumes the converted Python code stores the final result in a 'result' variable.
        """
        exec_globals = {}
        exec(python_code, predefined_input, exec_globals)
        return exec_globals.get('result')

    # Test cases

    def test_if_else(self):
        matlab_code = """
        if x > 0
            result = 'Positive';
        else
            result = 'Non-positive';
        end
        """
        # Predefined inputs and expected outputs
        predefined_inputs = [{'x': 10}, {'x': -5}]  # x = 10, x = -5
        expected_outputs = ['Positive', 'Non-positive']

        # Run the test for both input scenarios
        self.test_conversion(matlab_code, predefined_inputs, expected_outputs, my_converter_function)

    def test_for_loop(self):
        matlab_code = """
        result = 0;
        for i = 1:n
            result = result + i;
        end
        """
        # Predefined inputs and expected outputs
        predefined_inputs = [{'n': 5}, {'n': 10}]
        expected_outputs = [15, 55]  # 1+2+3+4+5 = 15, 1+2+...+10 = 55

        # Run the test for both input scenarios
        self.test_conversion(matlab_code, predefined_inputs, expected_outputs, my_converter_function)

    def test_function(self):
        matlab_code = """
        function [sum_, product] = my_function(x, y)
            sum_ = x + y;
            product = x * y;
        end
        """
        # Predefined inputs and expected outputs
        predefined_inputs = [{'x': 3, 'y': 4}, {'x': 5, 'y': 6}]
        expected_outputs = [(7, 12), (11, 30)]  # (sum = 7, product = 12), (sum = 11, product = 30)

        # Run the test for both input scenarios
        self.test_conversion(matlab_code, predefined_inputs, expected_outputs, my_converter_function)

    def test_matrix_operations(self):
        matlab_code = """
        A = [1, 2; 3, 4];
        B = [5, 6; 7, 8];
        result = A * B;  % Matrix multiplication
        """
        # Predefined inputs and expected outputs (none needed for this specific test)
        predefined_inputs = [{}]  # No input required for this test
        expected_outputs = [np.array([[19, 22], [43, 50]])]  # Result of A * B

        # Run the test for matrix multiplication
        self.test_conversion(matlab_code, predefined_inputs, expected_outputs, my_converter_function)

    def test_while_loop(self):
        matlab_code = """
        result = 0;
        i = 1;
        while i <= n
            result = result + i;
            i = i + 1;
        end
        """
        # Predefined inputs and expected outputs
        predefined_inputs = [{'n': 5}, {'n': 3}]
        expected_outputs = [15, 6]  # Sum from 1 to 5 = 15, sum from 1 to 3 = 6

        # Run the test for both input scenarios
        self.test_conversion(matlab_code, predefined_inputs, expected_outputs, my_converter_function)

# Assuming my_converter_function is your MATLAB-to-Python conversion function
def my_converter_function(matlab_code):
    # Placeholder conversion logic; replace with actual conversion implementation
    python_code = """
    x = predefined_input.get('x', 0)
    if x > 0:
        result = 'Positive'
    else:
        result = 'Non-positive'
    """
    return python_code

# To run the tests, use the following:
if __name__ == '__main__':
    unittest.main()
