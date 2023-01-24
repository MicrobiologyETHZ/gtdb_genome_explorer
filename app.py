import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
# DtypeWarning: Columns(61, 65, 74, 82, 83, 85) have mixed types.


@st.cache
def get_data():
    columns = ['accession', 'gc_percentage', 'genome_size',
               'gtdb_phylum', 'gtdb_class', 'gtdb_order',
               'gtdb_family', 'gtdb_genus',  'gtdb_species',
               'checkm_completeness', 'checkm_strain_heterogeneity', 'checkm_contamination',
               'ncbi_assembly_level']
    return pd.read_csv('bac120_metadata_r207_edited.csv.gz', usecols=columns)

st.markdown('# GTDB Genome Explorer')
df = get_data()
tax_options = ['gtdb_phylum', 'gtdb_class', 'gtdb_order',
               'gtdb_family', 'gtdb_genus',  'gtdb_species']
filter_by = st.selectbox('Filter by', tax_options)
filter_value = st.selectbox('To keep', [''] + list(df[filter_by].unique()))
if filter_value:
    fdf = df[df[filter_by] == filter_value]

    st.markdown(f'## GC Percentage - {filter_value}')
    c1, c2 = st.columns((1, 2))
    display_options = ['accession', 'gtdb_species', 'gc_percentage', 'genome_size', 'checkm_completeness',
                       'checkm_strain_heterogeneity', 'checkm_contamination', 'ncbi_assembly_level']
    c1.plotly_chart(px.box(fdf, y='gc_percentage', points='all',
                           hover_data=display_options,
                           width=400, height=400), use_container_width=True)
    c2.plotly_chart(px.histogram(fdf, x='gc_percentage', width=1000, height=400,
                                 hover_data=['gtdb_genus']), use_container_width=True)

    st.markdown(f'## Genome Size - {filter_value}')
    c3, c4 = st.columns((1, 2))

    c3.plotly_chart(px.box(fdf, y='genome_size', points='all',
                           hover_data=display_options,
                           width=400, height=400), use_container_width=True)
    c4.plotly_chart(px.histogram(fdf, x='genome_size', width=1000, height=400,
                                 hover_data=['gtdb_genus']), use_container_width=True)
    st.markdown(f'## Genome Size vs. GC - {filter_value}')
    st.plotly_chart(px.scatter(fdf, x='genome_size', y='gc_percentage',
                               hover_data=display_options,
                               width=1000, height=600))

