import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* ===========================
BACKGROUND
=========================== */

.stApp{
    background:#0E1117;
}


/* ===========================
SIDEBAR
=========================== */

section[data-testid="stSidebar"]{
    background:#161A23;
    border-right:1px solid #2C3443;
}


/* ===========================
HEADERS
=========================== */

h1{
    font-size:46px !important;
    font-weight:800 !important;
}

h2{
    font-size:34px !important;
    font-weight:700 !important;
}

h3{
    font-size:28px !important;
}


/* ===========================
DIVIDERS
=========================== */

hr{
    border:1px solid #2A3441;
}


/* ===========================
METRICS
=========================== */

div[data-testid="metric-container"]{

    background:#161B22;

    border-radius:18px;

    padding:25px;

    border:1px solid #30363D;

    transition:0.3s;

    box-shadow:
    0px 4px 15px rgba(0,0,0,.30);

}


div[data-testid="metric-container"]:hover{

    transform:translateY(-4px);

    border:1px solid #4F8EF7;

}


/* Metric Label */

div[data-testid="metric-container"] label{

    font-size:15px !important;

    color:#9CA3AF !important;

}


/* Metric Value */

div[data-testid="metric-container"] div{

    font-size:34px !important;

    font-weight:700;

}


/* ===========================
BUTTONS
=========================== */

.stButton>button{

    background:#4F8EF7;

    color:white;

    border-radius:10px;

    border:none;

    padding:10px 22px;

    font-weight:600;

}


.stButton>button:hover{

    background:#2D6CEB;

}


/* ===========================
EXPANDERS
=========================== */

.streamlit-expanderHeader{

    font-size:18px;

    font-weight:700;

}


/* ===========================
TABLES
=========================== */

thead tr th{

    background:#1F2937 !important;

}


tbody tr{

    background:#111827;

}


/* ===========================
SCROLLBAR
=========================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#4F8EF7;

    border-radius:10px;

}

</style>
""",
        unsafe_allow_html=True,
    )