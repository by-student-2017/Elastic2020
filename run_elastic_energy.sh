#!/bin/bash

# Set number of threads and CPUs
export OMP_NUM_THREADS=1
NCPUs=$(($(nproc) / 2))

# Base input file
base_input="case.scf.in"

# input file
input_file="case.elastic.in"

# Base input file
base_input="case.scf.in"

# input file
input_file="case.elastic.in"

A=$(awk '/A / {print $3; exit} /A=/ {print $2; exit}' "$base_input")

awk -v A="$A" '
  BEGIN { in_cell = 0 }
  /^CELL_PARAMETERS/ { print; in_cell = 1; next }
  in_cell && NF == 3 {
    printf "  %.15f   %.15f   %.15f\n", $1*A, $2*A, $3*A
    next
  }
  in_cell && NF != 3 { in_cell = 0 }
  { print }c
' "$base_input" > "$input_file"

# Create a temporary input file for ElaStic_Setup
cat <<EOF > set_stress.txt
1
2
case.elastic.in
0.030
6
EOF

# Run ElaStic_Setup with the input file
python3 $HOME/Elastic2020/ElaStic_Setup < set_stress.txt

# copy pseudo-potentials
cp *.UPF ./Structures_ESPRESSO/

# Navigate to Structures_ESPRESSO directory
cd Structures_ESPRESSO

# Run Quantum ESPRESSO calculations for each Dst*_*,in file
for infile in Dst*_*.in; do
  sed -i '/^[[:space:]]*A[[:space:]]*=/d' "$infile"
  
  # base = Dst01_01
  base="${infile%.in}"
  
  # subdir = Dst01
  subdir="${base%%_*}"
  
  # output file (e.g., Dst01_01.out)
  outfile="${infile%.in}.out"
  
  echo "Running $infile -> $outfile"
  mpirun -np ${NCPUs} pw.x < "$infile" > "$outfile"
  
  cp "$outfile" "./../${subdir}/${base}/$outfile"
done

# Return to the main directory and run ElaStic_Analyze_Energy
cd ..
#python3 $HOME/Elastic2020/ElaStic_Analyze_Energy
python3 $HOME/Elastic2020/ElaStic_Analyze

python3 $HOME/Elastic2020/ElaStic_Result
