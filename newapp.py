import streamlit as st
import math

def validate_dna(sequence):
    sequence = sequence.upper()
    valid_nucleotides = set("ATCG")
    if not sequence:
        return False
    for letter in sequence:
        if letter not in valid_nucleotides:
            return False
    return True

def count_nucleotide_frequency(sequence):
    sequence = sequence.upper()
    total = len(sequence)
    frequencies = {}
    for n in ['A', 'T', 'C', 'G']:
        count = sequence.count(n)
        pct = (count / total) * 100 if total > 0 else 0
        frequencies[n] = {"count": count, "percentage": pct}
    return frequencies

def calculate_gc_content(sequence):
    sequence = sequence.upper()
    total_length = len(sequence)
    if total_length == 0: 
        return 0.0
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return ((g_count + c_count) / total_length) * 100

def generate_complementary_strand(sequence):
    sequence = sequence.upper()
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(complement_dict[letter] for letter in sequence)

def transcribe_dna_to_mrna(sequence):
    sequence = sequence.upper()
    # Define the exact biological mapping from DNA template to mRNA
    transcription_map = str.maketrans({
        'A': 'U',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    })
    return sequence.translate(transcription_map)

def translate_mrna_to_protein(mrna_sequence):
    mrna_sequence = mrna_sequence.upper()
    genetic_code = {
        'AUG': 'Methionine (START)', 'UUU': 'Phenylalanine', 'UUC': 'Phenylalanine',
        'UUA': 'Leucine', 'UUG': 'Leucine', 'CUU': 'Leucine', 'CUC': 'Leucine',
        'CUA': 'Leucine', 'CUG': 'Leucine', 'AUU': 'Isoleucine', 'AUC': 'Isoleucine',
        'AUA': 'Isoleucine', 'GUU': 'Valine', 'GUC': 'Valine', 'GUA': 'Valine',
        'GUG': 'Valine', 'GCU': 'Alanine', 'GCC': 'Alanine', 'GCA': 'Alanine',
        'GCG': 'Alanine', 'UGU': 'Cysteine', 'UGC': 'Cysteine', 'UAA': 'STOP',
        'UAG': 'STOP', 'UGA': 'STOP'
    }
    protein_sequence = []
    for i in range(0, len(mrna_sequence) - 2, 3):
        codon = mrna_sequence[i:i+3]
        amino_acid = genetic_code.get(codon, "Unknown")
        protein_sequence.append(amino_acid)
        if amino_acid == "STOP":
            break
    return " -> ".join(protein_sequence)

def calculate_molecular_weight(sequence):
    sequence = sequence.upper()
    weights = {'A': 313.2, 'T': 304.2, 'C': 289.2, 'G': 329.2}
    total_weight = sum(weights[letter] for letter in sequence)
    if len(sequence) > 0:
        total_weight += 15.9
    return total_weight

def find_cpg_islands(sequence):
    sequence = sequence.upper()
    islands = []
    for i in range(len(sequence) - 1):
        if sequence[i:i+2] == "CG":
            islands.append(i)
    return islands

def calculate_melting_temperature(sequence):
    sequence = sequence.upper()
    length = len(sequence)
    if length == 0:
        return 0.0
    a_count = sequence.count('A')
    t_count = sequence.count('T')
    c_count = sequence.count('C')
    g_count = sequence.count('G')
    if length < 14:
        return 2 * (a_count + t_count) + 4 * (g_count + c_count)
    else:
        return 64.9 + 41 * (g_count + c_count - 16.4) / (a_count + t_count + g_count + c_count)

def generate_reverse_complement(sequence):
    complement = generate_complementary_strand(sequence)
    return complement[::-1]

def calculate_purine_pyrimidine_skew(sequence):
    sequence = sequence.upper()
    purines = sequence.count('A') + sequence.count('G')
    pyrimidines = sequence.count('T') + sequence.count('C')
    total = purines + pyrimidines
    if total == 0:
        return 0.0, 0.0
    return (purines / total) * 100, (pyrimidines / total) * 100

if __name__ == "__main__":
    st.set_page_config(page_title="Advanced Genomics Dashboard", layout="centered")
    st.title("🧬 Advanced Genomics & Bioinformatics Toolkit")
    st.markdown("---")
    
    user_input = st.text_area("Enter raw DNA Sequence (A, T, C, G only):", height=150)
    user_input = user_input.strip().replace(" ", "").replace("\n", "")
    
    tasks = [
        "1. Nucleotide Frequency & Distribution",
        "2. GC Content Ratio & Thermal Estimation",
        "3. Generate Complementary DNA Strand",
        "4. Transcribe DNA to mRNA Strand",
        "5. Translate mRNA Sequence to Protein Chain",
        "6. Calculate Total DNA Molecular Weight",
        "7. Locate CpG Islands (Regulatory Regions)",
        "8. Calculate Primer Melting Temperature (Tm)",
        "9. Generate Reverse Complement Strand",
        "10. Purine vs Pyrimidine Skew Analysis"
    ]
    
    selected_task = st.selectbox("Select Bioinformatics Analysis Task:", tasks)
    
    if st.button("Run Analytical Pipeline", type="primary"):
        if not user_input:
            st.error("Execution Failed: Input sequence is entirely empty.")
        elif not validate_dna(user_input):
            st.error("Execution Failed: Found invalid characters. Only A, T, C, and G are permitted.")
        else:
            st.success("Sequence Check Passed: Valid DNA Structure Detected.")
            st.markdown("### Analysis Results")
            
            if selected_task.startswith("1."):
                # 1. Calculate the total count of all bases combined
                total_bases = len(user_input)
                st.subheader(f"Total Length: {total_bases} Nitrogenous Bases")
                st.markdown("---")
                
                # 2. Display the individual frequency and percentage for each base
                freq = count_nucleotide_frequency(user_input)
                for base, info in freq.items():
                    st.metric(
                        label=f"Nucleotide Base {base}", 
                        value=f"{info['count']} counts", 
                        delta=f"{info['percentage']:.2f}%"
                    )
                    
            elif selected_task.startswith("2."):
                gc = calculate_gc_content(user_input)
                st.metric("GC Content Percentage", f"{gc:.2f}%")
                if gc > 50.0:
                    st.info("Biological Interpretation: High thermal stability due to triple hydrogen bonding.")
                else:
                    st.info("Biological Interpretation: Low thermal stability due to double hydrogen bonding.")
                    
            elif selected_task.startswith("3."):
                comp = generate_complementary_strand(user_input)
                st.text_area("Complementary DNA Strand (5' -> 3'):", comp, height=70)
                
            elif selected_task.startswith("4."):
                mrna = transcribe_dna_to_mrna(user_input)
                st.text_area("Transcribed mRNA Transcript:", mrna, height=70)
                
            elif selected_task.startswith("5."):
                mrna_strand = transcribe_dna_to_mrna(user_input)
                protein = translate_mrna_to_protein(mrna_strand)
                st.text_area("Resulting Amino Acid Peptide Chain:", protein, height=100)
                
            elif selected_task.startswith("6."):
                weight = calculate_molecular_weight(user_input)
                st.metric("Calculated Molecular Weight", f"{weight:.2f} g/mol (Da)")
                
            elif selected_task.startswith("7."):
                positions = find_cpg_islands(user_input)
                st.write(f"Total CpG dinucleotides found: **{len(positions)}**")
                if positions:
                    st.write(f"Identified starting index positions: {positions}")
                    
            elif selected_task.startswith("8."):
                tm = calculate_melting_temperature(user_input)
                st.metric("Melting Temperature (Tm)", f"{tm:.1f} °C")
                
            elif selected_task.startswith("9."):
                rev_comp = generate_reverse_complement(user_input)
                st.text_area("Reverse Complement Strand (3' -> 5' flipped):", rev_comp, height=70)
                
            elif selected_task.startswith("10."):
                pur, pyr = calculate_purine_pyrimidine_skew(user_input)
                col1, col2 = st.columns(2)
                col1.metric("Purines Ratio (A + G)", f"{pur:.2f}%")
                col2.metric("Pyrimidines Ratio (T + C)", f"{pyr:.2f}%")