import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
# DtypeWarning: Columns(61, 65, 74, 82, 83, 85) have mixed types.

from streamlit_plotly_events import plotly_events

@st.cache
def get_data():
    columns = ['accession', 'gc_percentage', 'genome_size',
               'gtdb_phylum', 'gtdb_class', 'gtdb_order',
               'gtdb_family', 'gtdb_genus',  'gtdb_species',
               'checkm_completeness', 'checkm_strain_heterogeneity', 'checkm_contamination',
               'ncbi_assembly_level']
    return pd.read_csv('bac120_metadata_r207_edited.csv.gz', usecols=columns)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


st.markdown('# GTDB Genome Explorer')
df = get_data()
tax_options = ['gtdb_phylum', 'gtdb_class', 'gtdb_order',
               'gtdb_family', 'gtdb_genus',  'gtdb_species']
filter_by = st.selectbox('Filter by', tax_options)
filter_value = st.selectbox('To keep', [''] + list(df[filter_by].unique()))
if filter_value:
    fdf = df[df[filter_by] == filter_value]

    if 'gc_points' not in st.session_state:
        st.session_state['gc_points'] = []
    if 'size_points' not in st.session_state:
        st.session_state['size_points'] = []

    st.markdown(f'## GC Percentage - {filter_value}')
    display_options = ['accession', 'gtdb_species', 'gc_percentage', 'genome_size', 'checkm_completeness',
                       'checkm_strain_heterogeneity', 'checkm_contamination', 'ncbi_assembly_level']

    gc_fig = px.strip(fdf, y='gc_percentage',
                           hover_data=display_options,
                           width=800, height=500)

    #c1.plotly_chart(gc_fig, use_container_width=True)
    selected_points = plotly_events(gc_fig, click_event=True, hover_event=False, select_event=True)
    st.session_state['gc_points'] += selected_points
    c1, c2 = st.columns((1, 2))
    if c1.button('Clear'):
        del st.session_state.gc_points
        pt_ids = []
    else:
        pt_ids = [x['pointIndex'] for x in st.session_state.gc_points]

    if pt_ids:
        try:
            pt_df = fdf.iloc[pt_ids].drop_duplicates()
            st.write(pt_df)
            csv = convert_df(pt_df)
            c2.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{filter_value}_gc_percentage.csv',
                mime='text/csv',
            )

        except IndexError:
            del st.session_state.gc_points
            pt_ids = []

    st.markdown(f'## Genome Size - {filter_value}')
    # size_fig = px.histogram(fdf, x='gc_percentage', width=1000, height=500,
    #                              hover_data=['gtdb_genus'])
    #c2.plotly_chart( size_fig, use_container_width=True)

    size_fig = px.strip(fdf, y='genome_size',
                           hover_data=display_options,
                           width=800, height=500)
    size_selected_points = plotly_events(size_fig, click_event=True, hover_event=False, select_event=True)
    st.session_state['size_points'] += size_selected_points

    c3, c4 = st.columns((1, 2))
    if c3.button('Clear', key='size'):
        del st.session_state.size_points
        size_pt_ids = []
    else:
        size_pt_ids = [x['pointIndex'] for x in st.session_state.size_points]
    if size_pt_ids:
        try:
            size_df = fdf.iloc[size_pt_ids].drop_duplicates()
            st.write(size_df)
            csv = convert_df(size_df)

            c4.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{filter_value}_genome_size.csv',
                mime='text/csv',
            )
        except IndexError:
            del st.session_state.size_points
            size_pt_ids = []

    #c3.plotly_chart(size_fig, use_container_width=True)
    # c4.plotly_chart(px.histogram(fdf, x='genome_size', width=1000, height=400,
    #                              hover_data=['gtdb_genus']), use_container_width=True)



    st.markdown(f'## Genome Size vs. GC - {filter_value}')
    st.plotly_chart(px.scatter(fdf, x='genome_size', y='gc_percentage',
                               hover_data=display_options,
                               width=1000, height=600))

