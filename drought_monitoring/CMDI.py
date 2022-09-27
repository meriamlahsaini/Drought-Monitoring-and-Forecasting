import streamlit as st


@st.experimental_memo
def compute_CMDI(VCI, TCI, PCI, ETCI, SMCI, weights, roi):
    wVCI = VCI.clip(roi).multiply(weights[0])
    wTCI = TCI.clip(roi).multiply(weights[1]) 
    wPCI = PCI.clip(roi).multiply(weights[2])
    wETCI = ETCI.clip(roi).multiply(weights[3]) 
    wSMCI = SMCI.clip(roi).multiply(weights[4])  
 
    return  wVCI.add(wTCI).add(wPCI).add(wETCI).add(wSMCI)
