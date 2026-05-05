import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="DNA to Protein Analyzer",
    layout="wide",
    page_icon="🧬"
)

# ================= CODON TABLE =================
CODON_TABLE = {
    'UUU':'F','UUC':'F','UUA':'L','UUG':'L',
    'CUU':'L','CUC':'L','CUA':'L','CUG':'L',
    'AUU':'I','AUC':'I','AUA':'I','AUG':'M',
    'GUU':'V','GUC':'V','GUA':'V','GUG':'V',
    'UCU':'S','UCC':'S','UCA':'S','UCG':'S',
    'CCU':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACU':'T','ACC':'T','ACA':'T','ACG':'T',
    'GCU':'A','GCC':'A','GCA':'A','GCG':'A',
    'UAU':'Y','UAC':'Y','UAA':'Stop','UAG':'Stop',
    'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAU':'N','AAC':'N','AAA':'K','AAG':'K',
    'GAU':'D','GAC':'D','GAA':'E','GAG':'E',
    'UGU':'C','UGC':'C','UGA':'Stop','UGG':'W',
    'CGU':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGU':'S','AGC':'S','AGA':'R','AGG':'R',
    'GGU':'G','GGC':'G','GGA':'G','GGG':'G'
}

# ================= FUNCTIONS =================

def is_valid_dna(seq):
    return all(b in "ATGC" for b in seq) and len(seq) > 0


# ✔ SIMPLIFIED (TEACHER FRIENDLY)
def dna_to_mrna(dna):
    return dna.replace("T", "U")


def find_start(mrna):
    for i in range(len(mrna) - 2):
        if mrna[i:i+3] == "AUG":
            return i
    return -1


def translate(mrna):
    start = find_start(mrna)

    if start == -1:
        return [], [], False, False

    codons = []
    protein = []
    stop_found = False

    for i in range(start, len(mrna) - 2, 3):
        codon = mrna[i:i+3]
        codons.append(codon)

        aa = CODON_TABLE.get(codon, "?")

        if aa == "Stop":
            stop_found = True
            break

        protein.append(aa)

    return codons, protein, True, stop_found


def mutate(seq, pos, base):
    if pos < 1 or pos > len(seq):
        return seq
    return seq[:pos-1] + base + seq[pos:]


def highlight_diff(a, b):
    out = []
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            out.append(f"<span style='color:red;font-weight:bold'>{b[i]}</span>")
        else:
            out.append(b[i])
    if len(b) > len(a):
        for i in range(len(a), len(b)):
            out.append(f"<span style='color:red;font-weight:bold'>{b[i]}</span>")
    return "".join(out)


def format_codons(codons):
    return " ".join(codons)


# ================= UI =================

st.title("🧬 DNA → Protein Analyzer")
st.markdown("### Central Dogma + Mutation Simulator")
st.divider()

# Sidebar
with st.sidebar:
    st.title("📘 About Project")
    st.write("Simulates DNA → RNA → Protein process.")

    st.markdown("### Flow")
    st.write("DNA → mRNA → Protein")

    st.markdown("### Mutation")
    st.write("Single base change effect on protein")

# INPUT
st.header("1. Input DNA Sequence")
dna = st.text_input("Enter DNA (A T G C):", "TACCGTTACTAG").upper()

if dna:

    if not is_valid_dna(dna):
        st.error("Invalid DNA sequence")
    else:

        mrna = dna_to_mrna(dna)
        codons, protein, start_found, stop_found = translate(mrna)

        st.header("2. Results")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("DNA")
            st.code(dna)

            st.subheader("mRNA")
            st.code(mrna)

        with col2:
            st.subheader("Protein")

            if not start_found:
                st.warning("No START codon found (AUG)")
            else:
                st.write("Codons:")
                st.code(format_codons(codons))

                st.write("Amino Acids:")
                st.success("-".join(protein))

                st.write("Length:", len(protein))

                if not stop_found:
                    st.info("No stop codon reached")

        # ================= MUTATION =================
        st.divider()
        st.header("3. Mutation Simulator")

        pos = st.number_input("Position", 1, len(dna), 1)
        base = st.selectbox("New Base", ["A","T","G","C"])

        if st.button("Mutate"):

            mutated_dna = mutate(dna, pos, base)
            mutated_mrna = dna_to_mrna(mutated_dna)
            mcodons, mprotein, mstart, mstop = translate(mutated_mrna)

            st.subheader("Mutation Result")

            c1, c2 = st.columns(2)

            with c1:
                st.write("Mutated DNA")
                st.markdown(highlight_diff(dna, mutated_dna), unsafe_allow_html=True)

                st.write("Mutated mRNA")
                st.markdown(highlight_diff(mrna, mutated_mrna), unsafe_allow_html=True)

            with c2:
                if not mstart:
                    st.warning("No start codon after mutation")
                else:
                    st.write("Mutated Protein")
                    st.success("-".join(mprotein))

                    st.write("Length:", len(mprotein))

                    if mprotein != protein:
                        st.error("Protein changed → Mutation effect detected")
                    else:
                        st.success("Silent mutation (no protein change)")