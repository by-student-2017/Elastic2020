import numpy as np
import pandas as pd

# Definition of the strain tensor
Ls_Dic = {
    '36':[ 1., 2., 3., 4., 5., 6.],
    '37':[-2., 1., 4.,-3., 6.,-5.],
    '38':[ 3.,-5.,-1., 6., 2.,-4.],
    '42':[ 1., 1., 0., 2., 0., 0.],
    '43':[ 1., 0., 1., 0., 2., 0.]
}

# Number of tensor components per LC
LC_components = {
    'CI':  6, 'CII':  8, 'HI': 10, 'HII': 12,
    'RI': 14, 'RII': 14, 'TI':  8, 'TII': 10,
    'O' : 10, 'M': 12, 'N': 15
}

# Distortion introduction list for each LC
LC_strains = {
    'CI' : ['36', '42', '43'],
    'CII': ['36', '42'],
    'HI' : ['36', '38', '42'],
    'HII': ['36', '38'],
    'RI' : ['36', '38', '42'],
    'RII': ['36', '38', '42'],
    'TI' : ['36', '38', '42'],
    'TII': ['36', '38', '42'],
    'O'  : ['36', '42', '43'],
    'M'  : ['36', '38', '42', '43'],
    'N'  : ['36', '37', '38', '42', '43']
}

# Function to generate Cijk labels
def generate_Cijk_labels(n):
    labels = []
    for i in range(1, n+1):
        if i <= 6:
            labels.append(f'C11{i}')
        elif i <= 10:
            labels.append(f'C12{i-6}')
        elif i <= 14:
            labels.append(f'C13{i-10}')
        else:
            labels.append(f'C14{i-14}')
    return labels

# Function to generate the configuration matrix
def generate_matrix(LC):
    strain_keys = LC_strains[LC]
    num_components = LC_components[LC]
    matrix_rows = []
    for key in strain_keys:
        strain = Ls_Dic[key]
        for i in range(6):  # 6 stress components for each strain
            row = [strain[i] * (j + 1) for j in range(num_components)]
            matrix_rows.append(row)
    return np.array(matrix_rows)

# Dictionary to store matrices
matrices = {}

# Generate and display matrices for all LC values
for LC in LC_components.keys():
    matrix = generate_matrix(LC)
    labels = generate_Cijk_labels(LC_components[LC])
    df = pd.DataFrame(matrix, columns=labels)
    matrices[LC] = df
    print(f"\nMatrix for LC = '{LC}' with shape {matrix.shape}")
    print(df)

# Print disclaimer and explanation to console
print("")
print("DISCLAIMER:")
print("The matrices generated below are based on a simplified theoretical model and may differ from those presented in the following publication:")
print("R. Golesorkhtabar et al., ElaStic: A tool for calculating second-order elastic constants from first principles, CPC 184, 1861 (2013).")
print("These matrices are intended for educational and conceptual purposes. Future researchers are encouraged to refine and validate the model.\n")
print("The matrices are constructed using the following formula:")
print("  For each strain tensor ε and each stress component sigma_i (i = 1 to 6),")
print("  the row vector is defined as: [epsilon_i * 1, epsilon_i * 2, ..., epsilon_i * N],")
print("  where N is the number of independent elastic tensor components for the given lattice configuration (LC).\n")
print("Note on Voigt notation:")
print("  In Voigt notation, the symmetric strain and stress tensors are represented as 6-component vectors:")
print("    epsilon = [e11, e22, e33, 2e23, 2e13, 2e12]")
print("    sigma   = [s11, s22, s33, s23,  s13,  s12]")
print("  This notation is used to simplify the representation of second-order tensors in matrix form.\n")

# Write the matrices to a text file in np.mat([...]) format
with open("python3-code.txt", "w") as f:
    f.write("# DISCLAIMER:\n")
    f.write("# The matrices generated below are based on a simplified theoretical model and may differ from those presented in the following publication:\n")
    f.write("# R. Golesorkhtabar et al., ElaStic: A tool for calculating second-order elastic constants from first principles, CPC 184, 1861 (2013).\n")
    f.write("# These matrices are intended for educational and conceptual purposes. Future researchers are encouraged to refine and validate the model.\n\n")
    f.write("# The matrices are constructed using the following formula:\n")
    f.write("#   For each strain tensor ε and each stress component sigma_i (i = 1 to 6),\n")
    f.write("#   the row vector is defined as: [epsilon_i * 1, epsilon_i * 2, ..., epsilon_i * N],\n")
    f.write("#   where N is the number of independent elastic tensor components for the given lattice configuration (LC).\n\n")
    f.write("# Note on Voigt notation:\n")
    f.write("#   In Voigt notation, the symmetric strain and stress tensors are represented as 6-component vectors:\n")
    f.write("#     epsilon = [e11, e22, e33, 2e23, 2e13, 2e12]\n")
    f.write("#     sigma   = [s11, s22, s33, s23,  s13,  s12]\n")
    f.write("#   This notation is used to simplify the representation of second-order tensors in matrix form.\n\n")

    # Write matrices
    for LC in LC_components.keys():
        matrix = generate_matrix(LC)
        labels = generate_Cijk_labels(LC_components[LC])
        f.write("#     " + "  ".join(f"{label:>6}" for label in labels) + "\n")
        f.write(f"if (LC == '{LC}'):\n")
        f.write("    Matrix = np.mat([\n")
        for row in matrix:
            row_str = ", ".join(f"{val:5.1f}" for val in row)
            f.write(f"        [{row_str}],\n")
        f.write("    ])\n\n")

print("The configuration matrices and disclaimer have been written to 'python3-code.txt'.")
